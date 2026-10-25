# case_192 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_190: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_6608: USER_PROFILE → DELETE; state ABSENT (proof evidence_83); linked by batch-delay-match (activity_2591, confidence 1.0); alternatives ['account_9317']; category USER_PROFILE: resource type default
- analytics_platform/analytics_4472: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_83); linked by identifier match in evidence_83; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- export_service/export_2705: USER_EXPORT → DELETE; state PII (proof evidence_83); linked by identifier match in evidence_83; category USER_EXPORT: resource type default
- search_service/search_6680: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_83); linked by identifier match in evidence_83; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_5493: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_83); linked by identifier match in evidence_83; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | export_service | export_2705 | REPORT_REMAINING_RECORD | PRESENT | evidence_83 |
| 2 | FINDING | search_service | search_6680 | REPORT_REMAINING_RECORD | PRESENT | evidence_83 |
| 3 | FINDING | analytics_platform | analytics_4472 | REPORT_EXPOSED_PII | PRESENT | evidence_83 |
| 4 | FINDING | support_platform | support_5493 | REPORT_EXPOSED_PII | PRESENT | evidence_83 |
| 5 | REMEDIATION | export_service | export_2705 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | search_service | search_6680 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_5493 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_4472 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_6608 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | export_service | export_2705 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | search_service | search_6680 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 12 | VERIFICATION | support_platform | support_5493 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_4472 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
