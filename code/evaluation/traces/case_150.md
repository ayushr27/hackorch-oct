# case_150 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_148: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_3897: USER_PROFILE → DELETE; state ABSENT (proof evidence_86); linked by batch-unique (activity_2903, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_7254: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_86); linked by policy-delay-match via activity_2906; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_1584: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_86); linked by identifier match in evidence_86; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_3897 | VERIFY_RECORD_ABSENT | ABSENT | evidence_86 |
| 2 | VERIFICATION | security_service | audit_record_1584 | VERIFY_RECORD_PRESENT | PRESENT | evidence_86 |
| 3 | VERIFICATION | analytics_platform | analytics_7254 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_86 |
