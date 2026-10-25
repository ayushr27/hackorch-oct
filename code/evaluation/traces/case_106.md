# case_106 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_104: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_8804: USER_PROFILE → DELETE; state ABSENT (proof evidence_10); linked by batch-delay-match (activity_3272, confidence 0.966); alternatives ['account_4514']; category USER_PROFILE: resource type default
- security_service/audit_record_8723: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_10); linked by identifier match in evidence_10; category SECURITY_AUDIT_LOG: resource type default
- search_service/search_7223: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_10); linked by identifier match in evidence_10; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_7223 | REPORT_REMAINING_RECORD | PRESENT | evidence_10 |
| 2 | REMEDIATION | search_service | search_7223 | DELETE_RECORD | ABSENT |  |
| 3 | VERIFICATION | account_service | account_8804 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | search_service | search_7223 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 5 | VERIFICATION | security_service | audit_record_8723 | VERIFY_RECORD_PRESENT | PRESENT |  |
