# case_326 — COMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_324: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_3785: USER_PROFILE → DELETE; state ABSENT (proof evidence_73); linked by evidence (activity_1593, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_2072: ANALYTICS_PROFILE → ANONYMIZE; state CLEAN (proof evidence_73); linked by policy-delay-match via activity_1597; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_1219: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_73); linked by identifier match in evidence_73; category SECURITY_AUDIT_LOG: resource type default
- backup_service/backup_2894: BACKUP_ARCHIVE → BLOCK; state INACTIVE (proof evidence_73); linked by identifier match in evidence_73; category BACKUP_ARCHIVE: resource type default
- integration_service/data_flow_2468: DATA_FLOW → DISABLE; state INACTIVE (proof evidence_73); linked by identifier match in evidence_73; category DATA_FLOW: resource type default
- support_platform/support_305: SUPPORT_MESSAGE → REDACT; state CLEAN (proof evidence_73); linked by identifier match in evidence_73; category SUPPORT_MESSAGE: stated by evidence_31

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | VERIFICATION | account_service | account_3785 | VERIFY_RECORD_ABSENT | ABSENT | evidence_73 |
| 2 | VERIFICATION | security_service | audit_record_1219 | VERIFY_RECORD_PRESENT | PRESENT | evidence_73 |
| 3 | VERIFICATION | support_platform | support_305 | VERIFY_RECORD_REDACTED | REDACTED | evidence_73 |
| 4 | VERIFICATION | analytics_platform | analytics_2072 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED | evidence_73 |
| 5 | VERIFICATION | integration_service | data_flow_2468 | VERIFY_DATA_FLOW_DISABLED | DISABLED | evidence_73 |
| 6 | VERIFICATION | backup_service | backup_2894 | VERIFY_RESTORE_BLOCKED | BLOCKED | evidence_73 |
