"""Paths, time helpers, identifier normalisation, CSV loaders and identity resolution."""
from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "dataset"
CODE = ROOT / "code"
CACHE_DIR = CODE / "cache"


# ---------------------------------------------------------------- time

def parse_ts(s: str) -> datetime:
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm_ts(s: str) -> str:
    """Canonical 'YYYY-MM-DDTHH:MM:SSZ' so timestamps compare as strings."""
    return iso(parse_ts(s))


# ------------------------------------------------- identifier tokens

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
HASH_RE = re.compile(r"\b[0-9a-fA-F]{64}\b")
USER_RE = re.compile(r"\buser_\d+\b")
PHONE_RE = re.compile(r"\+\d[\d ().-]{6,}\d")
RESOURCE_RE = re.compile(
    r"\b(?:account|search|analytics|support|export|data_flow|backup|audit_record|"
    r"tombstone|legal_hold|marketing|object|telemetry|cache|email_delivery)_\d+\b"
)


def phone_token(value: str) -> str | None:
    digits = re.sub(r"\D", "", value)
    return "tel:" + digits if len(digits) >= 8 else None


def norm_ident(value) -> str | None:
    """Normalise one field value into an identifier token, or None if it is not one."""
    if value is None:
        return None
    v = str(value).strip()
    if not v or v.lower() in ("null", "none", "-", "—"):
        return None
    if EMAIL_RE.fullmatch(v):
        return v.lower()
    if HASH_RE.fullmatch(v):
        return v.lower()
    if USER_RE.fullmatch(v):
        return v.lower()
    if v.startswith("+") and PHONE_RE.fullmatch(v):
        return phone_token(v)
    return None


def text_idents(text: str) -> set[str]:
    """All identifier tokens embedded in free text."""
    if not text:
        return set()
    out = {m.lower() for m in EMAIL_RE.findall(text)}
    out |= {m.lower() for m in HASH_RE.findall(text)}
    out |= {m.lower() for m in USER_RE.findall(text)}
    for m in PHONE_RE.findall(text):
        t = phone_token(m)
        if t:
            out.add(t)
    return out


def email_hash(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


# ------------------------------------------------------------- loaders

def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


@dataclass
class Request:
    case_id: str
    email: str
    requested_at: str
    reported_status: str
    reported_at: str
    audit_at: str
    request_text: str


def load_requests(path: Path) -> list[Request]:
    out = []
    for r in read_csv(path):
        out.append(Request(
            case_id=r["case_id"], email=r["email"].strip(),
            requested_at=norm_ts(r["requested_at"]), reported_status=r["reported_status"].strip(),
            reported_at=norm_ts(r["reported_at"]), audit_at=norm_ts(r["audit_at"]),
            request_text=r["request_text"],
        ))
    return out


@dataclass
class Activity:
    activity_id: str
    event_time: str
    event_type: str
    source_system: str
    target_system: str
    resource_id: str
    reported_result: str
    details: str

    @property
    def dt(self) -> datetime:
        return parse_ts(self.event_time)


def load_activity() -> list[Activity]:
    acts = [Activity(**{**r, "event_time": norm_ts(r["event_time"])})
            for r in read_csv(DATASET / "system_activity.csv")]
    acts.sort(key=lambda a: (a.event_time, int(a.activity_id.split("_")[1])))
    return acts


@dataclass
class ManifestEntry:
    file_id: str
    path: Path
    origin: str
    captured_at: str


def load_manifest() -> dict[str, ManifestEntry]:
    out = {}
    for r in read_csv(DATASET / "evidence_files.csv"):
        out[r["file_id"]] = ManifestEntry(r["file_id"], DATASET / r["file_path"], r["origin"],
                                          norm_ts(r["captured_at"]))
    return out


def load_rules() -> dict[str, dict]:
    return {r["data_category"]: r for r in read_csv(DATASET / "deletion_rules.csv")}


# ------------------------------------------------------------ identity

@dataclass
class Subject:
    user_id: str
    name: str
    current_email: str
    emails: set[str] = field(default_factory=set)
    hashes: set[str] = field(default_factory=set)
    phones: set[str] = field(default_factory=set)
    audit_ids: list[str] = field(default_factory=list)

    @property
    def keys(self) -> set[str]:
        return {self.user_id.lower()} | self.emails | self.hashes | self.phones


class IdentityIndex:
    """Current snapshot + full audit history → one key set per user (multi-hop safe)."""

    def __init__(self):
        self.subjects: dict[str, Subject] = {}
        for r in read_csv(DATASET / "user_identities.csv"):
            s = Subject(r["user_id"], r["name"], r["email"].lower())
            s.emails.add(r["email"].lower())
            s.hashes.add(r["email_hash"].lower())
            t = phone_token(r["phone"])
            if t:
                s.phones.add(t)
            self.subjects[r["user_id"]] = s
        for r in read_csv(DATASET / "user_audit_log.csv"):
            s = self.subjects.get(r["user_id"])
            if s is None:
                continue
            s.audit_ids.append(r["audit_id"])
            for v in (r["old_value"], r["new_value"]):
                if not v:
                    continue
                if r["field_name"] == "email":
                    s.emails.add(v.strip().lower())
                elif r["field_name"] == "email_hash":
                    s.hashes.add(v.strip().lower())
                elif r["field_name"] == "phone":
                    t = phone_token(v)
                    if t:
                        s.phones.add(t)
        for s in self.subjects.values():
            s.hashes |= {email_hash(e) for e in s.emails}
        self.by_key: dict[str, str] = {}
        for uid, s in self.subjects.items():
            for k in s.keys:
                self.by_key.setdefault(k, uid)

    def resolve(self, email: str) -> Subject | None:
        uid = self.by_key.get(email.strip().lower())
        return self.subjects.get(uid) if uid else None

    def owner(self, token: str) -> str | None:
        return self.by_key.get(token)
