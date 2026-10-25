# case_394 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_392: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_2191: USER_PROFILE → DELETE; state ABSENT (proof evidence_69); linked by batch-delay-match (activity_1006, confidence 0.0); alternatives ['account_5754', 'account_7174']; category USER_PROFILE: resource type default
- search_service/search_195: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_69); linked by identifier match in evidence_69; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_195 | REPORT_REMAINING_RECORD | PRESENT | evidence_69 |
| 2 | REMEDIATION | search_service | search_195 | DELETE_RECORD | ABSENT |  |
| 3 | VERIFICATION | account_service | account_2191 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | search_service | search_195 | VERIFY_RECORD_ABSENT | ABSENT |  |
