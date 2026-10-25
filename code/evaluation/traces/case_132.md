# case_132 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'exclusão' (LLM agrees)
- subject user_130: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_4395: USER_PROFILE → DELETE; state ABSENT (proof evidence_87); linked by batch-unique (activity_3015, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_1424: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_12; category SECURITY_AUDIT_LOG: resource type default; state from evidence_12 (captured after audit_at; not citable)
- export_service/export_9157: USER_EXPORT → DELETE; state PII (proof evidence_87); linked by identifier match in evidence_87; category USER_EXPORT: resource type default
- search_service/search_3112: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_87); linked by identifier match in evidence_87; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | export_service | export_9157 | REPORT_REMAINING_RECORD | PRESENT | evidence_87 |
| 2 | FINDING | search_service | search_3112 | REPORT_REMAINING_RECORD | PRESENT | evidence_87 |
| 3 | REMEDIATION | export_service | export_9157 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | search_service | search_3112 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_4395 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | export_service | export_9157 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | search_service | search_3112 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 8 | VERIFICATION | security_service | audit_record_1424 | VERIFY_RECORD_PRESENT | PRESENT |  |
