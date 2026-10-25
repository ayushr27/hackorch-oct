# case_123 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'suppression' (LLM agrees)
- subject user_121: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_2988: USER_PROFILE → DELETE; state ABSENT (proof evidence_87); linked by batch-unique (activity_3165, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_5645: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_12; category SECURITY_AUDIT_LOG: resource type default; state from evidence_12 (captured after audit_at; not citable)
- backup_service/backup_8742: BACKUP_ARCHIVE → BLOCK; state ACTIVE (proof evidence_87); linked by identifier match in evidence_87; category BACKUP_ARCHIVE: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | backup_service | backup_8742 | REPORT_RESTORE_RISK | ACTIVE | evidence_87 |
| 2 | REMEDIATION | backup_service | backup_8742 | BLOCK_RESTORE | BLOCKED |  |
| 3 | VERIFICATION | account_service | account_2988 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | security_service | audit_record_5645 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 5 | VERIFICATION | backup_service | backup_8742 | VERIFY_RESTORE_BLOCKED | BLOCKED |  |
