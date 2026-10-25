# case_206 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_204: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_4522: USER_PROFILE → DELETE; state ABSENT (proof evidence_20); linked by batch-unique (activity_2510, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_9580: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_20); linked by policy-delay-match via activity_2512; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_9878: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_20); linked by identifier match in evidence_20; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_4522 | VERIFY_RECORD_ABSENT | ABSENT | evidence_20 |
| 2 | VERIFICATION | security_service | audit_record_9878 | VERIFY_RECORD_PRESENT | PRESENT | evidence_20 |
| 3 | VERIFICATION | analytics_platform | analytics_9580 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_20 |
