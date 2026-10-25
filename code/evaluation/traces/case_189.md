# case_189 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_187: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_5848: USER_PROFILE → DELETE; state PII (proof evidence_83); linked by evidence (activity_2637, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_1120: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_83); linked by identifier match in evidence_83; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- search_service/search_4334: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_83); linked by identifier match in evidence_83; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_8447: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_83); linked by identifier match in evidence_83; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | account_service | account_5848 | REPORT_REMAINING_RECORD | PRESENT | evidence_83 |
| 2 | FINDING | search_service | search_4334 | REPORT_REMAINING_RECORD | PRESENT | evidence_83 |
| 3 | FINDING | analytics_platform | analytics_1120 | REPORT_EXPOSED_PII | PRESENT | evidence_83 |
| 4 | FINDING | support_platform | support_8447 | REPORT_EXPOSED_PII | PRESENT | evidence_83 |
| 5 | REMEDIATION | account_service | account_5848 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | search_service | search_4334 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_8447 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_1120 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_5848 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_4334 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | support_platform | support_8447 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 12 | VERIFICATION | analytics_platform | analytics_1120 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
