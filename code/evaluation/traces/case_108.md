# case_108 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eliminación' (LLM agrees)
- subject user_106: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_6750: USER_PROFILE → DELETE; state ABSENT (proof evidence_10); linked by batch-unique (activity_3239, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_5001: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_10); linked by policy-delay-match via activity_3243; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_1469: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_10); linked by identifier match in evidence_10; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_6750 | VERIFY_RECORD_ABSENT | ABSENT | evidence_10 |
| 2 | VERIFICATION | security_service | audit_record_1469 | VERIFY_RECORD_PRESENT | PRESENT | evidence_10 |
| 3 | VERIFICATION | analytics_platform | analytics_5001 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_10 |
