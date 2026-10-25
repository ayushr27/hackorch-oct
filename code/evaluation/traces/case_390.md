# case_390 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: '削除' (LLM agrees)
- subject user_388: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_7618: USER_PROFILE → DELETE; state ABSENT (proof evidence_36); linked by evidence (activity_1117, confidence 1.0); category USER_PROFILE: stated by evidence_36
- analytics_platform/analytics_448: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_36); linked by policy-delay-match via activity_1121; category ANALYTICS_PROFILE: stated by evidence_36
- security_service/audit_record_101: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_36); linked by identifier match in evidence_36; category SECURITY_AUDIT_LOG: stated by evidence_36
- backup_service/backup_5165: BACKUP_ARCHIVE → BLOCK; state INACTIVE (proof evidence_36); linked by identifier match in evidence_36; category BACKUP_ARCHIVE: stated by evidence_36
- integration_service/data_flow_5737: DATA_FLOW → DISABLE; state INACTIVE (proof evidence_36); linked by identifier match in evidence_36; category DATA_FLOW: resource type default
- legal_service/legal_hold_8049: LEGAL_HOLD_RECORD → RETAIN; state CLEAN (proof evidence_36); linked by identifier match in evidence_36; category LEGAL_HOLD_RECORD: stated by evidence_36
- support_platform/support_5720: SUPPORT_MESSAGE → REDACT; state CLEAN (proof evidence_36); linked by identifier match in evidence_36; category SUPPORT_MESSAGE: stated by evidence_36

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_7618 | VERIFY_RECORD_ABSENT | ABSENT | evidence_36 |
| 2 | VERIFICATION | legal_service | legal_hold_8049 | VERIFY_RECORD_PRESENT | PRESENT | evidence_36 |
| 3 | VERIFICATION | security_service | audit_record_101 | VERIFY_RECORD_PRESENT | PRESENT | evidence_36 |
| 4 | VERIFICATION | support_platform | support_5720 | VERIFY_RECORD_REDACTED | REDACTED | evidence_36 |
| 5 | VERIFICATION | analytics_platform | analytics_448 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_36 |
| 6 | VERIFICATION | integration_service | data_flow_5737 | VERIFY_DATA_FLOW_DISABLED | DISABLED | evidence_36 |
| 7 | VERIFICATION | backup_service | backup_5165 | VERIFY_RESTORE_BLOCKED | BLOCKED | evidence_36 |
