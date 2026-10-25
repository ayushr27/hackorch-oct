# case_532 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'remov' (LLM agrees)
- subject user_530: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_470: USER_PROFILE → DELETE; state ABSENT (proof evidence_62); linked by batch-unique (activity_91, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_3744: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_62); linked by policy-delay-match via activity_92; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_4828: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_62); linked by identifier match in evidence_62; category SECURITY_AUDIT_LOG: resource type default
- backup_service/backup_6344: BACKUP_ARCHIVE → BLOCK; state INACTIVE (proof evidence_62); linked by identifier match in evidence_62; category BACKUP_ARCHIVE: resource type default
- integration_service/data_flow_6987: DATA_FLOW → DISABLE; state INACTIVE (proof evidence_62); linked by identifier match in evidence_62; category DATA_FLOW: resource type default
- support_platform/support_7724: SUPPORT_MESSAGE → REDACT; state CLEAN (proof evidence_62); linked by identifier match in evidence_62; category SUPPORT_MESSAGE: stated by evidence_49

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_470 | VERIFY_RECORD_ABSENT | ABSENT | evidence_62 |
| 2 | VERIFICATION | security_service | audit_record_4828 | VERIFY_RECORD_PRESENT | PRESENT | evidence_62 |
| 3 | VERIFICATION | support_platform | support_7724 | VERIFY_RECORD_REDACTED | REDACTED | evidence_62 |
| 4 | VERIFICATION | analytics_platform | analytics_3744 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_62 |
| 5 | VERIFICATION | integration_service | data_flow_6987 | VERIFY_DATA_FLOW_DISABLED | DISABLED | evidence_62 |
| 6 | VERIFICATION | backup_service | backup_6344 | VERIFY_RESTORE_BLOCKED | BLOCKED | evidence_62 |
