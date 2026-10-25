"""Business-artifact evidence (screenshots, PDFs) → Observations.

Each artifact is bound to the resource it shows through the data catalog's
LINK_RESOURCE_IDENTITY activity row, which is written a few minutes after the
artifact's capture and names the resource, its system, email and user_id.  The
state shown on the artifact comes from a vision model when one is configured
(cached, see llm.py), otherwise from the artifact's text (PDFs) or a per-type
default.  Vision output is validated against the bound resource ids.
"""
from __future__ import annotations

import re
from datetime import timedelta

from .core import RESOURCE_RE, Activity, ManifestEntry, norm_ident, parse_ts, text_idents
from .evidence import ABSENT, ACTIVE, CLEAN, INACTIVE, PII, EvidenceIndex, Observation, system_for

LINK_RE = re.compile(r"(?:linked|confirmed) (\S+) \(([^)]*)\) (?:belongs only )?to (\S+) and (user_\d+)")
LINK_WINDOW = timedelta(minutes=15)
ARTIFACT_SUFFIXES = {".png", ".jpg", ".jpeg", ".pdf"}
STATES = {ABSENT, PII, CLEAN, ACTIVE, INACTIVE}


def catalog_links(manifest: dict[str, ManifestEntry], activity: list[Activity]) -> dict[str, list[dict]]:
    """file_id -> catalog links written within LINK_WINDOW after that artifact's capture."""
    arts = [m for m in manifest.values() if m.path.suffix.lower() in ARTIFACT_SUFFIXES]
    out: dict[str, list[dict]] = {}
    for a in activity:
        if a.event_type != "LINK_RESOURCE_IDENTITY":
            continue
        mm = LINK_RE.search(a.details)
        if not mm:
            continue
        rid, label, email, user = mm.groups()
        t = a.dt
        best = min(arts, key=lambda m: abs((t - parse_ts(m.captured_at)).total_seconds()))
        lag = t - parse_ts(best.captured_at)
        if timedelta(0) <= lag <= LINK_WINDOW:
            out.setdefault(best.file_id, []).append(
                {"resource_id": rid, "label": label, "system_id": a.target_system,
                 "email": email.lower().rstrip(";."), "user_id": user, "activity_id": a.activity_id})
    return out


def default_state(rid: str, text: str | None) -> str:
    prefix = rid.rsplit("_", 1)[0]
    if prefix in ("audit_record", "legal_hold"):
        return CLEAN
    if prefix in ("data_flow", "backup"):
        return ACTIVE
    if text is not None:
        direct = [t for t in text_idents(text) if not t.startswith("user_")]
        return PII if direct else CLEAN
    return CLEAN if prefix == "tombstone" else PII


def add_artifact_observations(idx: EvidenceIndex, manifest: dict[str, ManifestEntry],
                              activity: list[Activity], vision=None) -> dict[str, dict]:
    """Append artifact observations to ``idx``; returns a per-file perception report."""
    links = catalog_links(manifest, activity)
    report = {}
    for m in manifest.values():
        if m.path.suffix.lower() not in ARTIFACT_SUFFIXES:
            continue
        text = idx.texts.get(m.file_id)
        bound = {l["resource_id"]: l for l in links.get(m.file_id, [])}
        rids = dict(bound)
        if text:
            for rid in RESOURCE_RE.findall(text):
                rids.setdefault(rid, {"resource_id": rid, "system_id": system_for(rid)})
        seen = vision(m, list(rids.values())) if vision else None
        entry = {"bound": sorted(bound), "vision": bool(seen), "resources": {}}
        for rid, link in sorted(rids.items()):
            toks = set(text_idents(text)) if text else set()
            for k in ("email", "user_id"):
                t = norm_ident(link.get(k))
                if t:
                    toks.add(t)
            state, category, how = default_state(rid, text), None, "text" if text else "default"
            if text and m.path.suffix.lower() == ".pdf" and system_for(rid) == "support_platform" \
                    and re.search(r"\b(?:uploader|attachment)\b", text, re.I):
                category = "SUPPORT_ATTACHMENT"
            v = (seen or {}).get(rid)
            if v and v.get("state") in STATES:
                state, how = v["state"], "vision"
                category = v.get("category") or category
                toks |= {t for t in (norm_ident(x) for x in v.get("identifiers", [])) if t}
            idx.observations.append(Observation(
                m.file_id, m.captured_at, m.captured_at, link.get("system_id") or system_for(rid) or "unknown",
                rid, state, frozenset(toks), "artifact:" + how, category,
                (("catalog_link", link.get("activity_id", "")),)))
            entry["resources"][rid] = {"state": state, "how": how, "category": category}
        report[m.file_id] = entry
    return report
