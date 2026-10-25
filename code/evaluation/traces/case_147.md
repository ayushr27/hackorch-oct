# case_147 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eliminación' (LLM agrees)
- subject user_145: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_8632: USER_PROFILE → DELETE; state ABSENT (proof evidence_86); linked by batch-delay-match (activity_2947, confidence 1.0); alternatives ['account_5023', 'account_7864']; category USER_PROFILE: resource type default
- backup_service/backup_4244: BACKUP_ARCHIVE → BLOCK; state ACTIVE (proof evidence_86); linked by identifier match in evidence_86; category BACKUP_ARCHIVE: resource type default

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | backup_service | backup_4244 | REPORT_RESTORE_RISK | ACTIVE | evidence_86 |
| 2 | REMEDIATION | backup_service | backup_4244 | BLOCK_RESTORE | BLOCKED |  |
| 3 | VERIFICATION | account_service | account_8632 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | backup_service | backup_4244 | VERIFY_RESTORE_BLOCKED | BLOCKED |  |
