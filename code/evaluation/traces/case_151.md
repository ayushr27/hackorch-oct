# case_151 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_149: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_874: USER_PROFILE → DELETE; state ABSENT (proof evidence_86); linked by batch-unique (activity_2901, confidence 0.95); category USER_PROFILE: resource type default
- analytics_platform/analytics_1626: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_86); linked by policy-delay-match via activity_2907; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_8905: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_86); linked by identifier match in evidence_86; category SECURITY_AUDIT_LOG: resource type default
- backup_service/backup_9557: BACKUP_ARCHIVE → BLOCK; state INACTIVE (proof evidence_86); linked by identifier match in evidence_86; category BACKUP_ARCHIVE: resource type default
- integration_service/data_flow_2437: DATA_FLOW → DISABLE; state INACTIVE (proof evidence_86); linked by identifier match in evidence_86; category DATA_FLOW: resource type default
- support_platform/support_5400: SUPPORT_MESSAGE → REDACT; state CLEAN (proof evidence_86); linked by identifier match in evidence_86; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_874 | VERIFY_RECORD_ABSENT | ABSENT | evidence_86 |
| 2 | VERIFICATION | security_service | audit_record_8905 | VERIFY_RECORD_PRESENT | PRESENT | evidence_86 |
| 3 | VERIFICATION | support_platform | support_5400 | VERIFY_RECORD_REDACTED | REDACTED | evidence_86 |
| 4 | VERIFICATION | analytics_platform | analytics_1626 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_86 |
| 5 | VERIFICATION | integration_service | data_flow_2437 | VERIFY_DATA_FLOW_DISABLED | DISABLED | evidence_86 |
| 6 | VERIFICATION | backup_service | backup_9557 | VERIFY_RESTORE_BLOCKED | BLOCKED | evidence_86 |
