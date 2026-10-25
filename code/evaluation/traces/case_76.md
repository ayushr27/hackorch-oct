# case_76 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'remov' (LLM agrees)
- subject user_74: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_925: USER_PROFILE → DELETE; state ABSENT (proof evidence_54); linked by batch-unique (activity_3355, confidence 0.95); category USER_PROFILE: resource type default; never observed; absence proven by evidence_54
- security_service/audit_record_6766: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_07; category SECURITY_AUDIT_LOG: resource type default; state from evidence_07 (captured after audit_at; not citable)
- support_platform/support_9746: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_91); linked by identifier match in evidence_91; category SUPPORT_MESSAGE: stated by evidence_07

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | support_platform | support_9746 | REPORT_EXPOSED_PII | PRESENT | evidence_91 |
| 2 | REMEDIATION | support_platform | support_9746 | REDACT_RECORD | REDACTED |  |
| 3 | VERIFICATION | account_service | account_925 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | security_service | audit_record_6766 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 5 | VERIFICATION | support_platform | support_9746 | VERIFY_RECORD_REDACTED | REDACTED |  |
