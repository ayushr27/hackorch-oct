# case_544 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_544: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_7320: USER_PROFILE → DELETE; state ABSENT (proof evidence_52); linked by batch-delay-match (activity_3720, confidence 1.0); alternatives ['account_8931']; category USER_PROFILE: resource type default
- security_service/audit_record_1037: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_52); linked by identifier match in evidence_52; category SECURITY_AUDIT_LOG: resource type default
- identity_service/tombstone_8648: ACCOUNT_TOMBSTONE → REDACT; state PII (proof evidence_52); linked by identifier match in evidence_52; category ACCOUNT_TOMBSTONE: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | identity_service | tombstone_8648 | REPORT_EXPOSED_PII | PRESENT | evidence_52 |
| 2 | REMEDIATION | identity_service | tombstone_8648 | REDACT_RECORD | REDACTED |  |
| 3 | VERIFICATION | account_service | account_7320 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | security_service | audit_record_1037 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 5 | VERIFICATION | identity_service | tombstone_8648 | VERIFY_RECORD_REDACTED | REDACTED |  |
