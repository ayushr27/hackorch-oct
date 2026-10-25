# case_400 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_398: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_928: USER_PROFILE → DELETE; state ABSENT (proof evidence_69); linked by batch-unique (activity_940, confidence 0.95); category USER_PROFILE: resource type default
- search_service/search_4649: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_69); linked by identifier match in evidence_69; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_4521: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_69); linked by identifier match in evidence_69; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_4649 | REPORT_REMAINING_RECORD | PRESENT | evidence_69 |
| 2 | FINDING | support_platform | support_4521 | REPORT_EXPOSED_PII | PRESENT | evidence_69 |
| 3 | REMEDIATION | search_service | search_4649 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_4521 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_928 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_4649 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | support_platform | support_4521 | VERIFY_RECORD_REDACTED | REDACTED |  |
