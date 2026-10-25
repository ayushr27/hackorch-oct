# case_500 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'remov' (LLM agrees)
- subject user_498: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_5738: USER_PROFILE → DELETE; state ABSENT (proof evidence_63); linked by batch-unique (activity_173, confidence 0.95); category USER_PROFILE: resource type default
- integration_service/data_flow_006: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_63); linked by identifier match in evidence_63; category DATA_FLOW: resource type default
- search_service/search_6092: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_63); linked by identifier match in evidence_63; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_6092 | REPORT_REMAINING_RECORD | PRESENT | evidence_63 |
| 2 | FINDING | integration_service | data_flow_006 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_63 |
| 3 | REMEDIATION | integration_service | data_flow_006 | DISABLE_DATA_FLOW | DISABLED |  |
| 4 | REMEDIATION | search_service | search_6092 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_5738 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_6092 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | integration_service | data_flow_006 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
