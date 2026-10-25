# case_175 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_173: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_246: USER_PROFILE → DELETE; state ABSENT (proof evidence_84); linked by evidence (activity_2642, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_9505: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_84); linked by policy-delay-match via activity_2644; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_7166: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_84); linked by identifier match in evidence_84; category SECURITY_AUDIT_LOG: resource type default
- backup_service/backup_549: BACKUP_ARCHIVE → BLOCK; state INACTIVE (proof evidence_84); linked by identifier match in evidence_84; category BACKUP_ARCHIVE: resource type default
- integration_service/data_flow_4319: DATA_FLOW → DISABLE; state INACTIVE (proof evidence_84); linked by identifier match in evidence_84; category DATA_FLOW: resource type default
- support_platform/support_8164: SUPPORT_MESSAGE → REDACT; state CLEAN (proof evidence_84); linked by identifier match in evidence_84; category SUPPORT_MESSAGE: stated by evidence_17

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_246 | VERIFY_RECORD_ABSENT | ABSENT | evidence_84 |
| 2 | VERIFICATION | security_service | audit_record_7166 | VERIFY_RECORD_PRESENT | PRESENT | evidence_84 |
| 3 | VERIFICATION | support_platform | support_8164 | VERIFY_RECORD_REDACTED | REDACTED | evidence_84 |
| 4 | VERIFICATION | analytics_platform | analytics_9505 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_84 |
| 5 | VERIFICATION | integration_service | data_flow_4319 | VERIFY_DATA_FLOW_DISABLED | DISABLED | evidence_84 |
| 6 | VERIFICATION | backup_service | backup_549 | VERIFY_RESTORE_BLOCKED | BLOCKED | evidence_84 |
