# case_125 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'remov' (LLM agrees)
- subject user_123: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_7637: USER_PROFILE → DELETE; state ABSENT (proof evidence_87); linked by batch-unique (activity_3112, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_1103: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_87); linked by identifier match in evidence_87; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_023: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_12; category SECURITY_AUDIT_LOG: resource type default; state from evidence_12 (captured after audit_at; not citable)
- search_service/search_9752: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_87); linked by identifier match in evidence_87; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_9752 | REPORT_REMAINING_RECORD | PRESENT | evidence_87 |
| 2 | FINDING | analytics_platform | analytics_1103 | REPORT_EXPOSED_PII | PRESENT | evidence_87 |
| 3 | REMEDIATION | search_service | search_9752 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | analytics_platform | analytics_1103 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 5 | VERIFICATION | account_service | account_7637 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_9752 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_023 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | analytics_platform | analytics_1103 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
