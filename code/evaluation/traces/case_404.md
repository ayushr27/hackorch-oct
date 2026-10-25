# case_404 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_402: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_1759: USER_PROFILE → DELETE; state ABSENT (proof evidence_38); linked by batch-delay-match (activity_1047, confidence 0.938); alternatives ['account_8997']; category USER_PROFILE: resource type default
- analytics_platform/analytics_1792: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_38); linked by identifier match in evidence_38; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_6099: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_38); linked by identifier match in evidence_38; category SECURITY_AUDIT_LOG: resource type default
- integration_service/data_flow_8093: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_38); linked by identifier match in evidence_38; category DATA_FLOW: resource type default
- search_service/search_7022: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_38); linked by identifier match in evidence_38; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_880: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_38); linked by identifier match in evidence_38; category SUPPORT_MESSAGE: stated by evidence_38

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_7022 | REPORT_REMAINING_RECORD | PRESENT | evidence_38 |
| 2 | FINDING | analytics_platform | analytics_1792 | REPORT_EXPOSED_PII | PRESENT | evidence_38 |
| 3 | FINDING | support_platform | support_880 | REPORT_EXPOSED_PII | PRESENT | evidence_38 |
| 4 | FINDING | integration_service | data_flow_8093 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_38 |
| 5 | REMEDIATION | integration_service | data_flow_8093 | DISABLE_DATA_FLOW | DISABLED |  |
| 6 | REMEDIATION | search_service | search_7022 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_880 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_1792 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_1759 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_7022 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_6099 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_880 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_1792 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
| 14 | VERIFICATION | integration_service | data_flow_8093 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
