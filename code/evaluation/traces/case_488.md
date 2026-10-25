# case_488 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_486: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_1433: USER_PROFILE → DELETE; state ABSENT (proof -); linked by evidence (activity_405, confidence 1.0); category USER_PROFILE: stated by evidence_45; state from evidence_45 (captured after audit_at; not citable)
- security_service/audit_record_6252: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_45; category SECURITY_AUDIT_LOG: stated by evidence_45; state from evidence_45 (captured after audit_at; not citable)
- integration_service/data_flow_3755: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_64); linked by identifier match in evidence_64; category DATA_FLOW: resource type default
- search_service/search_4216: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_64); linked by identifier match in evidence_64; category SEARCH_INDEX_ENTRY: stated by evidence_45

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_4216 | REPORT_REMAINING_RECORD | PRESENT | evidence_64 |
| 2 | FINDING | integration_service | data_flow_3755 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_64 |
| 3 | REMEDIATION | integration_service | data_flow_3755 | DISABLE_DATA_FLOW | DISABLED |  |
| 4 | REMEDIATION | search_service | search_4216 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_1433 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_4216 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_6252 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | integration_service | data_flow_3755 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
