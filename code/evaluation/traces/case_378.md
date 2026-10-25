# case_378 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: '삭제' (LLM agrees)
- subject user_376: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_976: USER_PROFILE → DELETE; state ABSENT (proof evidence_70); linked by evidence (activity_1079, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_3234: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_70); linked by policy-delay-match via activity_1081; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_7312: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_70); linked by identifier match in evidence_70; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_976 | VERIFY_RECORD_ABSENT | ABSENT | evidence_70 |
| 2 | VERIFICATION | security_service | audit_record_7312 | VERIFY_RECORD_PRESENT | PRESENT | evidence_70 |
| 3 | VERIFICATION | analytics_platform | analytics_3234 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_70 |
