# case_172 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_170: 1 email(s), 1 hash(es), 2 phone(s)
- account_service/account_5675: USER_PROFILE → DELETE; state ABSENT (proof -); linked by evidence (activity_2752, confidence 1.0); category USER_PROFILE: resource type default; state from evidence_16 (captured after audit_at; not citable)
- security_service/audit_record_6136: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_16; category SECURITY_AUDIT_LOG: resource type default; state from evidence_16 (captured after audit_at; not citable)
- search_service/search_7102: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_85); linked by identifier match in evidence_85; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_2322: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_85); linked by identifier match in evidence_85; category SUPPORT_MESSAGE: stated by evidence_16

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_7102 | REPORT_REMAINING_RECORD | PRESENT | evidence_85 |
| 2 | FINDING | support_platform | support_2322 | REPORT_EXPOSED_PII | PRESENT | evidence_85 |
| 3 | REMEDIATION | search_service | search_7102 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_2322 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_5675 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_7102 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_6136 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | support_platform | support_2322 | VERIFY_RECORD_REDACTED | REDACTED |  |
