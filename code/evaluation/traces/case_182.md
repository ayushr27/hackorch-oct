# case_182 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_180: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_2322: USER_PROFILE → DELETE; state ABSENT (proof evidence_84); linked by batch-unique (activity_2818, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_1522: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_84); linked by identifier match in evidence_84; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_8354: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_17; category SECURITY_AUDIT_LOG: resource type default; state from evidence_17 (captured after audit_at; not citable)
- integration_service/data_flow_7450: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_84); linked by identifier match in evidence_84; category DATA_FLOW: resource type default
- search_service/search_2073: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_84); linked by identifier match in evidence_84; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_4806: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_84); linked by identifier match in evidence_84; category SUPPORT_MESSAGE: stated by evidence_17

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_2073 | REPORT_REMAINING_RECORD | PRESENT | evidence_84 |
| 2 | FINDING | analytics_platform | analytics_1522 | REPORT_EXPOSED_PII | PRESENT | evidence_84 |
| 3 | FINDING | support_platform | support_4806 | REPORT_EXPOSED_PII | PRESENT | evidence_84 |
| 4 | FINDING | integration_service | data_flow_7450 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_84 |
| 5 | REMEDIATION | integration_service | data_flow_7450 | DISABLE_DATA_FLOW | DISABLED |  |
| 6 | REMEDIATION | search_service | search_2073 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_4806 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_1522 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_2322 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_2073 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_8354 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_4806 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_1522 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
| 14 | VERIFICATION | integration_service | data_flow_7450 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
