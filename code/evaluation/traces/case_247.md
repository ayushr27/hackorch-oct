# case_247 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_245: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_2981: USER_PROFILE → DELETE; state PII (proof evidence_78); linked by evidence (activity_2236, confidence 1.0); category USER_PROFILE: resource type default
- search_service/search_9473: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_78); linked by identifier match in evidence_78; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | account_service | account_2981 | REPORT_REMAINING_RECORD | PRESENT | evidence_78 |
| 2 | FINDING | search_service | search_9473 | REPORT_REMAINING_RECORD | PRESENT | evidence_78 |
| 3 | REMEDIATION | account_service | account_2981 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | search_service | search_9473 | DELETE_RECORD | ABSENT |  |
| 5 | VERIFICATION | account_service | account_2981 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_9473 | VERIFY_RECORD_ABSENT | ABSENT |  |
