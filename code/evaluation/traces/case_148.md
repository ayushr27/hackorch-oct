# case_148 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_146: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_5023: USER_PROFILE → DELETE; state ABSENT (proof evidence_86); linked by batch-delay-match (activity_2946, confidence 1.0); alternatives ['account_8632', 'account_7864']; category USER_PROFILE: resource type default
- search_service/search_7239: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_86); linked by identifier match in evidence_86; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_5716: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_86); linked by identifier match in evidence_86; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_7239 | REPORT_REMAINING_RECORD | PRESENT | evidence_86 |
| 2 | FINDING | support_platform | support_5716 | REPORT_EXPOSED_PII | PRESENT | evidence_86 |
| 3 | REMEDIATION | search_service | search_7239 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_5716 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_5023 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_7239 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | support_platform | support_5716 | VERIFY_RECORD_REDACTED | REDACTED |  |
