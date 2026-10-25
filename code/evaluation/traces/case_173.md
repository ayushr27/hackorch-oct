# case_173 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'remov' (LLM agrees)
- subject user_171: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_6554: USER_PROFILE → DELETE; state ABSENT (proof evidence_84); linked by batch-delay-match (activity_2641, confidence 1.0); alternatives ['account_796']; category USER_PROFILE: resource type default
- analytics_platform/analytics_6000: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_84); linked by identifier match in evidence_84; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_4126: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_17; category SECURITY_AUDIT_LOG: resource type default; state from evidence_17 (captured after audit_at; not citable)
- search_service/search_9523: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_84); linked by identifier match in evidence_84; category SEARCH_INDEX_ENTRY: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_9523 | REPORT_REMAINING_RECORD | PRESENT | evidence_84 |
| 2 | FINDING | analytics_platform | analytics_6000 | REPORT_EXPOSED_PII | PRESENT | evidence_84 |
| 3 | REMEDIATION | search_service | search_9523 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | analytics_platform | analytics_6000 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 5 | VERIFICATION | account_service | account_6554 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_9523 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_4126 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | analytics_platform | analytics_6000 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
