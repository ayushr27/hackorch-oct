# case_180 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_178: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_9876: USER_PROFILE → DELETE; state ABSENT (proof evidence_84); linked by batch-unique (activity_2545, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_1391: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_84); linked by identifier match in evidence_84; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_2207: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_17; category SECURITY_AUDIT_LOG: resource type default; state from evidence_17 (captured after audit_at; not citable)
- export_service/export_7156: USER_EXPORT → DELETE; state PII (proof evidence_84); linked by identifier match in evidence_84; category USER_EXPORT: resource type default
- search_service/search_5570: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_84); linked by identifier match in evidence_84; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_2609: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_84); linked by identifier match in evidence_84; category SUPPORT_MESSAGE: stated by evidence_17

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | export_service | export_7156 | REPORT_REMAINING_RECORD | PRESENT | evidence_84 |
| 2 | FINDING | search_service | search_5570 | REPORT_REMAINING_RECORD | PRESENT | evidence_84 |
| 3 | FINDING | analytics_platform | analytics_1391 | REPORT_EXPOSED_PII | PRESENT | evidence_84 |
| 4 | FINDING | support_platform | support_2609 | REPORT_EXPOSED_PII | PRESENT | evidence_84 |
| 5 | REMEDIATION | export_service | export_7156 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | search_service | search_5570 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_2609 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_1391 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_9876 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | export_service | export_7156 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | search_service | search_5570 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 12 | VERIFICATION | security_service | audit_record_2207 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 13 | VERIFICATION | support_platform | support_2609 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 14 | VERIFICATION | analytics_platform | analytics_1391 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
