# case_412 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_410: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_6443: USER_PROFILE → DELETE; state ABSENT (proof evidence_38); linked by batch-delay-match (activity_970, confidence 0.0); alternatives ['account_163', 'account_2775', 'account_8985', 'account_3492', 'account_2464']; category USER_PROFILE: resource type default
- security_service/audit_record_5637: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_38); linked by identifier match in evidence_38; category SECURITY_AUDIT_LOG: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_6443 | VERIFY_RECORD_ABSENT | ABSENT | evidence_38 |
| 2 | VERIFICATION | security_service | audit_record_5637 | VERIFY_RECORD_PRESENT | PRESENT | evidence_38 |
