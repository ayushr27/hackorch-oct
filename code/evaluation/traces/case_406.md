# case_406 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_404: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_8997: USER_PROFILE → DELETE; state ABSENT (proof evidence_38); linked by batch-delay-match (activity_1048, confidence 0.938); alternatives ['account_1759']; category USER_PROFILE: resource type default
- security_service/audit_record_5455: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof evidence_38); linked by identifier match in evidence_38; category SECURITY_AUDIT_LOG: resource type default
- search_service/search_2804: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_38); linked by identifier match in evidence_38; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_6047: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_38); linked by identifier match in evidence_38; category SUPPORT_MESSAGE: stated by evidence_38

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_2804 | REPORT_REMAINING_RECORD | PRESENT | evidence_38 |
| 2 | FINDING | support_platform | support_6047 | REPORT_EXPOSED_PII | PRESENT | evidence_38 |
| 3 | REMEDIATION | search_service | search_2804 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_6047 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_8997 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_2804 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | security_service | audit_record_5455 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 8 | VERIFICATION | support_platform | support_6047 | VERIFY_RECORD_REDACTED | REDACTED |  |
