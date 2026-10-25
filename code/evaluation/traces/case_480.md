# case_480 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_478: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_2465: USER_PROFILE → DELETE; state ABSENT (proof evidence_45); linked by batch-delay-match (activity_315, confidence 1.0); alternatives ['account_9449']; category USER_PROFILE: resource type default
- analytics_platform/analytics_1794: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_45); linked by policy-delay-match via activity_319; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_7742: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_45); linked by identifier match in evidence_45; category SECURITY_AUDIT_LOG: resource type default
- backup_service/backup_7706: BACKUP_ARCHIVE → BLOCK; state INACTIVE (proof evidence_45); linked by identifier match in evidence_45; category BACKUP_ARCHIVE: resource type default
- integration_service/data_flow_2893: DATA_FLOW → DISABLE; state INACTIVE (proof evidence_45); linked by identifier match in evidence_45; category DATA_FLOW: resource type default
- support_platform/support_5854: SUPPORT_MESSAGE → REDACT; state CLEAN (proof evidence_45); linked by identifier match in evidence_45; category SUPPORT_MESSAGE: stated by evidence_45

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_2465 | VERIFY_RECORD_ABSENT | ABSENT | evidence_45 |
| 2 | VERIFICATION | security_service | audit_record_7742 | VERIFY_RECORD_PRESENT | PRESENT | evidence_45 |
| 3 | VERIFICATION | support_platform | support_5854 | VERIFY_RECORD_REDACTED | REDACTED | evidence_45 |
| 4 | VERIFICATION | analytics_platform | analytics_1794 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_45 |
| 5 | VERIFICATION | integration_service | data_flow_2893 | VERIFY_DATA_FLOW_DISABLED | DISABLED | evidence_45 |
| 6 | VERIFICATION | backup_service | backup_7706 | VERIFY_RESTORE_BLOCKED | BLOCKED | evidence_45 |
