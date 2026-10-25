"""Point-in-time state reconstruction, policy application and step planning for one case.

Time rules (two tiers):
* discovery — a resource belongs to the case when an observation whose own time is
  within [requested_at, audit_at] carries one of the subject's identifiers (any file,
  even one captured later), or when activity correlation attaches it;
* state & citation — only observations from files captured at or before audit_at
  with record time at or before audit_at; the latest one wins. Later files never
  change the answer and are never cited.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .evidence import (ABSENT, ACTIVE, CLEAN, INACTIVE, PII, Observation, Scope,
                       resource_prefix, system_for)

# ------------------------------------------------------------------ policy

DELETE, REDACT, ANONYMIZE, DISABLE, BLOCK, RETAIN = \
    "DELETE", "REDACT", "ANONYMIZE", "DISABLE", "BLOCK", "RETAIN"

CATEGORY_ACTION = {
    "USER_PROFILE": DELETE, "SECONDARY_IDENTIFIER": DELETE, "SEARCH_INDEX_ENTRY": DELETE,
    "CACHE_ENTRY": DELETE, "SUPPORT_MESSAGE": REDACT, "SUPPORT_ATTACHMENT": DELETE,
    "ANALYTICS_PROFILE": ANONYMIZE, "PRODUCT_TELEMETRY": ANONYMIZE, "USER_EXPORT": DELETE,
    "MARKETING_PROFILE": DELETE, "EMAIL_DELIVERY_LOG": REDACT, "SECURITY_AUDIT_LOG": RETAIN,
    "LEGAL_HOLD_RECORD": RETAIN, "BACKUP_ARCHIVE": BLOCK, "ACCOUNT_TOMBSTONE": REDACT,
    "DATA_FLOW": DISABLE,
}

PREFIX_CATEGORY = {
    "account": "USER_PROFILE", "search": "SEARCH_INDEX_ENTRY", "export": "USER_EXPORT",
    "analytics": "ANALYTICS_PROFILE", "support": "SUPPORT_MESSAGE", "tombstone": "ACCOUNT_TOMBSTONE",
    "data_flow": "DATA_FLOW", "backup": "BACKUP_ARCHIVE", "audit_record": "SECURITY_AUDIT_LOG",
    "legal_hold": "LEGAL_HOLD_RECORD", "marketing": "MARKETING_PROFILE",
    "object": "SUPPORT_ATTACHMENT", "telemetry": "PRODUCT_TELEMETRY", "cache": "CACHE_ENTRY",
    "email_delivery": "EMAIL_DELIVERY_LOG",
}

# The workflow's own attempted operation is corroborating evidence of the category
# when no source states it explicitly (e.g. a support copy the worker tried to delete).
WORKER_OP_CATEGORY = {
    ("support", "DELETE_RECORD"): "SUPPORT_ATTACHMENT", ("support", "REDACT_RECORD"): "SUPPORT_MESSAGE",
    ("analytics", "DELETE_RECORD"): "MARKETING_PROFILE", ("analytics", "ANONYMIZE_RECORD"): "ANALYTICS_PROFILE",
}

OP_RANK = {
    "REPORT_REMAINING_RECORD": 0, "REPORT_EXPOSED_PII": 1, "REPORT_ACTIVE_DATA_FLOW": 2,
    "REPORT_RESTORE_RISK": 3,
    "DISABLE_DATA_FLOW": 0, "BLOCK_RESTORE": 1, "DELETE_RECORD": 2, "REDACT_RECORD": 3,
    "ANONYMIZE_RECORD": 4,
    "VERIFY_RECORD_ABSENT": 0, "VERIFY_RECORD_PRESENT": 1, "VERIFY_RECORD_REDACTED": 2,
    "VERIFY_RECORD_ANONYMIZED": 3, "VERIFY_DATA_FLOW_DISABLED": 4, "VERIFY_RESTORE_BLOCKED": 5,
}
PHASE_RANK = {"FINDING": 0, "REMEDIATION": 1, "VERIFICATION": 2}
OP_STATE = {
    "REPORT_REMAINING_RECORD": "PRESENT", "REPORT_EXPOSED_PII": "PRESENT",
    "REPORT_ACTIVE_DATA_FLOW": "ACTIVE", "REPORT_RESTORE_RISK": "ACTIVE",
    "DISABLE_DATA_FLOW": "DISABLED", "BLOCK_RESTORE": "BLOCKED", "DELETE_RECORD": "ABSENT",
    "REDACT_RECORD": "REDACTED", "ANONYMIZE_RECORD": "ANONYMIZED",
    "VERIFY_RECORD_ABSENT": "ABSENT", "VERIFY_RECORD_PRESENT": "PRESENT",
    "VERIFY_RECORD_REDACTED": "REDACTED", "VERIFY_RECORD_ANONYMIZED": "ANONYMIZED",
    "VERIFY_DATA_FLOW_DISABLED": "DISABLED", "VERIFY_RESTORE_BLOCKED": "BLOCKED",
}
# action -> (finding op, remediation op, final verification op)
ACTION_OPS = {
    DELETE: ("REPORT_REMAINING_RECORD", "DELETE_RECORD", "VERIFY_RECORD_ABSENT"),
    REDACT: ("REPORT_EXPOSED_PII", "REDACT_RECORD", "VERIFY_RECORD_REDACTED"),
    ANONYMIZE: ("REPORT_EXPOSED_PII", "ANONYMIZE_RECORD", "VERIFY_RECORD_ANONYMIZED"),
    DISABLE: ("REPORT_ACTIVE_DATA_FLOW", "DISABLE_DATA_FLOW", "VERIFY_DATA_FLOW_DISABLED"),
    BLOCK: ("REPORT_RESTORE_RISK", "BLOCK_RESTORE", "VERIFY_RESTORE_BLOCKED"),
    RETAIN: (None, None, "VERIFY_RECORD_PRESENT"),
}


def violates(action: str, state: str) -> bool:
    if action == DELETE:
        return state in (PII, CLEAN)
    if action in (REDACT, ANONYMIZE):
        return state == PII
    if action in (DISABLE, BLOCK):
        return state == ACTIVE
    return False


# ------------------------------------------------------------- per-case model

@dataclass
class ResourceView:
    resource_id: str
    system_id: str
    category: str
    action: str
    state: str | None = None
    proof: str = ""                 # evidence id proving `state` (citable at audit_at)
    proof_time: str = ""
    how_linked: str = ""
    notes: list = field(default_factory=list)

    @property
    def violation(self) -> bool:
        return self.state is not None and violates(self.action, self.state)


@dataclass
class CaseResult:
    case_id: str
    status: str
    steps: list
    resources: list = field(default_factory=list)
    trace: list = field(default_factory=list)


def latest(obs: list[Observation]) -> Observation | None:
    return max(obs, key=lambda o: (o.rec_time, o.file_time, o.file_id)) if obs else None


def resolve_state(rid: str, obs: list[Observation], scopes: list[Scope], audit_at: str,
                  own_files: set[str], retained: bool) -> tuple[str | None, str, str, list]:
    """(state, proof evidence id, proof time, notes) for one resource at audit_at."""
    notes = []
    citable = [o for o in obs if o.file_time <= audit_at and o.rec_time <= audit_at]
    best = latest(citable)
    cand = [] if best is None else [(best.rec_time, best.file_time, best.file_id, best.state)]
    if not retained:
        # Absence by omission: a capture that covered the resource's system (and is
        # trusted for this subject) but did not list the resource.
        for s in scopes:
            if s.file_time <= audit_at and s.rec_time <= audit_at and rid not in s.listed \
                    and s.file_id in own_files:
                cand.append((s.rec_time, s.file_time, s.file_id, ABSENT))
    if cand:
        rec_time, _, fid, state = max(cand)
        if best is not None and fid != best.file_id:
            notes.append(f"scope of {fid} supersedes {best.file_id}")
        return state, fid, rec_time, notes
    later = [o for o in obs if o.rec_time <= audit_at]
    if later:
        o = latest(later)
        notes.append(f"state from {o.file_id} (captured after audit_at; not citable)")
        return o.state, "", o.rec_time, notes
    return None, "", "", notes


def absence_proof(system: str, scopes: list[Scope], audit_at: str, own_files: set[str],
                  rid: str) -> tuple[str, str]:
    """Evidence id proving a never-observed resource absent: the case's own snapshot
    covering the system, else the latest non-empty dump of that store."""
    own = [s for s in scopes if s.system_id == system and s.file_id in own_files
           and s.file_time <= audit_at and rid not in s.listed]
    if own:
        s = max(own, key=lambda s: (s.rec_time, s.file_time))
        return s.file_id, s.rec_time
    dumps = [s for s in scopes if s.system_id == system and s.listed and s.file_time <= audit_at
             and rid not in s.listed]
    if dumps:
        s = max(dumps, key=lambda s: (s.rec_time, s.file_time))
        return s.file_id, s.rec_time
    return "", ""


def step(phase, system_id, resource_id, operation, evidence_id=""):
    return {"step_no": 0, "phase": phase, "system_id": system_id, "resource_id": resource_id,
            "operation": operation, "state": OP_STATE[operation], "evidence_id": evidence_id}


def order_steps(steps: list[dict]) -> list[dict]:
    steps = sorted(steps, key=lambda s: (PHASE_RANK[s["phase"]], OP_RANK[s["operation"]],
                                         s["system_id"], s["resource_id"]))
    for i, s in enumerate(steps, 1):
        s["step_no"] = i
    return steps


def plan(views: list[ResourceView]) -> tuple[str, list[dict]]:
    """Status + ordered steps from the resolved resource views."""
    violations = [v for v in views if v.violation]
    steps = []
    if not violations:
        for v in views:
            if v.state is None:
                continue
            op = ACTION_OPS[v.action][2]
            if v.action == DELETE or v.state == ABSENT:
                op = "VERIFY_RECORD_ABSENT"
            if not v.proof:
                continue
            steps.append(step("VERIFICATION", v.system_id, v.resource_id, op, v.proof))
        return "COMPLETE", order_steps(steps)
    for v in views:
        f_op, r_op, v_op = ACTION_OPS[v.action]
        if v.violation:
            steps.append(step("FINDING", v.system_id, v.resource_id, f_op, v.proof))
            steps.append(step("REMEDIATION", v.system_id, v.resource_id, r_op))
            steps.append(step("VERIFICATION", v.system_id, v.resource_id, v_op))
        elif v.state is not None:
            op = "VERIFY_RECORD_ABSENT" if (v.action == DELETE or v.state == ABSENT) else v_op
            steps.append(step("VERIFICATION", v.system_id, v.resource_id, op))
    return "INCOMPLETE", order_steps(steps)


def category_of(rid: str, obs: list[Observation], worker_ops: list[str], audit_at: str) -> tuple[str, str]:
    """(category, reason) — explicit source category first, then the worker's attempted op."""
    explicit = [o for o in obs if o.category and o.rec_time <= audit_at]
    if explicit:
        o = latest(explicit)
        return o.category, f"stated by {o.file_id}"
    prefix = resource_prefix(rid)
    for op in reversed(worker_ops):
        cat = WORKER_OP_CATEGORY.get((prefix, op))
        if cat:
            return cat, f"implied by worker {op}"
    return PREFIX_CATEGORY.get(prefix, "USER_PROFILE"), "resource type default"


def build_view(rid: str, obs: list[Observation], scopes: list[Scope], worker_ops: list[str],
               audit_at: str, own_files: set[str], how: str) -> ResourceView:
    system = (latest(obs).system_id if obs else None) or system_for(rid) or "unknown"
    category, why = category_of(rid, obs, worker_ops, audit_at)
    action = CATEGORY_ACTION.get(category, DELETE)
    v = ResourceView(rid, system, category, action, how_linked=how, notes=[f"category {category}: {why}"])
    sys_scopes = [s for s in scopes if s.system_id == system]
    v.state, v.proof, v.proof_time, notes = resolve_state(
        rid, obs, sys_scopes, audit_at, own_files, retained=(action == RETAIN))
    v.notes += notes
    if v.state is None and action == DELETE:
        v.proof, v.proof_time = absence_proof(system, scopes, audit_at, own_files, rid)
        v.state = ABSENT
        v.notes.append(f"never observed; absence proven by {v.proof or 'nothing citable'}")
    if action == RETAIN and v.state in (None, ABSENT):
        # A retained record's absence from one snapshot is not evidence it is gone; a
        # record the workflow successfully retained for this case must stay present.
        if any(o.rec_time <= audit_at for o in obs) or "RETAIN_RECORD" in worker_ops:
            v.state = CLEAN
    return v
