# case_528 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_526: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_1184: USER_PROFILE → DELETE; state ABSENT (proof evidence_62); linked by batch-unique (activity_132, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_8476: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_62); linked by identifier match in evidence_62; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_2284: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_49; category SECURITY_AUDIT_LOG: resource type default; state from evidence_49 (captured after audit_at; not citable)
- export_service/export_9388: USER_EXPORT → DELETE; state PII (proof evidence_62); linked by identifier match in evidence_62; category USER_EXPORT: resource type default
- search_service/search_1429: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_62); linked by identifier match in evidence_62; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_193: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_62); linked by identifier match in evidence_62; category SUPPORT_MESSAGE: stated by evidence_49

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | export_service | export_9388 | REPORT_REMAINING_RECORD | PRESENT | evidence_62 |
| 2 | FINDING | search_service | search_1429 | REPORT_REMAINING_RECORD | PRESENT | evidence_62 |
| 3 | FINDING | analytics_platform | analytics_8476 | REPORT_EXPOSED_PII | PRESENT | evidence_62 |
| 4 | FINDING | support_platform | support_193 | REPORT_EXPOSED_PII | PRESENT | evidence_62 |
| 5 | REMEDIATION | export_service | export_9388 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | search_service | search_1429 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_193 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_8476 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_1184 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | export_service | export_9388 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | search_service | search_1429 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 12 | VERIFICATION | security_service | audit_record_2284 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 13 | VERIFICATION | support_platform | support_193 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 14 | VERIFICATION | analytics_platform | analytics_8476 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
