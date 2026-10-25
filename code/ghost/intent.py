"""Does the request authorise deletion?  Negation-aware rules (always available) that the
LLM classifier is cross-checked against; rules veto the LLM on explicit retention language."""
from __future__ import annotations

import re

DELETE, NON_DELETION = "DELETE_ACCOUNT", "NON_DELETION"

# Explicit "do not delete / keep it" language, or a request whose whole purpose is
# something else (access, export, correction, marketing opt-out, login help).
RETAIN_PATTERNS = [
    r"\bnot (?:asking|a request) (?:for|to) (?:deletion|delet|eras|remov|clos)",
    r"\bdo(?:n'?t| not) (?:close|delete|erase|remove|change)",
    r"\bwithout removing\b",
    r"\bkeep (?:the|my) account\b",
    r"\bleave (?:the|my) (?:account|profile)\b",
    r"\bcontinue using\b",
    r"\bstill (?:need|use|want) (?:the|my|it|receipts)",
    r"\bmarketing lists only\b",
    r"\bstop the promotional emails\b",
    r"\bdownload my (?:account )?(?:information|data)\b",
    r"\bcopy of (?:the |my |last year's )?(?:information|invoices|data)\b",
    r"\bwhat personal information you hold\b",
    r"\b(?:replace|correct|change) (?:it|the email|my|the mobile)",
    r"\bresetting the login\b",
]
DELETE_PATTERNS = [
    r"\bdelet", r"\beras", r"\bremov", r"\bclos(?:e|ed|ing)\b", r"\bdeletion\b",
    r"exclus[ãa]o", r"suppression", r"eliminaci[óo]n", r"\beliminar\b", r"削除", r"삭제",
    r"\b(?:profile|account) is gone\b", r"\bcannot identify me\b",
]


def rule_intent(text: str) -> tuple[str, str]:
    """(label, reason)."""
    t = text.lower().replace("’", "'")
    for p in RETAIN_PATTERNS:
        m = re.search(p, t)
        if m:
            return NON_DELETION, f"retention/non-deletion language: '{m.group(0)}'"
    for p in DELETE_PATTERNS:
        m = re.search(p, t)
        if m:
            return DELETE, f"deletion language: '{m.group(0)}'"
    return NON_DELETION, "no deletion language"
