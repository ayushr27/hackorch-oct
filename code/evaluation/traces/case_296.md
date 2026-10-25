# case_296 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_294: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_4267: USER_PROFILE → DELETE; state ABSENT (proof evidence_75); linked by batch-delay-match (activity_1668, confidence 1.0); alternatives ['account_4718']; category USER_PROFILE: resource type default
- integration_service/data_flow_085: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_75); linked by identifier match in evidence_75; category DATA_FLOW: resource type default
- search_service/search_9631: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_75); linked by identifier match in evidence_75; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_9631 | REPORT_REMAINING_RECORD | PRESENT | evidence_75 |
| 2 | FINDING | integration_service | data_flow_085 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_75 |
| 3 | REMEDIATION | integration_service | data_flow_085 | DISABLE_DATA_FLOW | DISABLED |  |
| 4 | REMEDIATION | search_service | search_9631 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_4267 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_9631 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | integration_service | data_flow_085 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
