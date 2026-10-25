# case_497 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_495: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_5281: USER_PROFILE → DELETE; state ABSENT (proof evidence_63); linked by batch-delay-match (activity_228, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_6565: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_63); linked by policy-delay-match via activity_231; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_9796: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_63); linked by identifier match in evidence_63; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_5281 | VERIFY_RECORD_ABSENT | ABSENT | evidence_63 |
| 2 | VERIFICATION | security_service | audit_record_9796 | VERIFY_RECORD_PRESENT | PRESENT | evidence_63 |
| 3 | VERIFICATION | analytics_platform | analytics_6565 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_63 |
