# case_428 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_426: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_2157: USER_PROFILE → DELETE; state ABSENT (proof evidence_68); linked by batch-unique (activity_849, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_7557: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_40; category SECURITY_AUDIT_LOG: resource type default; state from evidence_40 (captured after audit_at; not citable)
- integration_service/data_flow_2107: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_68); linked by identifier match in evidence_68; category DATA_FLOW: resource type default
- search_service/search_2625: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_68); linked by identifier match in evidence_68; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_2625 | REPORT_REMAINING_RECORD | PRESENT | evidence_68 |
| 2 | FINDING | integration_service | data_flow_2107 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_68 |
| 3 | REMEDIATION | integration_service | data_flow_2107 | DISABLE_DATA_FLOW | DISABLED |  |
| 4 | REMEDIATION | search_service | search_2625 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_2157 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_2625 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_7557 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | integration_service | data_flow_2107 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
