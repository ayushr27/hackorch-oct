# case_446 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_444: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_3827: USER_PROFILE → DELETE; state ABSENT (proof evidence_66); linked by batch-unique (activity_721, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_195: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_66); linked by identifier match in evidence_66; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- analytics_platform/analytics_7270: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_66); linked by policy-delay-match(2 fits) via activity_724; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- integration_service/data_flow_1068: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_66); linked by identifier match in evidence_66; category DATA_FLOW: resource type default
- search_service/search_3780: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_66); linked by identifier match in evidence_66; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_9938: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_66); linked by identifier match in evidence_66; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_3780 | REPORT_REMAINING_RECORD | PRESENT | evidence_66 |
| 2 | FINDING | analytics_platform | analytics_195 | REPORT_EXPOSED_PII | PRESENT | evidence_66 |
| 3 | FINDING | support_platform | support_9938 | REPORT_EXPOSED_PII | PRESENT | evidence_66 |
| 4 | FINDING | integration_service | data_flow_1068 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_66 |
| 5 | REMEDIATION | integration_service | data_flow_1068 | DISABLE_DATA_FLOW | DISABLED |  |
| 6 | REMEDIATION | search_service | search_3780 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_9938 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_195 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_3827 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_3780 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | support_platform | support_9938 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 12 | VERIFICATION | analytics_platform | analytics_195 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
| 13 | VERIFICATION | analytics_platform | analytics_7270 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
| 14 | VERIFICATION | integration_service | data_flow_1068 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
