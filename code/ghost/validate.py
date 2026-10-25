"""Contract validator for output.csv (AGENTS.md §6.3–6.6)."""
from __future__ import annotations

import csv
import json

from .audit import OP_RANK, OP_STATE, PHASE_RANK
from .core import DATASET, load_manifest, load_requests, read_csv

PHASE_OPS = {
    "FINDING": {"REPORT_REMAINING_RECORD", "REPORT_EXPOSED_PII", "REPORT_ACTIVE_DATA_FLOW", "REPORT_RESTORE_RISK"},
    "REMEDIATION": {"DISABLE_DATA_FLOW", "BLOCK_RESTORE", "DELETE_RECORD", "REDACT_RECORD", "ANONYMIZE_RECORD"},
    "VERIFICATION": {"VERIFY_RECORD_ABSENT", "VERIFY_RECORD_PRESENT", "VERIFY_RECORD_REDACTED",
                     "VERIFY_RECORD_ANONYMIZED", "VERIFY_DATA_FLOW_DISABLED", "VERIFY_RESTORE_BLOCKED"},
}
STEP_KEYS = {"step_no", "phase", "system_id", "resource_id", "operation", "state", "evidence_id"}


def validate(output_path, requests_path=None) -> list[str]:
    requests_path = requests_path or DATASET / "deletion_requests.csv"
    reqs = {r.case_id: r for r in load_requests(requests_path)}
    files = {m.file_id: m.captured_at for m in load_manifest().values()}
    acts = {r["activity_id"]: r["event_time"] for r in read_csv(DATASET / "system_activity.csv")}
    audits = {r["audit_id"]: r["event_time"] for r in read_csv(DATASET / "user_audit_log.csv")}
    errors = []
    with open(output_path, encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows or rows[0] != ["case_id", "deletion_status", "steps_json"]:
        return ["bad header"]
    seen = []
    for case_id, status, steps_json in rows[1:]:
        seen.append(case_id)
        e = lambda msg: errors.append(f"{case_id}: {msg}")
        if case_id not in reqs:
            e("unknown case_id")
            continue
        if status not in ("COMPLETE", "INCOMPLETE", "NOT_APPLICABLE"):
            e(f"bad status {status}")
        try:
            steps = json.loads(steps_json)
        except json.JSONDecodeError:
            e("steps_json is not JSON")
            continue
        if not isinstance(steps, list):
            e("steps_json is not an array")
            continue
        if status == "NOT_APPLICABLE" and steps:
            e("NOT_APPLICABLE must have []")
        if status == "COMPLETE" and any(s.get("phase") != "VERIFICATION" for s in steps):
            e("COMPLETE may only contain verification steps")
        if status == "INCOMPLETE" and not any(s.get("phase") == "FINDING" for s in steps):
            e("INCOMPLETE without findings")
        prev = None
        for i, s in enumerate(steps, 1):
            if set(s) != STEP_KEYS:
                e(f"step {i}: keys {sorted(s)}")
                continue
            if s["step_no"] != i:
                e(f"step {i}: step_no {s['step_no']}")
            if s["operation"] not in PHASE_OPS.get(s["phase"], ()):
                e(f"step {i}: {s['operation']} not allowed in {s['phase']}")
            elif s["state"] != OP_STATE[s["operation"]]:
                e(f"step {i}: state {s['state']} for {s['operation']}")
            key = (PHASE_RANK.get(s["phase"], 9), OP_RANK.get(s["operation"], 9), s["system_id"], s["resource_id"])
            if prev and key < prev:
                e(f"step {i}: out of order")
            prev = key
            ev, audit_at = s["evidence_id"], reqs[case_id].audit_at
            cited = s["phase"] == "FINDING" or status == "COMPLETE"
            if cited:
                t = files.get(ev) or acts.get(ev) or audits.get(ev)
                if not t:
                    e(f"step {i}: evidence '{ev}' does not exist")
                elif t > audit_at and ev in files:
                    e(f"step {i}: evidence {ev} captured after audit_at")
            elif ev:
                e(f"step {i}: future-work step must have empty evidence_id")
    missing = set(reqs) - set(seen)
    if missing:
        errors.append(f"missing {len(missing)} case(s), e.g. {sorted(missing)[:3]}")
    if len(seen) != len(set(seen)):
        errors.append("duplicate case_id rows")
    return errors
