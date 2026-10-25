# case_250 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_248: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_7010: USER_PROFILE → DELETE; state ABSENT (proof evidence_78); linked by batch-unique (activity_2197, confidence 0.95); category USER_PROFILE: resource type default
- search_service/search_3760: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_78); linked by identifier match in evidence_78; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_3760 | REPORT_REMAINING_RECORD | PRESENT | evidence_78 |
| 2 | REMEDIATION | search_service | search_3760 | DELETE_RECORD | ABSENT |  |
| 3 | VERIFICATION | account_service | account_7010 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | search_service | search_3760 | VERIFY_RECORD_ABSENT | ABSENT |  |
