# case_398 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_396: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_1140: USER_PROFILE → DELETE; state ABSENT (proof evidence_69); linked by batch-delay-match (activity_939, confidence 0.999); alternatives ['account_2138']; category USER_PROFILE: resource type default
- analytics_platform/analytics_4455: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_69); linked by policy-delay-match via activity_941; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_7361: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_69); linked by identifier match in evidence_69; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_1140 | VERIFY_RECORD_ABSENT | ABSENT | evidence_69 |
| 2 | VERIFICATION | security_service | audit_record_7361 | VERIFY_RECORD_PRESENT | PRESENT | evidence_69 |
| 3 | VERIFICATION | analytics_platform | analytics_4455 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_69 |
