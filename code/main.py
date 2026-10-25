"""Ghost Data Still Exists — deletion-audit agent CLI.

    python3 code/main.py                      # audit dataset/deletion_requests.csv -> output.csv
    python3 code/main.py --offline            # never call an LLM (cache + deterministic fallbacks)
    python3 code/main.py --traces code/evaluation/traces   # also write per-case investigation memos
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ghost.core import CACHE_DIR, DATASET, ROOT  # noqa: E402
from ghost.pipeline import case_sort_key, run_all, serialise  # noqa: E402
from ghost.validate import validate  # noqa: E402


def write_traces(results, directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    for r in results:
        lines = [f"# {r.case_id} — {r.status}", "", "## Investigation", ""]
        lines += [f"- {t}" for t in r.trace]
        lines += ["", "## Steps", "", "| # | phase | system | resource | operation | state | evidence |",
                  "|---|---|---|---|---|---|---|"]
        lines += [f"| {s['step_no']} | {s['phase']} | {s['system_id']} | {s['resource_id']} | "
                  f"{s['operation']} | {s['state']} | {s['evidence_id']} |" for s in r.steps]
        (directory / f"{r.case_id}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=DATASET / "deletion_requests.csv")
    ap.add_argument("--output", type=Path, default=ROOT / "output.csv")
    ap.add_argument("--context", type=Path, nargs="*", default=[DATASET / "sample_deletion_requests.csv"],
                    help="extra request files used only as cross-case linkage context")
    ap.add_argument("--offline", action="store_true", help="never call an LLM")
    ap.add_argument("--refresh-llm", action="store_true", help="ignore the LLM cache and call live")
    ap.add_argument("--max-llm-calls", type=int, default=40)
    ap.add_argument("--traces", type=Path, help="directory for per-case investigation memos")
    args = ap.parse_args(argv)

    from ghost.llm import build_perception  # noqa: E402
    engine_kw, llm = build_perception(offline=args.offline, refresh=args.refresh_llm,
                                      max_calls=args.max_llm_calls)

    context = [p for p in args.context if p.resolve() != args.input.resolve()]
    eng, main_reqs, _, results = run_all(args.input, context, **engine_kw)
    ordered = sorted((results[r.case_id] for r in main_reqs), key=lambda r: case_sort_key(r.case_id))
    args.output.write_text(serialise(ordered), encoding="utf-8", newline="")
    if args.traces:
        write_traces(ordered, args.traces)

    counts = {}
    for r in ordered:
        counts[r.status] = counts.get(r.status, 0) + 1
    print(f"wrote {args.output} — {len(ordered)} cases {counts}")
    hits = sum(1 for e in llm.events if e["cache_hit"])
    tokens = sum(e.get("input_tokens", 0) + e.get("output_tokens", 0) for e in llm.events)
    print(f"llm: {llm.live_calls} live call(s), {hits} cache hit(s), {tokens} live tokens (run {llm.run_id})")
    if args.output.resolve() == (ROOT / "output.csv").resolve():
        summary = {"run_id": llm.run_id, "requests": len(ordered), "status_counts": counts,
                   "offline": args.offline, "live_calls": llm.live_calls, "cache_hits": hits,
                   "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(),
                   "finished_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
        (CACHE_DIR / "last_run.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    errors = validate(args.output, args.input)
    if errors:
        print(f"VALIDATION FAILED ({len(errors)}):", *errors[:20], sep="\n  ")
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
