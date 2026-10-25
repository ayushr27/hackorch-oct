# case_207 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_205: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_5678: USER_PROFILE → DELETE; state ABSENT (proof evidence_20); linked by batch-delay-match (activity_2508, confidence 1.0); alternatives ['account_3685']; category USER_PROFILE: resource type default
- security_service/audit_record_3578: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_20); linked by identifier match in evidence_20; category SECURITY_AUDIT_LOG: resource type default
- backup_service/backup_6407: BACKUP_ARCHIVE → BLOCK; state ACTIVE (proof evidence_20); linked by identifier match in evidence_20; category BACKUP_ARCHIVE: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | backup_service | backup_6407 | REPORT_RESTORE_RISK | ACTIVE | evidence_20 |
| 2 | REMEDIATION | backup_service | backup_6407 | BLOCK_RESTORE | BLOCKED |  |
| 3 | VERIFICATION | account_service | account_5678 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | security_service | audit_record_3578 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 5 | VERIFICATION | backup_service | backup_6407 | VERIFY_RESTORE_BLOCKED | BLOCKED |  |
