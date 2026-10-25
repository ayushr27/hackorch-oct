# case_198 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_196: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_2210: USER_PROFILE → DELETE; state ABSENT (proof evidence_20); linked by batch-unique (activity_2427, confidence 0.95); category USER_PROFILE: resource type default; never observed; absence proven by evidence_20
- search_service/search_1414: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_82); linked by identifier match in evidence_82; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_6131: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_82); linked by identifier match in evidence_82; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_1414 | REPORT_REMAINING_RECORD | PRESENT | evidence_82 |
| 2 | FINDING | support_platform | support_6131 | REPORT_EXPOSED_PII | PRESENT | evidence_82 |
| 3 | REMEDIATION | search_service | search_1414 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_6131 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_2210 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_1414 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | support_platform | support_6131 | VERIFY_RECORD_REDACTED | REDACTED |  |
