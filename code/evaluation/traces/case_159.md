# case_159 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_157: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_4272: USER_PROFILE → DELETE; state ABSENT (proof evidence_15); linked by batch-unique (activity_2710, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_8742: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_15); linked by identifier match in evidence_15; category SECURITY_AUDIT_LOG: resource type default
- backup_service/backup_1214: BACKUP_ARCHIVE → BLOCK; state ACTIVE (proof evidence_15); linked by identifier match in evidence_15; category BACKUP_ARCHIVE: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | backup_service | backup_1214 | REPORT_RESTORE_RISK | ACTIVE | evidence_15 |
| 2 | REMEDIATION | backup_service | backup_1214 | BLOCK_RESTORE | BLOCKED |  |
| 3 | VERIFICATION | account_service | account_4272 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | security_service | audit_record_8742 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 5 | VERIFICATION | backup_service | backup_1214 | VERIFY_RESTORE_BLOCKED | BLOCKED |  |
