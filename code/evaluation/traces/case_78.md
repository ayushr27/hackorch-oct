# case_78 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: '削除' (LLM agrees)
- subject user_76: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_8754: USER_PROFILE → DELETE; state ABSENT (proof evidence_54); linked by batch-unique (activity_3302, confidence 0.95); category USER_PROFILE: resource type default; never observed; absence proven by evidence_54
- security_service/audit_record_6593: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_07; category SECURITY_AUDIT_LOG: resource type default; state from evidence_07 (captured after audit_at; not citable)
- search_service/search_8295: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_91); linked by identifier match in evidence_91; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_9652: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_91); linked by identifier match in evidence_91; category SUPPORT_MESSAGE: stated by evidence_07

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_8295 | REPORT_REMAINING_RECORD | PRESENT | evidence_91 |
| 2 | FINDING | support_platform | support_9652 | REPORT_EXPOSED_PII | PRESENT | evidence_91 |
| 3 | REMEDIATION | search_service | search_8295 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_9652 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_8754 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_8295 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_6593 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | support_platform | support_9652 | VERIFY_RECORD_REDACTED | REDACTED |  |
