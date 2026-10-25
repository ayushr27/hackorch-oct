# Ghost Data Still Exists — deletion-audit agent

HackerRank Orchestrate (October 2026). For every request in `dataset/deletion_requests.csv`
the agent decides whether deletion was actually requested, reconstructs the subject's current
and historical identifiers, investigates every evidence source *as of `audit_at`*, applies
`deletion_rules.csv`, and returns `COMPLETE` / `INCOMPLETE` / `NOT_APPLICABLE` with an ordered
FINDING → REMEDIATION → VERIFICATION plan. Full contract: [`problem_statement.md`](./problem_statement.md).

## Quick start

```bash
python3 -m venv .venv && .venv/bin/pip install -r code/requirements.txt   # pypdf only
.venv/bin/python code/main.py                 # → output.csv (repo root), validated
.venv/bin/python code/evaluation/main.py      # → code/evaluation/{evaluation_report,usage_report}.md
```

Python ≥ 3.9 (tested on 3.9.6 and 3.14). Everything else is the standard library (sqlite3, json,
csv, urllib). PDF text is cached in `code/cache/pdf_text.json`, so the run also works with no
`pypdf`/`pdftotext` installed; plain `python3 code/main.py` without a venv is fine.
On Windows use `.venv\Scripts\python code\main.py`.

| Command | What it does |
|---|---|
| `python3 code/main.py` | Cache-first run; calls the free LLM APIs only for cache misses when a key is configured |
| `python3 code/main.py --offline` | Never calls an LLM (cache + deterministic fallbacks). Byte-identical to the online run once the cache is warm |
| `python3 code/main.py --refresh-llm` | Ignore the cache and call live (used for the final run recorded in `usage_report.md`) |
| `python3 code/main.py --traces code/evaluation/traces` | Also write a per-case investigation memo (Markdown) |
| `python3 code/main.py --input <csv> --output <csv>` | Audit another request file |

### Free LLM APIs (optional)

Put keys in an **uncommitted** `.env` at the repo root (never in code or logs):

```
GEMINI_API_KEY=...        # Google AI Studio free tier — primary (intent + screenshots)
GROQ_API_KEY=...          # Groq free tier — fallback
# optional model overrides: INTENT_MODEL, VISION_MODEL, GROQ_INTENT_MODEL, GROQ_VISION_MODEL
```

A full run needs ~15 calls (4 batched intent calls over 375 unique request texts + 11
screenshots). Without keys the agent still runs: it uses the committed cache in
`code/cache/llm_cache.json`, then deterministic fallbacks. Free-tier prompts may be used by
the provider to improve products; only fictional request text and screenshots are sent.

## Architecture

```
dataset/ ──► evidence.py      SQL inventory + replica dumps, JSON exports/bundles/ledgers, handover TXT,
                              7 log syntaxes (trace-joined), PDFs  →  Observation(file, record time,
                              system, resource, state, identifier tokens) + Scope(capture covered system S)
         ──► perception.py    screenshots/PDFs bound to resources via data-catalog LINK rows; state from
                              the vision model (cached) or text/type defaults
         ──► core.py          identity: user_id + every current/historical email, phone, sha256 email hash
         ──► intent.py/llm.py negation-aware rules × LLM classifier (rules veto on explicit retention)
         ──► linkage.py       activity-batch correlation for identifier-less ids (accounts, anonymised
                              analytics, legal holds): delay model calibrated at runtime from
                              evidence-anchored pairs + exact max-likelihood matching per component
         ──► audit.py         point-in-time state, policy (rules → action), absence proofs, step planner
         ──► pipeline.py      orchestration + serialisation;  validate.py  output contract checks
```

Key rules the engine enforces:

- **Two-tier time.** A resource is *discovered* when an observation whose own time is in
  `[requested_at, audit_at]` carries a subject identifier (any file, even one captured later). Its
  *state* and *citation* come only from files captured ≤ `audit_at`; the latest observation wins.
  Evidence from before `requested_at` belongs to an earlier episode.
- **Claims are not proof.** `reported_status`, `reported_result` and activity messages never decide a state.
- **Absence by scope.** A resource is absent when a trusted capture covering its system does not list it
  (or an explicit 404 / NOT_FOUND / rows=0).
- **Policy.** Category comes from the source (collection/event/handover) first, then the deletion
  workflow's attempted operation, then the resource type. Retained records (security audit, legal hold)
  are verified PRESENT; backups are retained with restores blocked; tombstones keep only the stable
  `user_id`.
- **Steps.** Phase → operation order of the problem-statement table → `system_id` → `resource_id`.
  COMPLETE cites the proving file per step; INCOMPLETE remediation/verification use `""`.
- **The LLM never decides.** Its outputs are enum/id-constrained and validated against the engine's
  own candidates; request and evidence text is treated as data (see the injection custom case).

## Evaluation

`code/evaluation/evaluation_report.md` (also copied to `evaluation/`) reports case, step, field and
sequence accuracy on the 32 public samples, 7 custom cases, evaluation-set linkage diagnostics, and
the failures found / improvements made. `usage_report.md` summarises model calls, tokens and cost
for the final run.

## Repository layout

```
code/main.py                CLI entry point
code/ghost/                 engine (see architecture)
code/prompts/*.md           LLM prompts
code/cache/                 LLM response cache + usage ledger + last-run summary
code/evaluation/main.py     evaluation harness and report generator
history.md                  actions taken while building the solution
log.txt                     AI-assistant session log (chat transcript)
```

## Packaging

```bash
zip -r code.zip README.md code evaluation -x "*/__pycache__/*" "*/.venv/*" "*/venv/*" "*/.git/*" "*/.DS_Store" "*.env" "*/.env" "*.zip"
```

Challenge / submission page:
https://www.hackerrank.com/contests/hackerrank-orchestrate-october26/challenges/ghost-data-still-exists
