# case_157 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_155: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_2154: USER_PROFILE → DELETE; state ABSENT (proof evidence_15); linked by batch-delay-match (activity_2757, confidence 1.0); alternatives ['account_1992']; category USER_PROFILE: resource type default
- analytics_platform/analytics_8425: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_15); linked by policy-delay-match via activity_2759; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_8821: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_15); linked by identifier match in evidence_15; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_2154 | VERIFY_RECORD_ABSENT | ABSENT | evidence_15 |
| 2 | VERIFICATION | security_service | audit_record_8821 | VERIFY_RECORD_PRESENT | PRESENT | evidence_15 |
| 3 | VERIFICATION | analytics_platform | analytics_8425 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_15 |
