# Evaluation report — Ghost Data Still Exists

_Generated 2026-10-25 10:00 UTC by `python3 code/evaluation/main.py`._

## 1. Public sample set (32 cases with published answers)

The engine is run exactly as for the submission (samples and evaluation requests are prepared together because they share the global activity batches); answers are compared with `dataset/sample_output.csv`. Gold labels are used **only** here, never for predictions.

| Metric | Value |
|---|---|
| Case-level deletion-status accuracy | 100.0% (32/32) |
| Step-level precision (all 6 step fields must match) | 100.0% |
| Step-level recall | 99.0% |
| Step-level F1 | 99.5% |
| Sequence accuracy (exact ordered step list, all fields) | 93.8% (30/32) |
| Mean normalised LCS of step sequences | 99.4% |
| Steps predicted / gold | 191 / 193 |

### Field-level accuracy (position-aligned, over max(len(pred), len(gold)) positions)

| Field | Accuracy |
|---|---|
| `step_no` | 99.0% |
| `phase` | 99.0% |
| `system_id` | 96.9% |
| `resource_id` | 96.9% |
| `operation` | 96.9% |
| `state` | 96.9% |
| `evidence_id` | 99.0% |

### Remaining sample mismatches

- **case_18** — predicted INCOMPLETE, gold INCOMPLETE
  - missing: `('VERIFICATION', 'security_service', 'audit_record_6645', 'VERIFY_RECORD_PRESENT', 'PRESENT', '')`
- **case_20** — predicted INCOMPLETE, gold INCOMPLETE
  - missing: `('VERIFICATION', 'security_service', 'audit_record_5569', 'VERIFY_RECORD_PRESENT', 'PRESENT', '')`

## 2. Custom evaluation cases (participant-authored)

Each case re-uses a public subject so its expected answer is known, then changes one thing the agent must handle (language, negation, injection, identifier casing, audit cutoff).

| Case | Tests | Result | Detail |
|---|---|---|---|
| custom_01 | Negated deletion vocabulary ('don't delete or close') must not authorise deletion. | PASS | status NOT_APPLICABLE (expected NOT_APPLICABLE); missing none |
| custom_02 | Non-English access request with negation (Spanish) is NOT_APPLICABLE. | PASS | status NOT_APPLICABLE (expected NOT_APPLICABLE); missing none |
| custom_03 | Prompt injection inside request_text must not change the evidence-based answer (gold case_05). | PASS | status INCOMPLETE (expected INCOMPLETE); 3 steps vs 3 |
| custom_04 | Upper-case historical email must resolve to the same subject (gold case_10). | PASS | status INCOMPLETE (expected INCOMPLETE); 4 steps vs 4 |
| custom_05 | Korean phrasing of a tombstone case must give the same answer (gold case_31). | PASS | status COMPLETE (expected COMPLETE); 3 steps vs 3 |
| custom_06 | Point-in-time: moving audit_at after evidence_02 (captured 2026-09-17, account still ACTIVE) must flip case_27 from COMPLETE to INCOMPLETE, citing evidence_02. | PASS | status INCOMPLETE (expected INCOMPLETE); missing none |
| custom_07 | Point-in-time: with audit_at before evidence_92 exists, no step may cite evidence captured later. | PASS | status INCOMPLETE; 0 step(s) cite later evidence |

**7/7 custom cases pass.**

## 3. Evaluation-set diagnostics (518 requests, no labels)

Status distribution: COMPLETE 153, INCOMPLETE 355, NOT_APPLICABLE 10.

How each deletion case's account resource was linked:

| Method | Cases |
|---|---|
| evidence | 240 |
| batch-delay-match | 131 |
| batch-unique | 127 |
| subject-linked (outside window) | 7 |
| naming-convention fallback | 2 |
| none | 1 |

- Accounts chosen among tied candidates (confidence < 0.5): 29
- Identifier-less policy rows attached by delay matching: 119
- Screenshots read by the vision model in this run: 10 / 11 (others use catalog-link + type defaults)

## 4. Failures found and improvements made

| # | Failure found (how) | Improvement | Effect |
|---|---|---|---|
| 1 | Draft plan gated discovery on file capture time; red-team measurement showed gold answers discover audit records from later files whose *record* time precedes audit_at (case_09/23/24/29/30) | Two-tier time rule: discover by record time, cite only files captured ≤ audit_at | ~120 eval verification steps recovered; samples 23/29/30 exact |
| 2 | Prototype grouped log traces only for `trace_id=`/`requestId=` syntaxes (27 eval accounts unlinked) | Syntax-agnostic trace key across all 7 log syntaxes | +27 evidence-linked accounts |
| 3 | Most account ids exist only in deletion-worker activity; window + result mapping left ~100 eval cases ambiguous | Delay model calibrated at runtime from evidence-anchored pairs + exact per-component matching | 31/32 sample accounts; ties reduced to the cases listed above |
| 4 | Support attachments indistinguishable from messages in inventory/export files | Category priority: explicit collection/event → worker's attempted operation → default | DELETE vs REDACT correct for attachments (e.g. case_131 support_2315) |
| 5 | Legal holds linked only by a RETAIN_RECORD worker row had no observation and were dropped (case_287, case_98) | Successfully retained records stay VERIFY_RECORD_PRESENT | +2 eval steps |
| 6 | Hand-run sample cases (case_04) have no batch account; second user cases (case_61) blocked from re-using their own account | Same-user account sharing, off-grid worker-row attachment, low-confidence `account_<n>` fallback when no one owns that id | samples 29/32 → 30/32 exact |
| 7 | Over-broad intent pattern ('download … data') marked sample case_08 as non-deletion; case_26 had no deletion verb | Narrowed retention patterns, added verification phrasings; LLM cross-check with rule veto on explicit retention language | exactly the 10 non-deletion eval requests flagged |
| 8 | JSON keys were sorted; sample file uses the documented key order | Emit documented order | byte-identical rows for 20+ sample cases |
| 9 | First live run: gemini-2.5-* returned HTTP 404 (closed to new keys) and Groq HTTP 403 (default urllib User-Agent rejected) | Default models gemini-3.5-flash-lite (intent) / gemini-3.6-flash (vision) with per-family thinking settings; explicit User-Agent | 15/15 live calls succeed |
| 10 | With the model allowed to override rules, sample case_19 ('remove my profile … the conversation itself may need to stay') was misread as NON_DELETION — status accuracy fell 100% → 96.9% | Explicit rule signals (retention wording or a deletion verb) win; the model decides only requests with no explicit signal; disagreements are traced | back to 100% status; 0 eval disagreements |
| 11 | Vision reads marketing_001 (evidence_60) as showing a different person (Soo-jin Park) than the data-catalog link (kwame-mensah@proton.me, user_09) | Catalog binding kept, screen identifiers added to the observation; conflict noted for review | case_63 keeps its finding |

### Known unwinnable / residual errors

- Some gold steps reference ids that appear nowhere in participant data (sample case_18 `audit_record_6645`, case_20 `audit_record_5569`). The agent never invents ids, so these steps are missed by design; the evaluation set likely has similar cases.
- Accounts chosen among exact ties are ~50% likely to be the wrong one of the pair; the trace for each such case lists the alternatives.
- `account_<n>` fallback ids (low confidence) are used only when no evidence or activity links any account to the subject.

