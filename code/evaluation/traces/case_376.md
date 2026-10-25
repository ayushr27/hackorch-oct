# case_376 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_374: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_5454: USER_PROFILE → DELETE; state ABSENT (proof evidence_38); linked by batch-unique (activity_1110, confidence 0.95); category USER_PROFILE: resource type default; never observed; absence proven by evidence_38
- security_service/audit_record_4137: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_35; category SECURITY_AUDIT_LOG: resource type default; state from evidence_35 (captured after audit_at; not citable)
- search_service/search_3126: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_70); linked by identifier match in evidence_70; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_475: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_70); linked by identifier match in evidence_70; category SUPPORT_MESSAGE: stated by evidence_35

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_3126 | REPORT_REMAINING_RECORD | PRESENT | evidence_70 |
| 2 | FINDING | support_platform | support_475 | REPORT_EXPOSED_PII | PRESENT | evidence_70 |
| 3 | REMEDIATION | search_service | search_3126 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_475 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_5454 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_3126 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_4137 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | support_platform | support_475 | VERIFY_RECORD_REDACTED | REDACTED |  |
