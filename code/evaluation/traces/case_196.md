# case_196 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_194: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_5599: USER_PROFILE → DELETE; state ABSENT (proof evidence_82); linked by evidence (activity_2472, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_5166: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_82); linked by policy-delay-match via activity_2475; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_6389: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_82); linked by identifier match in evidence_82; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_5599 | VERIFY_RECORD_ABSENT | ABSENT | evidence_82 |
| 2 | VERIFICATION | security_service | audit_record_6389 | VERIFY_RECORD_PRESENT | PRESENT | evidence_82 |
| 3 | VERIFICATION | analytics_platform | analytics_5166 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_82 |
