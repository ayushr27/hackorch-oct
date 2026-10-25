# case_426 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_424: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_1576: USER_PROFILE → DELETE; state ABSENT (proof evidence_68); linked by batch-delay-match (activity_901, confidence 1.0); alternatives ['account_9633']; category USER_PROFILE: resource type default
- security_service/audit_record_5472: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_40; category SECURITY_AUDIT_LOG: resource type default; state from evidence_40 (captured after audit_at; not citable)
- search_service/search_2635: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_68); linked by identifier match in evidence_68; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_9212: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_68); linked by identifier match in evidence_68; category SUPPORT_MESSAGE: stated by evidence_40

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_2635 | REPORT_REMAINING_RECORD | PRESENT | evidence_68 |
| 2 | FINDING | support_platform | support_9212 | REPORT_EXPOSED_PII | PRESENT | evidence_68 |
| 3 | REMEDIATION | search_service | search_2635 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_9212 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_1576 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_2635 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_5472 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | support_platform | support_9212 | VERIFY_RECORD_REDACTED | REDACTED |  |
