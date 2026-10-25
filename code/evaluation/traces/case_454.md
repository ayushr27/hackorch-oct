# case_454 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_452: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_3024: USER_PROFILE → DELETE; state ABSENT (proof evidence_43); linked by batch-unique (activity_566, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_2775: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_43); linked by identifier match in evidence_43; category SECURITY_AUDIT_LOG: resource type default
- search_service/search_892: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_43); linked by identifier match in evidence_43; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_892 | REPORT_REMAINING_RECORD | PRESENT | evidence_43 |
| 2 | REMEDIATION | search_service | search_892 | DELETE_RECORD | ABSENT |  |
| 3 | VERIFICATION | account_service | account_3024 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | search_service | search_892 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 5 | VERIFICATION | security_service | audit_record_2775 | VERIFY_RECORD_PRESENT | PRESENT |  |
