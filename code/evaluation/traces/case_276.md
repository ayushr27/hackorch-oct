# case_276 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_274: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_4853: USER_PROFILE → DELETE; state ABSENT (proof evidence_77); linked by batch-unique (activity_1851, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_5923: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_77); linked by policy-delay-match via activity_1852; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_8323: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_77); linked by identifier match in evidence_77; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_4853 | VERIFY_RECORD_ABSENT | ABSENT | evidence_77 |
| 2 | VERIFICATION | security_service | audit_record_8323 | VERIFY_RECORD_PRESENT | PRESENT | evidence_77 |
| 3 | VERIFICATION | analytics_platform | analytics_5923 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_77 |
