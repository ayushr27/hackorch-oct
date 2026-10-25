# case_407 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_405: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_9087: USER_PROFILE → DELETE; state ABSENT (proof evidence_38); linked by batch-unique (activity_999, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_1922: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_38); linked by identifier match in evidence_38; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_6152: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_38); linked by identifier match in evidence_38; category SECURITY_AUDIT_LOG: resource type default
- search_service/search_5146: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_38); linked by identifier match in evidence_38; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_3802: SUPPORT_ATTACHMENT → DELETE; state PII (proof evidence_38); linked by identifier match in evidence_38; category SUPPORT_ATTACHMENT: stated by evidence_38
- support_platform/support_6569: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_38); linked by identifier match in evidence_38; category SUPPORT_MESSAGE: stated by evidence_38

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_5146 | REPORT_REMAINING_RECORD | PRESENT | evidence_38 |
| 2 | FINDING | support_platform | support_3802 | REPORT_REMAINING_RECORD | PRESENT | evidence_38 |
| 3 | FINDING | analytics_platform | analytics_1922 | REPORT_EXPOSED_PII | PRESENT | evidence_38 |
| 4 | FINDING | support_platform | support_6569 | REPORT_EXPOSED_PII | PRESENT | evidence_38 |
| 5 | REMEDIATION | search_service | search_5146 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | support_platform | support_3802 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_6569 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_1922 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_9087 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_5146 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | support_platform | support_3802 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 12 | VERIFICATION | security_service | audit_record_6152 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 13 | VERIFICATION | support_platform | support_6569 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 14 | VERIFICATION | analytics_platform | analytics_1922 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
