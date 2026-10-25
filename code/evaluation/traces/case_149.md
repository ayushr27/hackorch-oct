# case_149 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_147: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_9505: USER_PROFILE → DELETE; state ABSENT (proof evidence_86); linked by batch-unique (activity_2904, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_5886: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_86); linked by identifier match in evidence_86; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- search_service/search_7672: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_86); linked by identifier match in evidence_86; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_7672 | REPORT_REMAINING_RECORD | PRESENT | evidence_86 |
| 2 | FINDING | analytics_platform | analytics_5886 | REPORT_EXPOSED_PII | PRESENT | evidence_86 |
| 3 | REMEDIATION | search_service | search_7672 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | analytics_platform | analytics_5886 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 5 | VERIFICATION | account_service | account_9505 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_7672 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | analytics_platform | analytics_5886 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
