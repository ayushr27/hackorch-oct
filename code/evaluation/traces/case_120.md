# case_120 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_118: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_8656: USER_PROFILE → DELETE; state ABSENT (proof -); linked by evidence (activity_2975, confidence 1.0); category USER_PROFILE: resource type default; state from evidence_11 (captured after audit_at; not citable)
- security_service/audit_record_5496: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_11; category SECURITY_AUDIT_LOG: resource type default; state from evidence_11 (captured after audit_at; not citable)
- export_service/export_4289: USER_EXPORT → DELETE; state PII (proof evidence_88); linked by identifier match in evidence_88; category USER_EXPORT: resource type default
- search_service/search_943: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_88); linked by identifier match in evidence_88; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | export_service | export_4289 | REPORT_REMAINING_RECORD | PRESENT | evidence_88 |
| 2 | FINDING | search_service | search_943 | REPORT_REMAINING_RECORD | PRESENT | evidence_88 |
| 3 | REMEDIATION | export_service | export_4289 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | search_service | search_943 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_8656 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | export_service | export_4289 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | search_service | search_943 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 8 | VERIFICATION | security_service | audit_record_5496 | VERIFY_RECORD_PRESENT | PRESENT |  |
