# case_498 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eliminación' (LLM agrees)
- subject user_496: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_282: USER_PROFILE → DELETE; state ABSENT (proof evidence_63); linked by batch-unique (activity_230, confidence 0.95); category USER_PROFILE: resource type default
- search_service/search_6093: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_63); linked by identifier match in evidence_63; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_9075: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_63); linked by identifier match in evidence_63; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_6093 | REPORT_REMAINING_RECORD | PRESENT | evidence_63 |
| 2 | FINDING | support_platform | support_9075 | REPORT_EXPOSED_PII | PRESENT | evidence_63 |
| 3 | REMEDIATION | search_service | search_6093 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_9075 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_282 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_6093 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | support_platform | support_9075 | VERIFY_RECORD_REDACTED | REDACTED |  |
