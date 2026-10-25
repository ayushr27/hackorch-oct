# case_386 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_384: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_807: USER_PROFILE → DELETE; state ABSENT (proof evidence_36); linked by evidence (activity_1162, confidence 1.0); category USER_PROFILE: stated by evidence_36
- analytics_platform/analytics_4420: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_36); linked by identifier match in evidence_36; category ANALYTICS_PROFILE: stated by evidence_36
- security_service/audit_record_8245: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_36); linked by identifier match in evidence_36; category SECURITY_AUDIT_LOG: stated by evidence_36
- integration_service/data_flow_7623: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_36); linked by identifier match in evidence_36; category DATA_FLOW: resource type default
- search_service/search_3630: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_36); linked by identifier match in evidence_36; category SEARCH_INDEX_ENTRY: stated by evidence_36
- support_platform/support_1693: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_36); linked by identifier match in evidence_36; category SUPPORT_MESSAGE: stated by evidence_36

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_3630 | REPORT_REMAINING_RECORD | PRESENT | evidence_36 |
| 2 | FINDING | analytics_platform | analytics_4420 | REPORT_EXPOSED_PII | PRESENT | evidence_36 |
| 3 | FINDING | support_platform | support_1693 | REPORT_EXPOSED_PII | PRESENT | evidence_36 |
| 4 | FINDING | integration_service | data_flow_7623 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_36 |
| 5 | REMEDIATION | integration_service | data_flow_7623 | DISABLE_DATA_FLOW | DISABLED |  |
| 6 | REMEDIATION | search_service | search_3630 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_1693 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_4420 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_807 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_3630 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_8245 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_1693 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_4420 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
| 14 | VERIFICATION | integration_service | data_flow_7623 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
