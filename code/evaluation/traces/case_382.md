# case_382 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_380: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_2041: USER_PROFILE → DELETE; state ABSENT (proof evidence_38); linked by batch-unique (activity_1308, confidence 0.95); category USER_PROFILE: resource type default; never observed; absence proven by evidence_38
- analytics_platform/analytics_9918: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_70); linked by identifier match in evidence_70; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_6238: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_35; category SECURITY_AUDIT_LOG: resource type default; state from evidence_35 (captured after audit_at; not citable)
- integration_service/data_flow_6090: DATA_FLOW → DISABLE; state ACTIVE (proof evidence_70); linked by identifier match in evidence_70; category DATA_FLOW: resource type default
- search_service/search_8171: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_70); linked by identifier match in evidence_70; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_5071: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_70); linked by identifier match in evidence_70; category SUPPORT_MESSAGE: stated by evidence_35

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_8171 | REPORT_REMAINING_RECORD | PRESENT | evidence_70 |
| 2 | FINDING | analytics_platform | analytics_9918 | REPORT_EXPOSED_PII | PRESENT | evidence_70 |
| 3 | FINDING | support_platform | support_5071 | REPORT_EXPOSED_PII | PRESENT | evidence_70 |
| 4 | FINDING | integration_service | data_flow_6090 | REPORT_ACTIVE_DATA_FLOW | ACTIVE | evidence_70 |
| 5 | REMEDIATION | integration_service | data_flow_6090 | DISABLE_DATA_FLOW | DISABLED |  |
| 6 | REMEDIATION | search_service | search_8171 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_5071 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_9918 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_2041 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_8171 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_6238 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_5071 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_9918 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
| 14 | VERIFICATION | integration_service | data_flow_6090 | VERIFY_DATA_FLOW_DISABLED | DISABLED |  |
