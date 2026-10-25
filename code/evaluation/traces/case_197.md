# case_197 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_195: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_2952: USER_PROFILE → DELETE; state ABSENT (proof evidence_20); linked by batch-delay-match (activity_2428, confidence 1.0); category USER_PROFILE: resource type default; never observed; absence proven by evidence_20
- analytics_platform/analytics_6093: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_82); linked by identifier match in evidence_82; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- search_service/search_6762: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_82); linked by identifier match in evidence_82; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_6762 | REPORT_REMAINING_RECORD | PRESENT | evidence_82 |
| 2 | FINDING | analytics_platform | analytics_6093 | REPORT_EXPOSED_PII | PRESENT | evidence_82 |
| 3 | REMEDIATION | search_service | search_6762 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | analytics_platform | analytics_6093 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 5 | VERIFICATION | account_service | account_2952 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_6762 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | analytics_platform | analytics_6093 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
