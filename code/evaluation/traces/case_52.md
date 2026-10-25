# case_52 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'remov' (LLM agrees)
- subject user_18: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_2373: USER_PROFILE → DELETE; state ABSENT (proof evidence_78); linked by subject-linked (outside window) (evidence, confidence 0.6); category USER_PROFILE: resource type default; never observed; absence proven by evidence_78
- export_service/export_1260: USER_EXPORT → DELETE; state PII (proof evidence_23); linked by identifier match in evidence_23; category USER_EXPORT: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | export_service | export_1260 | REPORT_REMAINING_RECORD | PRESENT | evidence_23 |
| 2 | REMEDIATION | export_service | export_1260 | DELETE_RECORD | ABSENT |  |
| 3 | VERIFICATION | account_service | account_2373 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | export_service | export_1260 | VERIFY_RECORD_ABSENT | ABSENT |  |
