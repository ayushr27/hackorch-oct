# case_523 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_521: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_2424: USER_PROFILE → DELETE; state PII (proof evidence_62); linked by evidence (activity_246, confidence 1.0); category USER_PROFILE: resource type default
- security_service/audit_record_2172: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_49; category SECURITY_AUDIT_LOG: resource type default; state from evidence_49 (captured after audit_at; not citable)
- search_service/search_9075: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_62); linked by identifier match in evidence_62; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | account_service | account_2424 | REPORT_REMAINING_RECORD | PRESENT | evidence_62 |
| 2 | FINDING | search_service | search_9075 | REPORT_REMAINING_RECORD | PRESENT | evidence_62 |
| 3 | REMEDIATION | account_service | account_2424 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | search_service | search_9075 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_2424 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_9075 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_2172 | VERIFY_RECORD_PRESENT | PRESENT |  |
