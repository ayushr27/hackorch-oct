# case_365 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_363: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_3016: USER_PROFILE → DELETE; state ABSENT (proof evidence_34); linked by evidence (activity_1309, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_547: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_34); linked by identifier match in evidence_34; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_5798: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_34); linked by identifier match in evidence_34; category SECURITY_AUDIT_LOG: resource type default
- integration_service/data_flow_1021: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_34); linked by identifier match in evidence_34; category DATA_FLOW: resource type default
- search_service/search_6311: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_34); linked by identifier match in evidence_34; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_3294: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_34); linked by identifier match in evidence_34; category SUPPORT_MESSAGE: stated by evidence_34

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_6311 | REPORT_REMAINING_RECORD | PRESENT | evidence_34 |
| 2 | FINDING | analytics_platform | analytics_547 | REPORT_EXPOSED_PII | PRESENT | evidence_34 |
| 3 | FINDING | support_platform | support_3294 | REPORT_EXPOSED_PII | PRESENT | evidence_34 |
| 4 | FINDING | integration_service | data_flow_1021 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_34 |
| 5 | REMEDIATION | integration_service | data_flow_1021 | DISABLE_DATA_FLOW | DISABLED |  |
| 6 | REMEDIATION | search_service | search_6311 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_3294 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_547 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_3016 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_6311 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_5798 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_3294 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_547 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
| 14 | VERIFICATION | integration_service | data_flow_1021 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
