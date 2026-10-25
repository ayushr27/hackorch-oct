"""Free-tier LLM perception: request intent (text) and screenshot reading (vision).

Resolution order for every call (deterministic, grader-safe):
  1. committed content-hash cache  (code/cache/llm_cache.json)
  2. live call — Google AI Studio Gemini (free tier) first, Groq (free tier) as fallback
  3. caller's deterministic fallback (rules / catalog links) when both are unavailable

The model only perceives: outputs are schema-constrained enums/ids that are validated
against the engine's own candidates. It never decides a case status or steps.
Keys come only from the environment (or an uncommitted .env); never logged.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone

from .core import CACHE_DIR, CODE, ROOT
from .evidence import ABSENT, ACTIVE, CLEAN, INACTIVE, PII, resource_prefix
from .intent import DELETE, NON_DELETION

PROMPTS = CODE / "prompts"
CACHE_FILE = CACHE_DIR / "llm_cache.json"
LEDGER_FILE = CACHE_DIR / "usage_ledger.jsonl"
PROMPT_VERSION = "v1"
INTENT_BATCH = 100
MIN_INTERVAL_S = 6.0          # stay far below free-tier RPM limits

VISION_STATES = {
    "PRESENT_WITH_IDENTIFIERS": PII, "PRESENT_WITHOUT_IDENTIFIERS": CLEAN, "NOT_PRESENT": ABSENT,
    "FLOW_ENABLED": ACTIVE, "FLOW_DISABLED": INACTIVE,
    "RESTORE_ALLOWED": ACTIVE, "RESTORE_BLOCKED": INACTIVE,
}


def load_env():
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_prompt(name: str) -> str:
    return (PROMPTS / name).read_text(encoding="utf-8")


class LLMError(RuntimeError):
    pass


def _post(url: str, body: dict, headers: dict, timeout=150) -> dict:
    # An explicit User-Agent: some API edges reject urllib's default one (HTTP 403).
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "User-Agent": "ghost-audit/1.0",
                                          **headers})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ------------------------------------------------------------------ providers

class Gemini:
    name = "google-ai-studio"

    def __init__(self, model: str):
        self.model = model
        self.key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    def available(self) -> bool:
        return bool(self.key)

    def generate(self, prompt: str, schema: dict, image: tuple[str, bytes] | None = None):
        parts = [{"text": prompt}]
        if image:
            parts.append({"inline_data": {"mime_type": image[0], "data": base64.b64encode(image[1]).decode()}})
        config = {"temperature": 0, "responseMimeType": "application/json", "responseSchema": schema}
        # Keep thinking minimal: perception needs none and thought tokens are billed as output.
        if self.model.startswith("gemini-2.5"):
            config["thinkingConfig"] = {"thinkingBudget": 0}
        else:
            config["thinkingConfig"] = {"thinkingLevel": "minimal" if "lite" in self.model else "low"}
        body = {"contents": [{"role": "user", "parts": parts}], "generationConfig": config}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        data = _post(url, body, {"x-goog-api-key": self.key})
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as exc:
            raise LLMError(f"unexpected Gemini response shape: {list(data)}") from exc
        u = data.get("usageMetadata", {})
        usage = {"input_tokens": u.get("promptTokenCount", 0), "output_tokens": u.get("candidatesTokenCount", 0),
                 "thought_tokens": u.get("thoughtsTokenCount", 0)}
        return json.loads(text), usage


class Groq:
    name = "groq"

    def __init__(self, model: str):
        self.model = model
        self.key = os.environ.get("GROQ_API_KEY")

    def available(self) -> bool:
        return bool(self.key)

    def generate(self, prompt: str, schema: dict, image: tuple[str, bytes] | None = None):
        content = prompt + "\n\nReturn a single JSON object that matches this JSON schema:\n" + json.dumps(schema)
        if image:
            data_url = f"data:{image[0]};base64,{base64.b64encode(image[1]).decode()}"
            message = {"role": "user", "content": [{"type": "text", "text": content},
                                                   {"type": "image_url", "image_url": {"url": data_url}}]}
        else:
            message = {"role": "user", "content": content}
        body = {"model": self.model, "messages": [message], "temperature": 0,
                "response_format": {"type": "json_object"}}
        data = _post("https://api.groq.com/openai/v1/chat/completions", body,
                     {"Authorization": f"Bearer {self.key}"})
        text = data["choices"][0]["message"]["content"]
        u = data.get("usage", {})
        usage = {"input_tokens": u.get("prompt_tokens", 0), "output_tokens": u.get("completion_tokens", 0),
                 "thought_tokens": 0}
        return json.loads(text), usage


# --------------------------------------------------------------------- client

class LLM:
    def __init__(self, offline: bool = False, refresh: bool = False, max_calls: int = 40):
        load_env()
        self.offline, self.refresh, self.max_calls = offline, refresh, max_calls
        # gemini-2.5-* is closed to new API keys (HTTP 404 "no longer available to new users").
        self.text_providers = [Gemini(os.environ.get("INTENT_MODEL", "gemini-3.5-flash-lite")),
                               Groq(os.environ.get("GROQ_INTENT_MODEL", "openai/gpt-oss-20b"))]
        self.vision_providers = [Gemini(os.environ.get("VISION_MODEL", "gemini-3.6-flash")),
                                 Groq(os.environ.get("GROQ_VISION_MODEL", "qwen/qwen3.8-27b"))]
        self.cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}
        self.run_id = uuid.uuid4().hex[:12]
        self.live_calls = 0
        self.events: list[dict] = []
        self._last_call = 0.0

    def _ledger(self, rec: dict):
        rec = {"run_id": self.run_id, "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **rec}
        self.events.append(rec)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(LEDGER_FILE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")

    def _save(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(json.dumps(self.cache, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                              encoding="utf-8")

    def call(self, purpose: str, prompt: str, schema: dict, validate, providers, image=None):
        """Validated JSON from cache or a live provider, or None."""
        image_sha = hashlib.sha256(image[1]).hexdigest() if image else ""
        key = hashlib.sha256(json.dumps([purpose, PROMPT_VERSION, prompt, image_sha]).encode()).hexdigest()
        hit = self.cache.get(key)
        if hit and not self.refresh:
            self._ledger({"purpose": purpose, "provider": hit["provider"], "model": hit["model"],
                          "cache_hit": True, "input_tokens": 0, "output_tokens": 0, "thought_tokens": 0,
                          "key": key[:16]})
            return hit["response"]
        if self.offline or self.live_calls >= self.max_calls:
            return None
        for p in providers:
            if not p.available():
                continue
            for attempt in range(4):
                wait = MIN_INTERVAL_S - (time.monotonic() - self._last_call)
                if wait > 0:
                    time.sleep(wait)
                self._last_call = time.monotonic()
                t0 = time.monotonic()
                try:
                    obj, usage = p.generate(prompt, schema, image)
                    self.live_calls += 1
                    obj = validate(obj)
                except urllib.error.HTTPError as exc:
                    if exc.code in (429, 500, 503) and attempt < 3:
                        time.sleep(2 ** (attempt + 2))
                        continue
                    print(f"  [llm] {p.name}/{p.model} {purpose}: HTTP {exc.code}")
                    break
                except (urllib.error.URLError, TimeoutError, LLMError, ValueError, KeyError) as exc:
                    print(f"  [llm] {p.name}/{p.model} {purpose}: {type(exc).__name__}")
                    break
                self._ledger({"purpose": purpose, "provider": p.name, "model": p.model, "cache_hit": False,
                              "latency_ms": int((time.monotonic() - t0) * 1000), "key": key[:16], **usage})
                self.cache[key] = {"purpose": purpose, "provider": p.name, "model": p.model,
                                   "prompt_version": PROMPT_VERSION, "response": obj, "usage": usage,
                                   "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
                self._save()
                return obj
        return None

    # ------------------------------------------------------------- intent
    def classify_intents(self, texts: list[str]) -> dict[str, str]:
        unique = sorted(set(texts))
        schema = {"type": "OBJECT", "required": ["items"], "properties": {"items": {
            "type": "ARRAY", "items": {"type": "OBJECT", "required": ["id", "label"], "properties": {
                "id": {"type": "INTEGER"},
                "label": {"type": "STRING", "enum": [DELETE, NON_DELETION]},
                "confidence": {"type": "NUMBER"}}}}}}
        out: dict[str, str] = {}
        base = load_prompt("intent.md")
        for start in range(0, len(unique), INTENT_BATCH):
            chunk = unique[start:start + INTENT_BATCH]
            lines = "\n".join(f"[{i}] <<<{t}>>>" for i, t in enumerate(chunk))

            def validate(obj, n=len(chunk)):
                items = obj["items"]
                labels = {}
                for it in items:
                    i = int(it["id"])
                    if 0 <= i < n and it["label"] in (DELETE, NON_DELETION):
                        labels[i] = it["label"]
                if len(labels) < n:
                    raise LLMError(f"intent answer covered {len(labels)}/{n} requests")
                return {"labels": [labels[i] for i in range(n)]}
            res = self.call("intent", base + lines, schema, validate, self.text_providers)
            if res:
                out.update(zip(chunk, res["labels"]))
        return out

    # ------------------------------------------------------------- vision
    def read_artifact(self, m, bound: list[dict]) -> dict | None:
        if m.path.suffix.lower() not in (".png", ".jpg", ".jpeg") or not bound:
            return None
        rids = sorted(b["resource_id"] for b in bound)
        schema = {"type": "OBJECT", "required": ["resources"], "properties": {"resources": {
            "type": "ARRAY", "items": {"type": "OBJECT", "required": ["resource_id", "state"], "properties": {
                "resource_id": {"type": "STRING", "enum": rids},
                "state": {"type": "STRING", "enum": sorted(VISION_STATES)},
                "identifiers": {"type": "ARRAY", "items": {"type": "STRING"}},
                "retained": {"type": "BOOLEAN"},
                "note": {"type": "STRING"}}}}}}

        def validate(obj):
            good = {}
            for r in obj["resources"]:
                rid, st = r.get("resource_id"), r.get("state")
                if rid not in rids or st not in VISION_STATES:
                    continue
                prefix = resource_prefix(rid)
                if (prefix == "data_flow") != st.startswith("FLOW_"):
                    continue
                if (prefix == "backup") != st.startswith("RESTORE_"):
                    continue
                good[rid] = {"state": VISION_STATES[st], "identifiers": [str(x) for x in r.get("identifiers", [])],
                             "note": str(r.get("note", ""))[:200]}
            return good
        mime = "image/png" if m.path.suffix.lower() == ".png" else "image/jpeg"
        prompt = load_prompt("vision.md") + "\n".join(f"- {r}" for r in rids)
        return self.call("vision", prompt, schema, validate, self.vision_providers,
                         image=(mime, m.path.read_bytes()))


def build_perception(offline: bool = False, refresh: bool = False, max_calls: int = 40):
    """Engine keyword arguments wired to an LLM client (cache-first)."""
    llm = LLM(offline=offline, refresh=refresh, max_calls=max_calls)
    return {"vision": llm.read_artifact, "intent_classifier": llm.classify_intents}, llm
