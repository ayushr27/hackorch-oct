# case_46 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_17: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_6523: USER_PROFILE → DELETE; state ABSENT (proof evidence_67); linked by evidence (activity_3850, confidence 1.0); category USER_PROFILE: resource type default
- identity_service/tombstone_17: ACCOUNT_TOMBSTONE → REDACT; state CLEAN (proof evidence_42); linked by identifier match in evidence_42; category ACCOUNT_TOMBSTONE: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_6523 | VERIFY_RECORD_ABSENT | ABSENT | evidence_67 |
| 2 | VERIFICATION | identity_service | tombstone_17 | VERIFY_RECORD_REDACTED | REDACTED | evidence_42 |
