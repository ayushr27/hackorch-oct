# case_174 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_172: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_6659: USER_PROFILE → DELETE; state ABSENT (proof evidence_84); linked by batch-unique (activity_2643, confidence 0.95); category USER_PROFILE: resource type default
- security_service/audit_record_7011: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_17; category SECURITY_AUDIT_LOG: resource type default; state from evidence_17 (captured after audit_at; not citable)
- search_service/search_2138: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_84); linked by identifier match in evidence_84; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_1887: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_84); linked by identifier match in evidence_84; category SUPPORT_MESSAGE: stated by evidence_17

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_2138 | REPORT_REMAINING_RECORD | PRESENT | evidence_84 |
| 2 | FINDING | support_platform | support_1887 | REPORT_EXPOSED_PII | PRESENT | evidence_84 |
| 3 | REMEDIATION | search_service | search_2138 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_1887 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_6659 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_2138 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_7011 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | support_platform | support_1887 | VERIFY_RECORD_REDACTED | REDACTED |  |
