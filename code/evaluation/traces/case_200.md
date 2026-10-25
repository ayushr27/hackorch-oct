# case_200 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_198: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_1964: USER_PROFILE → DELETE; state ABSENT (proof evidence_20); linked by batch-unique (activity_2387, confidence 0.95); category USER_PROFILE: resource type default; never observed; absence proven by evidence_20
- integration_service/data_flow_2310: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_82); linked by identifier match in evidence_82; category DATA_FLOW: resource type default
- search_service/search_7472: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_82); linked by identifier match in evidence_82; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_7472 | REPORT_REMAINING_RECORD | PRESENT | evidence_82 |
| 2 | FINDING | integration_service | data_flow_2310 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_82 |
| 3 | REMEDIATION | integration_service | data_flow_2310 | DISABLE_DATA_FLOW | DISABLED |  |
| 4 | REMEDIATION | search_service | search_7472 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_1964 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_7472 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | integration_service | data_flow_2310 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
