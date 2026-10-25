# Usage report — Ghost Data Still Exists

_Generated 2026-10-25 09:50 UTC from `code/cache/usage_ledger.jsonl`._

## Final full-dataset run that produced `output.csv`

- Run id: `1ea80f4eb5a1` finished 2026-10-25T09:50:06Z; 518 requests; status counts {'INCOMPLETE': 355, 'COMPLETE': 153, 'NOT_APPLICABLE': 10}
- Mode: online (cache first, live on miss); live calls 15, cache hits 0
- `output.csv` sha256 `8290f4cd0ba84e3d45614202e51c3209c6eed36e69dd4e53758dcca4211df6ed`

### Model calls in the final run

| Provider | Model | Purpose | Calls | Cache hits | Input tokens | Output tokens | Thinking tokens | Paid-equivalent cost (USD) |
|---|---|---|---|---|---|---|---|---|
| google-ai-studio | gemini-3.5-flash-lite | intent | 4 | 0 | 17630 | 12866 | 0 | 0.00691 |
| google-ai-studio | gemini-3.6-flash | vision | 8 | 0 | 11412 | 500 | 902 | 0.00693 |
| groq | qwen/qwen3.8-27b | vision | 3 | 0 | 6935 | 305 | 0 | 0.00226 |
| **Total** | | | 15 | 0 | 35977 | 13671 | 902 | 0.01610 |

- Total live tokens: **50550**; average per request: **97.6**
- Actual cost: **$0.00** (free tiers); paid-equivalent: **$0.01610** total, **$0.0000311** per request

### All live calls recorded (runs that populated the cache)

| Provider | Model | Purpose | Calls | Cache hits | Input tokens | Output tokens | Thinking tokens | Paid-equivalent cost (USD) |
|---|---|---|---|---|---|---|---|---|
| google-ai-studio | gemini-3.5-flash-lite | intent | 8 | 0 | 35260 | 26538 | 0 | 0.01414 |
| google-ai-studio | gemini-3.6-flash | vision | 19 | 0 | 27111 | 1174 | 1015 | 0.01361 |
| groq | qwen/qwen3.8-27b | vision | 3 | 0 | 6935 | 305 | 0 | 0.00226 |
| **Total** | | | 30 | 0 | 69306 | 28017 | 1015 | 0.03001 |

## Design notes

- ~15 calls per full run: 4 intent calls (375 unique request texts, 100 per call) + 11 screenshot calls. The deterministic engine needs no model for SQL/JSON/log/PDF evidence.
- Every response is cached by content hash (prompt version + prompt + image sha256); reruns and `--offline` replay the cache, so output is reproducible without keys.
- Paid-equivalent prices are approximate list prices per 1M tokens and must be re-checked against the providers' pricing pages: gemini-3.6-flash $0.3/$2.5, gemini-3.5-flash-lite $0.1/$0.4, gemini-2.5-flash $0.3/$2.5, gemini-2.5-flash-lite $0.1/$0.4, openai/gpt-oss-20b $0.1/$0.5, qwen/qwen3.8-27b $0.3/$0.6.

