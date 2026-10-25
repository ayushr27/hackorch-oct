# History — actions taken

Append-only record of actions on the Ghost Data Still Exists solution. Newest at the bottom.

| Timestamp (UTC) | Action | Files | Result |
|---|---|---|---|
| 2026-10-25T05:00Z | Read challenge docs and dataset structure | AGENTS.md, problem_statement.md, README.md, dataset/*.csv | 518 eval cases, 32 samples, 94 evidence files (24 SQL, 29 records, 26 logs, 11 PNG, 4 PDF) |
| 2026-10-25T05:05Z | Explore workflow (4 read-only agents) | dataset/** (read-only) | All SQL/JSON/TXT/logs parse deterministically; only PNGs need vision; golden ordering rules reproduce 32/32 samples; account ids mostly linkable only via activity batches |
| 2026-10-25T05:20Z | Red-team workflow (4 lenses) on draft plan | dataset/** (read-only) | 14 threats found; top fixes: two-tier time rule, syntax-agnostic trace join, verify retained + compliant records, 3-tier LLM resolver with offline mode; approach scored 86/100 vs per-case LLM agent 48 |
| 2026-10-25T05:25Z | Plan approved | ~/.claude/plans/read-the-folder-devise-curried-pearl.md | Hybrid deterministic engine + free-tier LLM perception |
| 2026-10-25T05:27Z | Step 0: logging + hygiene | log.txt, history.md, .gitignore | Session start + turn entry logged; local .gitignore added (enclosing ~/Documents git repo has a remote — never commit from it) |
