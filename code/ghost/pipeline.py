"""End-to-end orchestration: load → perceive → link → audit each case → serialise."""
from __future__ import annotations

import csv
import io
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field

from . import intent as intent_mod
from .audit import CaseResult, build_view, plan
from .core import (DATASET, IdentityIndex, Request, load_activity, load_manifest, load_requests)
from .evidence import build_index
from .linkage import CaseLink, Linker
from .perception import add_artifact_observations

FIELDS = ("case_id", "deletion_status", "steps_json")


@dataclass
class CaseContext:
    request: Request
    user_id: str | None
    intent: str
    intent_reason: str
    link: CaseLink | None = None
    notes: list = field(default_factory=list)


class Engine:
    def __init__(self, vision=None, intent_classifier=None):
        self.manifest = load_manifest()
        self.idx = build_index(self.manifest)
        self.activity = load_activity()
        self.perception = add_artifact_observations(self.idx, self.manifest, self.activity, vision)
        self.ids = IdentityIndex()
        self.intent_classifier = intent_classifier

        owners: dict[str, set] = defaultdict(set)
        self.obs_by_rid = defaultdict(list)
        for o in self.idx.observations:
            self.obs_by_rid[o.resource_id].append(o)
            for t in o.idents:
                u = self.ids.owner(t)
                if u:
                    owners[o.resource_id].add(u)
        self.owner_of = {rid: next(iter(us)) for rid, us in owners.items() if len(us) == 1}
        self.worker_ops = defaultdict(list)
        for a in self.activity:
            if a.source_system == "deletion_worker":
                self.worker_ops[a.resource_id].append(a.event_type)
        # privacy intake's own non-deletion classifications, keyed by account owner
        self.intake_non_deletion = defaultdict(list)
        for a in self.activity:
            if a.event_type == "CLASSIFY_REQUEST" and "non-deletion" in a.details:
                u = self.owner_of.get(a.resource_id)
                if u:
                    self.intake_non_deletion[u].append(a)
        self.contexts: dict[str, CaseContext] = {}

    # ------------------------------------------------------------ discovery
    def linked_observations(self, req: Request, keys: set[str]):
        return [o for o in self.idx.observations
                if o.idents & keys and req.requested_at <= o.rec_time <= req.audit_at]

    # -------------------------------------------------------------- prepare
    def prepare(self, requests: list[Request]):
        """Intent + identity + cross-case activity linkage for every request at once."""
        texts = [r.request_text for r in requests]
        llm_labels = self.intent_classifier(texts) if self.intent_classifier else {}
        links = []
        for r in requests:
            subj = self.ids.resolve(r.email)
            label, reason = intent_mod.rule_intent(r.request_text)
            llm = llm_labels.get(r.request_text)
            if llm and llm != label:
                # Explicit language found by the rules (retention wording or a deletion verb)
                # wins; the model decides only requests the rules have no signal for. On the
                # public samples the model misread a deletion with a retention caveat (case_19).
                if reason == "no deletion language":
                    label, reason = llm, f"LLM classifier (rules found no explicit signal)"
                else:
                    reason += f" (LLM said {llm}; explicit rule signal kept)"
            elif llm:
                reason += " (LLM agrees)"
            ctx = CaseContext(r, subj.user_id if subj else None, label, reason)
            if subj and self.intake_non_deletion.get(subj.user_id):
                ids = [a.activity_id for a in self.intake_non_deletion[subj.user_id]
                       if r.requested_at <= a.event_time]
                if ids:
                    ctx.notes.append(f"privacy intake classified non-deletion: {', '.join(ids)}")
            self.contexts[r.case_id] = ctx
            if subj is None or label != intent_mod.DELETE:
                continue
            obs = self.linked_observations(r, subj.keys)
            linked = {o.resource_id for o in obs}
            own_files = {o.file_id for o in obs}
            snapshot = {o.resource_id for o in self.idx.observations if o.file_id in own_files}
            any_time = {rid for rid, u in self.owner_of.items() if u == subj.user_id}
            ctx.link = CaseLink(r.case_id, subj.user_id, r.reported_at, r.reported_status, linked, any_time,
                                snapshot)
            links.append(ctx.link)
        Linker(self.activity, self.owner_of).solve(links)
        # Cases with no batch account: an account linked to the subject at any time and
        # not used by another person's case; failing that, the account service's
        # `account_<user number>` reference when no one else owns that id (low confidence).
        used_by = {l.account: l.user_id for l in links if l.account}
        activity_ids = {a.resource_id for a in self.activity}
        for l in links:
            if l.account:
                continue
            same_user = {acc for acc, u in used_by.items() if u == l.user_id}
            own = sorted(r for r in l.owned_any_time | same_user
                         if r.startswith("account_") and used_by.get(r, l.user_id) == l.user_id)
            if own:
                l.account, l.account_how, l.confidence = own[-1], "subject-linked (outside window)", 0.6
            else:
                guess = "account_%03d" % int(l.user_id.split("_")[1])
                if guess not in self.owner_of and guess not in used_by and guess not in activity_ids:
                    l.account, l.account_how, l.confidence = guess, "naming-convention fallback", 0.2
            if l.account:
                used_by[l.account] = l.user_id

    # ---------------------------------------------------------------- audit
    def audit(self, req: Request) -> CaseResult:
        ctx = self.contexts[req.case_id]
        trace = [f"intent: {ctx.intent} — {ctx.intent_reason}"] + ctx.notes
        if ctx.user_id is None:
            trace.append("request email does not resolve to any known identity")
        if ctx.intent != intent_mod.DELETE or ctx.link is None:
            return CaseResult(req.case_id, "NOT_APPLICABLE", [], [], trace)
        subj = self.ids.subjects[ctx.user_id]
        link = ctx.link
        trace.append(f"subject {subj.user_id}: {len(subj.emails)} email(s), {len(subj.hashes)} hash(es), "
                     f"{len(subj.phones)} phone(s)")
        linked = self.linked_observations(req, subj.keys)
        own_files = {o.file_id for o in linked if o.file_time <= req.audit_at}
        how = {o.resource_id: f"identifier match in {o.file_id}" for o in linked}
        rids = {r for r in how if not r.startswith("account_")}
        if link.account:
            rids.add(link.account)
            how[link.account] = f"{link.account_how} ({link.account_activity or 'evidence'}, " \
                                f"confidence {link.confidence})"
            if link.alternatives:
                how[link.account] += f"; alternatives {link.alternatives}"
        else:
            trace.append("no account resource could be linked")
        for rid, (act, why) in link.attached.items():
            if rid not in rids:
                rids.add(rid)
                how[rid] = f"{why} via {act}"
        views = [build_view(rid, self.obs_by_rid.get(rid, []), self.idx.scopes, self.worker_ops.get(rid, []),
                            req.audit_at, own_files, how.get(rid, "")) for rid in sorted(rids)]
        status, steps = plan(views)
        for v in views:
            trace.append(f"{v.system_id}/{v.resource_id}: {v.category} → {v.action}; state {v.state} "
                         f"(proof {v.proof or '-'}); linked by {v.how_linked}; " + "; ".join(v.notes))
        return CaseResult(req.case_id, status, steps, views, trace)

    def run(self, requests: list[Request]) -> list[CaseResult]:
        self.prepare(requests)
        return [self.audit(r) for r in requests]


def case_sort_key(case_id: str):
    m = re.search(r"(\d+)$", case_id)
    return (int(m.group(1)) if m else 0, case_id)


def serialise(results: list[CaseResult]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(FIELDS)
    for r in sorted(results, key=lambda r: case_sort_key(r.case_id)):
        w.writerow([r.case_id, r.status,
                    json.dumps(r.steps, separators=(",", ":"), ensure_ascii=False)])
    return buf.getvalue()


def run_all(eval_path=None, extra_paths=(), **engine_kw):
    """Audit the evaluation requests (plus any extra request files, e.g. samples, which
    share the global activity batches and so improve cross-case linkage)."""
    eval_path = eval_path or DATASET / "deletion_requests.csv"
    main_reqs = load_requests(eval_path)
    extra = [r for p in extra_paths for r in load_requests(p)]
    eng = Engine(**engine_kw)
    eng.prepare(main_reqs + extra)
    results = {r.case_id: eng.audit(r) for r in main_reqs + extra}
    return eng, main_reqs, extra, results
