# case_126 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'remov' (LLM agrees)
- subject user_124: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_8819: USER_PROFILE → DELETE; state ABSENT (proof evidence_87); linked by evidence (activity_3114, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_1402: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_87); linked by policy-delay-match via activity_3115; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_6884: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_87); linked by identifier match in evidence_87; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_8819 | VERIFY_RECORD_ABSENT | ABSENT | evidence_87 |
| 2 | VERIFICATION | security_service | audit_record_6884 | VERIFY_RECORD_PRESENT | PRESENT | evidence_87 |
| 3 | VERIFICATION | analytics_platform | analytics_1402 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_87 |
