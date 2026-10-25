# case_367 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_365: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_3204: USER_PROFILE → DELETE; state PII (proof evidence_34); linked by evidence (activity_1310, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_946: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_34); linked by identifier match in evidence_34; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_9082: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_34); linked by identifier match in evidence_34; category SECURITY_AUDIT_LOG: resource type default
- search_service/search_9950: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_34); linked by identifier match in evidence_34; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_4691: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_34); linked by identifier match in evidence_34; category SUPPORT_MESSAGE: stated by evidence_34

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | account_service | account_3204 | REPORT_REMAINING_RECORD | PRESENT | evidence_34 |
| 2 | FINDING | search_service | search_9950 | REPORT_REMAINING_RECORD | PRESENT | evidence_34 |
| 3 | FINDING | analytics_platform | analytics_946 | REPORT_EXPOSED_PII | PRESENT | evidence_34 |
| 4 | FINDING | support_platform | support_4691 | REPORT_EXPOSED_PII | PRESENT | evidence_34 |
| 5 | REMEDIATION | account_service | account_3204 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | search_service | search_9950 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_4691 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_946 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_3204 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_9950 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_9082 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_4691 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_946 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
