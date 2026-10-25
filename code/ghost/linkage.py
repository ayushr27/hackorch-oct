"""Activity-batch correlation: attach identifier-less deletion-worker resources to cases.

Most account ids, and anonymised analytics records, carry no identifier any more
— the only participant-visible link to a case is the deletion workflow's own
activity: each request's batch runs shortly before its ``reported_at`` and its
follow-up policy actions run at fixed delays after the account submission.

The delays are *calibrated at runtime* from cases whose account and follow-up
resources are both proven by evidence identifiers (no labels are used), then
used as a likelihood to:

1. choose each case's account among the batch candidates (exact max-likelihood
   one-to-one assignment per connected component of competing cases), and
2. attach unowned "Policy action completed" rows (anonymised analytics, legal
   holds, ...) to the case whose account delay matches.

Every inferred link keeps the activity ids that justify it and a confidence.
"""
from __future__ import annotations

import itertools
import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from .core import Activity, parse_ts

STATUS_RESULT = {"COMPLETE": "SUCCESS", "PARTIALLY_COMPLETE": "PARTIAL", "NOT_STARTED": "FAILED"}
WORKER = "deletion_worker"
MAX_CHAIN_SECONDS = 5 * 3600


@dataclass
class CaseLink:
    case_id: str
    user_id: str
    reported_at: str
    reported_status: str
    linked: set              # resource ids evidence-linked to the subject in the discovery window
    owned_any_time: set      # resource ids evidence-linked to the subject at any time
    snapshot_rids: set = field(default_factory=set)   # every resource listed in the case's own captures
    account: str | None = None
    account_activity: str | None = None
    account_how: str = ""
    confidence: float = 0.0
    alternatives: list = field(default_factory=list)
    attached: dict = field(default_factory=dict)   # resource_id -> (activity_id, how)


def generated_batch(reported_at: str) -> bool:
    return reported_at[14:19] == "00:00"


def policy_class(a: Activity, reported_at: str) -> tuple | None:
    """Delay class of a follow-up worker row: fixed-slot policy action, or a failure/check chain row."""
    if a.source_system != WORKER:
        return None
    if a.details.startswith("Policy action completed"):
        minutes = (a.dt - parse_ts(reported_at)).total_seconds() / 60
        return ("POLICY", math.floor((minutes + 30) / 7))
    return ("CHAIN",)


class DelayModel:
    """Histogram of (delay mod 60) per delay class, Laplace-smoothed."""

    def __init__(self):
        self.hist: dict[tuple, Counter] = defaultdict(Counter)

    def add(self, cls, delay: float):
        self.hist[cls][int(delay) % 60] += 1

    def loglik(self, cls, delay: float) -> float:
        if delay < 0 or delay > MAX_CHAIN_SECONDS:
            return -12.0
        h = self.hist.get(cls)
        if not h:
            return 0.0
        n = sum(h.values())
        return math.log((h[int(delay) % 60] + 0.05) / (n + 3.0))

    def fits(self, cls, delay: float) -> bool:
        h = self.hist.get(cls)
        return bool(h) and 0 <= delay <= MAX_CHAIN_SECONDS and h[int(delay) % 60] > 0


class Linker:
    def __init__(self, activity: list[Activity], owner_of: dict[str, str]):
        self.acts = [a for a in activity if a.source_system == WORKER]
        self.by_rid: dict[str, list[Activity]] = defaultdict(list)
        for a in self.acts:
            self.by_rid[a.resource_id].append(a)
        self.account_rows = [a for a in self.acts
                             if a.event_type == "DELETE_RECORD" and a.target_system == "account_service"]
        self.owner_of = owner_of          # resource_id -> user_id, from evidence identifiers
        self.model = DelayModel()

    # ------------------------------------------------------------ candidates
    def account_candidates(self, c: CaseLink) -> list[Activity]:
        rep = parse_ts(c.reported_at)
        if generated_batch(c.reported_at):
            lo, hi, result = -120 * 60, 15 * 60, STATUS_RESULT.get(c.reported_status)
        else:
            lo, hi, result = -10 * 60, 10 * 60, None
        out = []
        for a in self.account_rows:
            d = (a.dt - rep).total_seconds()
            if lo <= d <= hi and (result is None or a.reported_result == result):
                out.append(a)
        return out

    def follow_ups(self, account_row: Activity, rids) -> list[Activity]:
        out = []
        for rid in rids:
            for a in self.by_rid.get(rid, []):
                if a is not account_row and 0 <= (a.dt - account_row.dt).total_seconds() <= MAX_CHAIN_SECONDS:
                    out.append(a)
        return out

    def score(self, c: CaseLink, a: Activity) -> float:
        # weak prior: the candidate also appears (identifier-less) in the case's own captures
        s = 0.5 if a.resource_id in c.snapshot_rids else 0.0
        for f in self.follow_ups(a, c.linked - {a.resource_id}):
            cls = policy_class(f, c.reported_at)
            if cls:
                s += self.model.loglik(cls, (f.dt - a.dt).total_seconds())
        return s

    # ------------------------------------------------------------------ solve
    def solve(self, cases: list[CaseLink]):
        # 1. Accounts fixed by evidence: a batch row owned by the subject, else an
        #    evidence-linked account in the discovery window.
        claimed: set[str] = set()
        for c in cases:
            cands = self.account_candidates(c)
            own = [a for a in cands if self.owner_of.get(a.resource_id) == c.user_id]
            if not own:
                own = [a for a in self.account_rows if a.resource_id in c.linked]
            if own:
                a = own[0]
                c.account, c.account_activity, c.account_how, c.confidence = \
                    a.resource_id, a.activity_id, "evidence", 1.0
            else:
                linked_acc = sorted(r for r in c.linked if r.startswith("account_"))
                if linked_acc:
                    c.account, c.account_how, c.confidence = linked_acc[0], "evidence", 1.0
            if c.account:
                claimed.add(c.account)

        # 2. Calibrate the delay model on evidence-anchored follow-ups.
        for c in cases:
            if c.account_activity:
                a = next(x for x in self.acts if x.activity_id == c.account_activity)
                for f in self.follow_ups(a, c.linked - {a.resource_id}):
                    cls = policy_class(f, c.reported_at)
                    if cls:
                        self.model.add(cls, (f.dt - a.dt).total_seconds())

        # 3. Assign the rest: exact max-likelihood matching per component.
        open_cases = [c for c in cases if not c.account]
        cand: dict[str, list[Activity]] = {}
        for c in open_cases:
            cand[c.case_id] = [a for a in self.account_candidates(c)
                               if a.resource_id not in claimed and a.resource_id not in self.owner_of]
        for comp in _components(open_cases, cand):
            self._assign_component(comp, cand)

        # 4. Attach unowned policy rows (anonymised analytics, legal holds, ...).
        self._attach_unowned(cases)
        self._attach_off_grid(cases)

    def _attach_off_grid(self, cases: list[CaseLink]):
        """Hand-run (off-grid) requests: the worker's own completion rows just before
        reported_at belong to that request when no other off-grid request is that close."""
        off = [c for c in cases if not generated_batch(c.reported_at)]
        for a in self.acts:
            if a.target_system == "account_service" or a.resource_id in self.owner_of:
                continue
            near = [c for c in off if -15 * 60 <= (a.dt - parse_ts(c.reported_at)).total_seconds() <= 5 * 60]
            if len(near) == 1 and a.reported_result != "FAILED":
                near[0].attached.setdefault(a.resource_id, (a.activity_id, "off-grid worker row"))

    def _assign_component(self, comp: list[CaseLink], cand: dict):
        comp = sorted(comp, key=lambda c: c.case_id)
        scores = {(c.case_id, a.activity_id): self.score(c, a) for c in comp for a in cand[c.case_id]}
        best, best_val, second_val = None, -math.inf, -math.inf
        options = [cand[c.case_id] + [None] for c in comp]
        if math.prod(len(o) for o in options) > 200000:
            options = [sorted(cand[c.case_id], key=lambda a: -scores[(c.case_id, a.activity_id)])[:4] + [None]
                       for c in comp]
        for combo in itertools.product(*options):
            picked = [a.activity_id for a in combo if a]
            if len(picked) != len(set(picked)):
                continue
            # every case that has a candidate should get one: unassigned costs a lot
            val = sum(scores[(c.case_id, a.activity_id)] if a else -50.0 for c, a in zip(comp, combo))
            if val > best_val + 1e-9:
                best, second_val, best_val = combo, best_val, val
            elif val > second_val:
                second_val = val
        if best is None:
            return
        margin = best_val - second_val
        for c, a in zip(comp, best):
            if a is None:
                continue
            c.account, c.account_activity = a.resource_id, a.activity_id
            c.alternatives = [x.resource_id for x in cand[c.case_id] if x is not a]
            if len(cand[c.case_id]) == 1 and len(comp) == 1:
                c.account_how, c.confidence = "batch-unique", 0.95
            else:
                c.account_how = "batch-delay-match"
                c.confidence = round(1 - math.exp(-max(margin, 0.0)), 3) if math.isfinite(margin) else 0.95

    def _attach_unowned(self, cases: list[CaseLink]):
        by_rep: dict[str, list[CaseLink]] = defaultdict(list)
        for c in cases:
            if c.account_activity:
                by_rep[c.reported_at].append(c)
        acc_row = {a.activity_id: a for a in self.account_rows}
        for a in self.acts:
            if not a.details.startswith("Policy action completed"):
                continue
            if a.resource_id in self.owner_of or a.target_system == "account_service":
                continue
            best, best_ll, n_fit = None, -math.inf, 0
            for rep, group in by_rep.items():
                if not (0 <= (parse_ts(rep) - a.dt).total_seconds() <= 3600):
                    continue
                for c in group:
                    acc = acc_row[c.account_activity]
                    d = (a.dt - acc.dt).total_seconds()
                    cls = policy_class(a, c.reported_at)
                    if self.model.fits(cls, d):
                        n_fit += 1
                        ll = self.model.loglik(cls, d)
                        if ll > best_ll:
                            best, best_ll = c, ll
            if best is not None:
                how = "policy-delay-match" if n_fit == 1 else f"policy-delay-match({n_fit} fits)"
                best.attached[a.resource_id] = (a.activity_id, how)


def _components(cases: list[CaseLink], cand: dict) -> list[list[CaseLink]]:
    by_act: dict[str, list[CaseLink]] = defaultdict(list)
    for c in cases:
        for a in cand[c.case_id]:
            by_act[a.activity_id].append(c)
    parent = {c.case_id: c.case_id for c in cases}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for group in by_act.values():
        for c in group[1:]:
            parent[find(c.case_id)] = find(group[0].case_id)
    comps: dict[str, list[CaseLink]] = defaultdict(list)
    for c in cases:
        if cand[c.case_id]:
            comps[find(c.case_id)].append(c)
    return list(comps.values())
