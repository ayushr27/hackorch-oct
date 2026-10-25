# case_154 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_152: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_7680: USER_PROFILE → DELETE; state ABSENT (proof evidence_15); linked by batch-unique (activity_2809, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_2580: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_15); linked by identifier match in evidence_15; category SECURITY_AUDIT_LOG: resource type default
- search_service/search_1446: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_15); linked by identifier match in evidence_15; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_1446 | REPORT_REMAINING_RECORD | PRESENT | evidence_15 |
| 2 | REMEDIATION | search_service | search_1446 | DELETE_RECORD | ABSENT |  |
| 3 | VERIFICATION | account_service | account_7680 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | search_service | search_1446 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 5 | VERIFICATION | security_service | audit_record_2580 | VERIFY_RECORD_PRESENT | PRESENT |  |
