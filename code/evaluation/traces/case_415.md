# case_415 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_413: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_9975: USER_PROFILE → DELETE; state PII (proof evidence_39); linked by evidence (activity_851, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_2102: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_39); linked by identifier match in evidence_39; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_6154: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_39); linked by identifier match in evidence_39; category SECURITY_AUDIT_LOG: resource type default
- search_service/search_3864: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_39); linked by identifier match in evidence_39; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_1993: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_39); linked by identifier match in evidence_39; category SUPPORT_MESSAGE: stated by evidence_39

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | account_service | account_9975 | REPORT_REMAINING_RECORD | PRESENT | evidence_39 |
| 2 | FINDING | search_service | search_3864 | REPORT_REMAINING_RECORD | PRESENT | evidence_39 |
| 3 | FINDING | analytics_platform | analytics_2102 | REPORT_EXPOSED_PII | PRESENT | evidence_39 |
| 4 | FINDING | support_platform | support_1993 | REPORT_EXPOSED_PII | PRESENT | evidence_39 |
| 5 | REMEDIATION | account_service | account_9975 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | search_service | search_3864 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_1993 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_2102 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_9975 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_3864 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_6154 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_1993 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_2102 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
