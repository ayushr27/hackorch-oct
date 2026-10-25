# case_352 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_350: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_6215: USER_PROFILE → DELETE; state ABSENT (proof evidence_71); linked by batch-unique (activity_1399, confidence 0.95); category USER_PROFILE: resource type default
- search_service/search_5685: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_71); linked by identifier match in evidence_71; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_3980: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_71); linked by identifier match in evidence_71; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_5685 | REPORT_REMAINING_RECORD | PRESENT | evidence_71 |
| 2 | FINDING | support_platform | support_3980 | REPORT_EXPOSED_PII | PRESENT | evidence_71 |
| 3 | REMEDIATION | search_service | search_5685 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_3980 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_6215 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_5685 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | support_platform | support_3980 | VERIFY_RECORD_REDACTED | REDACTED |  |
