# case_294 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_292: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_9091: USER_PROFILE → DELETE; state ABSENT (proof evidence_75); linked by batch-delay-match (activity_1720, confidence 0.0); alternatives ['account_6996', 'account_8353']; category USER_PROFILE: resource type default
- analytics_platform/analytics_7575: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_75); linked by policy-delay-match via activity_1726; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_4387: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_75); linked by identifier match in evidence_75; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_9091 | VERIFY_RECORD_ABSENT | ABSENT | evidence_75 |
| 2 | VERIFICATION | security_service | audit_record_4387 | VERIFY_RECORD_PRESENT | PRESENT | evidence_75 |
| 3 | VERIFICATION | analytics_platform | analytics_7575 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_75 |
