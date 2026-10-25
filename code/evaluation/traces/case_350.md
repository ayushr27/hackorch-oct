# case_350 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_348: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_5202: USER_PROFILE → DELETE; state ABSENT (proof evidence_71); linked by batch-unique (activity_1398, confidence 0.95); category USER_PROFILE: resource type default
- integration_service/data_flow_9775: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_71); linked by identifier match in evidence_71; category DATA_FLOW: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | integration_service | data_flow_9775 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_71 |
| 2 | REMEDIATION | integration_service | data_flow_9775 | DISABLE_DATA_FLOW | DISABLED |  |
| 3 | VERIFICATION | account_service | account_5202 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | integration_service | data_flow_9775 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
