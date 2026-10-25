# case_315 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_313: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_782: USER_PROFILE → DELETE; state ABSENT (proof evidence_74); linked by evidence (activity_1564, confidence 1.0); category USER_PROFILE: resource type default
- security_service/audit_record_2407: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_30; category SECURITY_AUDIT_LOG: resource type default; state from evidence_30 (captured after audit_at; not citable)
- backup_service/backup_7421: BACKUP_ARCHIVE → BLOCK; state ACTIVE (proof evidence_74); linked by identifier match in evidence_74; category BACKUP_ARCHIVE: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | backup_service | backup_7421 | REPORT_RESTORE_RISK | ACTIVE | evidence_74 |
| 2 | REMEDIATION | backup_service | backup_7421 | BLOCK_RESTORE | BLOCKED |  |
| 3 | VERIFICATION | account_service | account_782 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | security_service | audit_record_2407 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 5 | VERIFICATION | backup_service | backup_7421 | VERIFY_RESTORE_BLOCKED | BLOCKED |  |
