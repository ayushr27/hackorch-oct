# case_181 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_179: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_5309: USER_PROFILE → DELETE; state ABSENT (proof evidence_84); linked by batch-unique (activity_2544, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_3625: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_17; category SECURITY_AUDIT_LOG: resource type default; state from evidence_17 (captured after audit_at; not citable)
- integration_service/data_flow_8346: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_84); linked by identifier match in evidence_84; category DATA_FLOW: resource type default
- search_service/search_4894: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_84); linked by identifier match in evidence_84; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_4894 | REPORT_REMAINING_RECORD | PRESENT | evidence_84 |
| 2 | FINDING | integration_service | data_flow_8346 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_84 |
| 3 | REMEDIATION | integration_service | data_flow_8346 | DISABLE_DATA_FLOW | DISABLED |  |
| 4 | REMEDIATION | search_service | search_4894 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_5309 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_4894 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_3625 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | integration_service | data_flow_8346 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
