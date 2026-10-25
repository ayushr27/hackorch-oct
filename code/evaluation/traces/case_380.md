# case_380 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_378: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_4001: USER_PROFILE → DELETE; state ABSENT (proof evidence_70); linked by evidence (activity_1032, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_9326: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_70); linked by policy-delay-match via activity_1033; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_4489: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_70); linked by identifier match in evidence_70; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_4001 | VERIFY_RECORD_ABSENT | ABSENT | evidence_70 |
| 2 | VERIFICATION | security_service | audit_record_4489 | VERIFY_RECORD_PRESENT | PRESENT | evidence_70 |
| 3 | VERIFICATION | analytics_platform | analytics_9326 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_70 |
