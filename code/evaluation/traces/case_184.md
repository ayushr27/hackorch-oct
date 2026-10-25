# case_184 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_182: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_9620: USER_PROFILE → DELETE; state ABSENT (proof evidence_83); linked by batch-unique (activity_2728, confidence 0.95); category USER_PROFILE: resource type default
- search_service/search_8680: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_83); linked by identifier match in evidence_83; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_1892: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_83); linked by identifier match in evidence_83; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_8680 | REPORT_REMAINING_RECORD | PRESENT | evidence_83 |
| 2 | FINDING | support_platform | support_1892 | REPORT_EXPOSED_PII | PRESENT | evidence_83 |
| 3 | REMEDIATION | search_service | search_8680 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_1892 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_9620 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_8680 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | support_platform | support_1892 | VERIFY_RECORD_REDACTED | REDACTED |  |
