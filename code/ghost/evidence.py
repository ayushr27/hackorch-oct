"""Evidence parsers → normalised Observations and Scope records.

Every evidence family (SQL inventory / replica dumps, JSON exports, bundles and
ledgers, handover text, seven log syntaxes, PDFs) is reduced to:

* ``Observation``: what one source said about one resource at one moment
  (state + the identifier tokens that link it to a person).
* ``Scope``: "this capture covered system S at time T and listed exactly these
  resources" — the basis for proving absence by omission.

States: ABSENT, PII (present with direct identifiers), CLEAN (present with no
direct identifiers / only a stable user reference), ACTIVE (flow enabled or
restore allowed), INACTIVE (flow disabled or restore blocked).
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass, field

from .core import (CACHE_DIR, RESOURCE_RE, ManifestEntry, norm_ident, norm_ts, text_idents)

ABSENT, PII, CLEAN, ACTIVE, INACTIVE = "ABSENT", "PII", "CLEAN", "ACTIVE", "INACTIVE"

PREFIX_SYSTEM = {
    "account": "account_service", "search": "search_service", "analytics": "analytics_platform",
    "support": "support_platform", "export": "export_service", "data_flow": "integration_service",
    "backup": "backup_service", "audit_record": "security_service", "tombstone": "identity_service",
    "legal_hold": "legal_service", "marketing": "marketing_platform", "object": "object_storage",
}

# Fields that are direct identifiers wherever they appear.
DIRECT_FIELDS = {"full_name", "name", "display_name", "email", "phone", "email_hash",
                 "requester_name", "requester_email", "requester_phone", "owner_email",
                 "owner_phone", "customer_email", "uploaded_by"}
# Stable references: allowed on redacted support records / tombstones, but they keep an
# analytics record attributable, so analytics treats them as identifying.
REF_FIELDS = {"customer_reference", "user_id", "subject_reference", "subject_selector"}
FREE_TEXT_FIELDS = {"message_text", "message_excerpt"}


def resource_prefix(resource_id: str) -> str:
    return resource_id.rsplit("_", 1)[0]


def system_for(resource_id: str) -> str | None:
    return PREFIX_SYSTEM.get(resource_prefix(resource_id))


@dataclass(frozen=True)
class Observation:
    file_id: str
    file_time: str          # manifest captured_at of the containing file
    rec_time: str           # time the observation itself refers to
    system_id: str
    resource_id: str
    state: str
    idents: frozenset
    source: str             # parser family, for traces
    category: str | None = None   # explicit policy data category when the source states one
    extra: tuple = ()       # (key, value) pairs, e.g. dependency links


@dataclass(frozen=True)
class Scope:
    file_id: str
    file_time: str
    rec_time: str
    system_id: str
    listed: frozenset


@dataclass
class EvidenceIndex:
    observations: list[Observation] = field(default_factory=list)
    scopes: list[Scope] = field(default_factory=list)
    texts: dict[str, str] = field(default_factory=dict)   # file_id -> extracted text (PDF)


# ------------------------------------------------------------------ helpers

def _idents_of(rec: dict) -> set[str]:
    out = set()
    for k, v in rec.items():
        if isinstance(v, dict):
            out |= _idents_of(v)
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, dict):
                    out |= _idents_of(x)
        elif k in FREE_TEXT_FIELDS and isinstance(v, str):
            out |= text_idents(v)
        else:
            t = norm_ident(v)
            if t:
                out.add(t)
    return out


def _has_direct(rec: dict, refs_identify: bool) -> bool:
    for k, v in rec.items():
        if isinstance(v, dict):
            if _has_direct(v, refs_identify):
                return True
            continue
        if isinstance(v, list):
            continue
        if v in (None, "", "null"):
            continue
        if k in DIRECT_FIELDS:
            return True
        if k in REF_FIELDS:
            if refs_identify or (norm_ident(v) or "").count("@"):
                return True
        if k in FREE_TEXT_FIELDS and isinstance(v, str):
            if any(not t.startswith("user_") for t in text_idents(v)):
                return True
    return False


def _truthy(v) -> bool:
    return str(v).strip().lower() in ("1", "true", "yes")


def record_state(system: str, rec: dict) -> str:
    """State of a record that is known to exist in a capture."""
    if system == "integration_service":
        return ACTIVE if _truthy(rec.get("enabled")) else INACTIVE
    if system == "backup_service":
        return ACTIVE if _truthy(rec.get("restore_allowed")) else INACTIVE
    if system in ("security_service", "legal_service"):
        return CLEAN
    return PII if _has_direct(rec, refs_identify=(system == "analytics_platform")) else CLEAN


def _category_for(system: str, collection: str | None) -> str | None:
    if system == "support_platform":
        if collection in ("ticket_attachments",):
            return "SUPPORT_ATTACHMENT"
        if collection in ("support_conversations",):
            return "SUPPORT_MESSAGE"
    return None


# --------------------------------------------------------------------- SQL

INVENTORY_TABLES = {
    "customer_profiles": "account_service", "customer_search_documents": "search_service",
    "customer_analytics_profiles": "analytics_platform", "support_records": "support_platform",
    "customer_exports": "export_service", "connector_subscriptions": "integration_service",
    "backup_restore_entries": "backup_service", "security_audit_records": "security_service",
}


def _load_sql(path) -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.row_factory = sqlite3.Row
    con.executescript(path.read_text(encoding="utf-8"))
    return con


def _parse_sql(m: ManifestEntry, idx: EvidenceIndex):
    con = _load_sql(m.path)
    tables = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
    cap = m.captured_at
    if "snapshot_scope" in tables:                      # typed inventory snapshot
        scope_time = {r["origin_system"]: norm_ts(r["captured_at"])
                      for r in con.execute("select * from snapshot_scope")}
        for table, system in INVENTORY_TABLES.items():
            rows = [dict(r) for r in con.execute(f'select * from "{table}"')]
            if system not in scope_time:
                continue
            t = scope_time[system]
            for rec in rows:
                idx.observations.append(Observation(
                    m.file_id, cap, t, system, rec["resource_id"], record_state(system, rec),
                    frozenset(_idents_of(rec)), "sql_inventory:" + table))
            idx.scopes.append(Scope(m.file_id, cap, t, system,
                                    frozenset(r["resource_id"] for r in rows)))
        return
    if "customer_profiles_primary" in tables:           # account primary + failover replica
        listed = set()
        for table in [t for t in tables if t.startswith("customer_profiles_")]:
            for r in con.execute(f'select * from "{table}"'):
                rec = dict(r)
                listed.add(rec["resource_id"])
                idx.observations.append(Observation(
                    m.file_id, cap, cap, "account_service", rec["resource_id"],
                    record_state("account_service", rec), frozenset(_idents_of(rec)),
                    "sql_accounts:" + table))
        idx.scopes.append(Scope(m.file_id, cap, cap, "account_service", frozenset(listed)))
        return
    if "search_documents_primary" in tables:            # search primary
        listed = set()
        for r in con.execute('select * from "search_documents_primary"'):
            rec = dict(r)
            listed.add(rec["resource_id"])
            extra = (("source_resource_id", rec.get("source_resource_id")),)
            idx.observations.append(Observation(
                m.file_id, cap, cap, "search_service", rec["resource_id"],
                record_state("search_service", {k: v for k, v in rec.items()
                                                if k != "source_resource_id"}),
                frozenset(_idents_of(rec)), "sql_search_primary", None, extra))
        idx.scopes.append(Scope(m.file_id, cap, cap, "search_service", frozenset(listed)))
        return
    # Primary + replica tables holding record_json; present in any table = present.
    data_tables = [t for t in tables if t.startswith("customer_data_")]
    seen: dict[str, tuple] = {}
    systems = {"account_service"}
    for table in data_tables:
        for r in con.execute(f'select * from "{table}"'):
            rec = json.loads(r["record_json"])
            system = r["origin_system"]
            systems.add(system)
            seen.setdefault(r["resource_id"], (system, r["collection_name"], rec, []))[3].append(table)
    by_system: dict[str, set] = {s: set() for s in systems}
    for rid, (system, coll, rec, where) in seen.items():
        by_system[system].add(rid)
        idx.observations.append(Observation(
            m.file_id, cap, cap, system, rid, record_state(system, rec), frozenset(_idents_of(rec)),
            "sql_replica:" + coll, _category_for(system, coll), (("tables", ",".join(where)),)))
    for system, listed in by_system.items():
        idx.scopes.append(Scope(m.file_id, cap, cap, system, frozenset(listed)))


# -------------------------------------------------------------------- JSON

LEDGER_STATE = {"NOT_FOUND": ABSENT, "IDENTIFIABLE": PII, "ANONYMIZED": CLEAN, "REDACTED": CLEAN,
                "ACTIVE": ACTIVE, "DISABLED": INACTIVE, "BLOCKED": INACTIVE}
RETAINED_CATEGORIES = {"SECURITY_AUDIT_LOG", "LEGAL_HOLD_RECORD"}


def ledger_state(result: str, category: str) -> str:
    result = result.strip().upper()
    if result == "FOUND":
        return CLEAN if category in RETAINED_CATEGORIES else PII
    return LEDGER_STATE.get(result, PII)


def _ledger_obs(m, rec_time, system, rid, category, result, subject, source):
    toks = set()
    t = norm_ident(subject)
    if t:
        toks.add(t)
    return Observation(m.file_id, m.captured_at, norm_ts(rec_time), system, rid,
                       ledger_state(result, category), frozenset(toks), source,
                       category if category != "DATA_FLOW" else None)


COLLECTION_SYSTEM = {"customer_analytics_reports": "analytics_platform",
                     "customer_export_jobs": "export_service"}


def _parse_json(m: ManifestEntry, idx: EvidenceIndex):
    d = json.loads(m.path.read_text(encoding="utf-8"))
    cap = m.captured_at
    if "service_exports" in d:
        t_export = norm_ts(d["exported_at"])
        for system, cols in d["service_exports"].items():
            listed = set()
            for coll, recs in cols.items():
                for rec in recs:
                    rid = rec["resource_id"]
                    listed.add(rid)
                    t = norm_ts(rec.get("observed_at") or d["exported_at"])
                    if system == "account_service":
                        state = ABSENT if int(rec.get("status_code", 200)) == 404 or not rec.get("profile") \
                            else record_state(system, rec.get("profile") or {})
                        if state == CLEAN:
                            state = PII
                        toks = _idents_of(rec.get("profile") or {})
                    elif system == "search_service":
                        docs = rec.get("hits", {}).get("documents", [])
                        state = PII if docs else ABSENT
                        toks = _idents_of(rec)
                    else:
                        body = {k: v for k, v in rec.items() if k not in ("observed_at", "resource_id")}
                        state = record_state(system, body)
                        toks = _idents_of(body)
                    idx.observations.append(Observation(m.file_id, cap, t, system, rid, state,
                                                        frozenset(toks), "json_service_export:" + coll))
                    if system == "search_service":
                        for doc in rec.get("hits", {}).get("documents", []):
                            if doc.get("resource_id") and doc["resource_id"] != rid:
                                listed.add(doc["resource_id"])
            idx.scopes.append(Scope(m.file_id, cap, t_export, system, frozenset(listed)))
        return
    if "snapshots" in d:
        for snap in d["snapshots"]:
            t = norm_ts(snap["captured_at"])
            store, coll = snap["data_store"], snap["collection"]
            if coll == "operational_record_history":
                for rec in snap["records"]:
                    idx.observations.append(_ledger_obs(
                        m, rec["recorded_at"], rec["system"], rec["resource_id"], rec["record_type"],
                        rec["result"], rec.get("lookup_value"), "json_bundle_ledger"))
                continue
            listed = set()
            for rec in snap["records"]:
                listed.add(rec["resource_id"])
                body = {k: v for k, v in rec.items() if k != "resource_id"}
                idx.observations.append(Observation(
                    m.file_id, cap, t, store, rec["resource_id"], record_state(store, body),
                    frozenset(_idents_of(body)), "json_bundle:" + coll, _category_for(store, coll)))
            idx.scopes.append(Scope(m.file_id, cap, t, store, frozenset(listed)))
        return
    if "records" in d and d["records"] and "record_type" in d["records"][0]:   # generic ledger
        for rec in d["records"]:
            idx.observations.append(_ledger_obs(
                m, rec["recorded_at"], rec["system"], rec["resource_id"], rec["record_type"],
                rec["result"], rec.get("subject_reference"), "json_ledger"))
        return
    if "collection" in d:                                   # focused single-collection report
        system = COLLECTION_SYSTEM.get(d["collection"])
        t = norm_ts(d.get("captured_at") or cap)
        for rec in d["records"]:
            body = {k: v for k, v in rec.items() if k != "resource_id"}
            sys_ = system or system_for(rec["resource_id"])
            state = record_state(sys_, body)
            if sys_ == "export_service" and not _truthy(rec.get("download_available", True)):
                state = CLEAN
            idx.observations.append(Observation(m.file_id, cap, t, sys_, rec["resource_id"], state,
                                                frozenset(_idents_of(body)), "json_report:" + d["collection"]))
        return
    raise ValueError(f"unrecognised JSON evidence layout: {m.path.name}")


# --------------------------------------------------------------- handover

HANDOVER_RE = re.compile(r"^- (\S+) \| (\S+) \| (\S+) \| (\S+) \| (\S+) \| (.+)$")


def _parse_txt(m: ManifestEntry, idx: EvidenceIndex):
    for line in m.path.read_text(encoding="utf-8").splitlines():
        mm = HANDOVER_RE.match(line.strip())
        if mm:
            ts, system, rid, category, result, subject = mm.groups()
            idx.observations.append(_ledger_obs(m, ts, system, rid, category, result, subject.strip(),
                                                "txt_handover"))


# ------------------------------------------------------------------- logs

KV_RE = re.compile(r'(\w+)=("(?:[^"\\]|\\.)*"|\S+)')
TRACE_RE = re.compile(r"(?<![\w-])(tr-[A-Za-z0-9-]+|rb-\d+-\d+)")


def _kv(s: str) -> dict:
    return {k: (v[1:-1].replace('\\"', '"') if v.startswith('"') else v) for k, v in KV_RE.findall(s)}


def parse_log_line(line: str) -> dict | None:
    """One log line in any of the seven syntaxes → flat dict (ts, service, trace, event, fields)."""
    ts, rest = line[:20], line[21:]
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", ts):
        return None
    if rest.startswith("{"):
        d = {k: (str(v) if v is not None else None) for k, v in json.loads(rest).items()}
    elif (mm := re.match(r"<\d+>1 (\S+) (\S+) (\S+) - - (.*)", rest)):
        d = _kv(mm.group(4)); d.update(service=mm.group(2), trace_id=mm.group(3))
    elif (mm := re.match(r'requestId=(\S+) level=(\S+) function=(\S+) message="(.*)"$', rest)):
        d = _kv(mm.group(4).replace('\\"', '"')); d.update(trace_id=mm.group(1), service=mm.group(3))
    elif (mm := re.match(r"\| (\w+) \| (\S+) \| (\S+) \| (\S+) \| (.*)", rest)):
        d = _kv(mm.group(5)); d.update(service=mm.group(2), trace_id=mm.group(3), event=mm.group(4))
    elif (mm := re.match(r"\[(\w+)\] \[(\S+)\] \[(\S+)\] (\w+): (.*)", rest)):
        d = _kv(mm.group(5)); d.update(service=mm.group(2), trace_id=mm.group(3), event=mm.group(4))
    elif (mm := re.match(r"(?:INFO|WARN|DEBUG|ERROR) (.*)", rest)):
        d = _kv(mm.group(1))
    else:
        d = _kv(rest)
    d["ts"] = ts
    tm = TRACE_RE.search(str(d.get("trace_id") or ""))
    d["trace"] = tm.group(1) if tm else None
    return d


LOG_SERVICE_SYSTEM = {"support_replica": "support_platform"}
IGNORED_LOG_SERVICES = {"profile_service"}   # 5-digit decoy ids; not a system of record
IDENT_KEYS = {"lookup_key", "match_key", "subject_key", "scan_key", "subject_ref", "owner_key",
              "correlation_key", "matched_value", "email", "customer_reference", "customer_email",
              "requester_email", "requester_phone", "requester_name", "subject_reference",
              "owner_email", "phone", "email_hash"}


def _null(v) -> bool:
    return v is None or str(v).strip().lower() in ("", "null", "none")


def log_event_state(e: dict) -> tuple[str, str | None] | None:
    """(state, category) for a state-bearing log event, None otherwise."""
    ev = e.get("event")
    g = lambda k: str(e.get(k, "")).strip().lower()
    if ev == "profile_lookup_completed":
        return (ABSENT if g("rows") == "0" or g("http_status") == "404" else PII), None
    if ev == "index_query_completed":
        return (PII if g("result") == "hit" else ABSENT), None
    if ev == "audit_record_read_completed":
        return (ABSENT if g("rows") == "0" else CLEAN), None
    if ev in ("connector_config_read_completed", "connector_heartbeat", "connector_config_loaded"):
        return (ACTIVE if g("enabled") == "true" else INACTIVE), None
    if ev == "analytics_profile_read_completed":
        ids = any(not _null(e.get(k)) for k in ("customer_reference", "email", "phone", "email_hash"))
        return (PII if ids else CLEAN), None
    if ev == "analytics_profile_read":
        clean = g("direct_identifiers") == "0" and _null(e.get("email")) and _null(e.get("phone"))
        return (CLEAN if clean else PII), None
    if ev == "analytics_identity_scan":
        return PII, None
    if ev == "contact_lookup_completed":
        return (PII if g("rows") not in ("0", "") else ABSENT), "MARKETING_PROFILE"
    if ev == "support_ticket_read_completed":
        ids = any(not _null(e.get(k)) for k in ("requester_name", "requester_email", "requester_phone"))
        return (PII if ids else CLEAN), None
    if ev == "message_pii_scan":
        return PII, "SUPPORT_MESSAGE"
    if ev == "attachment_pii_scan":
        return PII, "SUPPORT_ATTACHMENT"
    if ev == "message_read":
        return (CLEAN if "[redacted]" in g("message_text") else PII), "SUPPORT_MESSAGE"
    if ev == "restore_policy_read_completed":
        return (ACTIVE if g("restore_allowed") == "true" else INACTIVE), None
    if ev == "restore_candidate_evaluated":
        allowed = g("eligible") == "true" and g("deletion_block") != "true"
        return (ACTIVE if allowed else INACTIVE), None
    if ev == "restore_authorization_completed":
        return (INACTIVE if g("decision") == "deny" else ACTIVE), None
    if ev in ("export_download_check_completed", "export_metadata_read_completed"):
        return (PII if g("available") == "true" else ABSENT), None
    if ev == "retained_order_loaded":
        return (CLEAN if g("access") != "denied" else ABSENT), None
    if ev == "contact_query_completed":
        return (PII if g("rows") not in ("0", "") else ABSENT), None
    if ev == "deletion_marker_check":
        return (PII if g("marker_found") == "false" else ABSENT), None
    return None


def _parse_log(m: ManifestEntry, idx: EvidenceIndex):
    lines = [parse_log_line(l) for l in m.path.read_text(encoding="utf-8").splitlines() if l.strip()]
    groups: dict[str, list[dict]] = {}
    for i, e in enumerate(lines):
        if e is None:
            continue
        groups.setdefault(e["trace"] or f"line{i}", []).append(e)
    for evs in groups.values():
        toks = set()
        for e in evs:
            for k in IDENT_KEYS:
                t = norm_ident(e.get(k))
                if t:
                    toks.add(t)
        for e in evs:
            rid = e.get("resource_id")
            if not rid or not RESOURCE_RE.fullmatch(str(rid)):
                continue
            if e.get("event") == "record_lookup":
                idx.observations.append(_ledger_obs(m, e["ts"], e["system"], rid, e["record_type"],
                                                    e["result"], e.get("subject_reference"), "log_ledger"))
                continue
            service = e.get("service", "")
            if service in IGNORED_LOG_SERVICES:
                continue
            st = log_event_state(e)
            if st is None:
                continue
            system = LOG_SERVICE_SYSTEM.get(service, service) or system_for(rid)
            idx.observations.append(Observation(m.file_id, m.captured_at, e["ts"], system, rid, st[0],
                                                frozenset(toks), "log:" + e["event"], st[1]))


# -------------------------------------------------------------------- PDF

PDF_TEXT_CACHE = CACHE_DIR / "pdf_text.json"


def _extract_pdf(path) -> str:
    try:
        import pypdf  # type: ignore
        reader = pypdf.PdfReader(str(path))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except ImportError:
        if not shutil.which("pdftotext"):
            raise RuntimeError("PDF evidence needs `pip install pypdf` (or poppler's pdftotext)")
        return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True,
                              text=True, check=True).stdout


def pdf_text(path) -> str:
    """Extracted text, cached by the PDF's sha256 so every environment parses identically
    (and runs without pypdf/poppler once the committed cache exists)."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    cache = json.loads(PDF_TEXT_CACHE.read_text(encoding="utf-8")) if PDF_TEXT_CACHE.exists() else {}
    if digest not in cache:
        cache[digest] = _extract_pdf(path)
        PDF_TEXT_CACHE.parent.mkdir(parents=True, exist_ok=True)
        PDF_TEXT_CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                                  encoding="utf-8")
    # The generator splits "HH:MM" across a column boundary ("10\n24 UTC" / "10 | 24 UTC").
    return re.sub(r"(\b\d{1,2})\s*(?:\|\s*)?\n?\s*(\d{2}) UTC", r"\1:\2 UTC", cache[digest])


def _parse_pdf(m: ManifestEntry, idx: EvidenceIndex):
    idx.texts[m.file_id] = pdf_text(m.path)
    # Resource-level observations are built by perception.py, which also binds
    # catalog LINK rows; the text is kept here for that step.


PARSERS = {".sql": _parse_sql, ".json": _parse_json, ".txt": _parse_txt, ".log": _parse_log,
           ".pdf": _parse_pdf}


def build_index(manifest: dict[str, ManifestEntry]) -> EvidenceIndex:
    idx = EvidenceIndex()
    for m in manifest.values():
        parser = PARSERS.get(m.path.suffix.lower())
        if parser:
            parser(m, idx)
    return idx
