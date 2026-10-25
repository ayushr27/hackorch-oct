# case_165 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_163: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_3064: USER_PROFILE → DELETE; state PII (proof evidence_85); linked by evidence (activity_2845, confidence 1.0); category USER_PROFILE: resource type default
- analytics_platform/analytics_2713: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_85); linked by identifier match in evidence_85; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD
- security_service/audit_record_4964: SECURITY_AUDIT_LOG → RETAIN; state CLEAN (proof -); linked by identifier match in evidence_16; category SECURITY_AUDIT_LOG: resource type default; state from evidence_16 (captured after audit_at; not citable)
- search_service/search_8678: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_85); linked by identifier match in evidence_85; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_3586: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_85); linked by identifier match in evidence_85; category SUPPORT_MESSAGE: stated by evidence_16

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | account_service | account_3064 | REPORT_REMAINING_RECORD | PRESENT | evidence_85 |
| 2 | FINDING | search_service | search_8678 | REPORT_REMAINING_RECORD | PRESENT | evidence_85 |
| 3 | FINDING | analytics_platform | analytics_2713 | REPORT_EXPOSED_PII | PRESENT | evidence_85 |
| 4 | FINDING | support_platform | support_3586 | REPORT_EXPOSED_PII | PRESENT | evidence_85 |
| 5 | REMEDIATION | account_service | account_3064 | DELETE_RECORD | ABSENT |  |
| 6 | REMEDIATION | search_service | search_8678 | DELETE_RECORD | ABSENT |  |
| 7 | REMEDIATION | support_platform | support_3586 | REDACT_RECORD | REDACTED |  |
| 8 | REMEDIATION | analytics_platform | analytics_2713 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 9 | VERIFICATION | account_service | account_3064 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 10 | VERIFICATION | search_service | search_8678 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 11 | VERIFICATION | security_service | audit_record_4964 | VERIFY_RECORD_PRESENT | PRESENT |  |
| 12 | VERIFICATION | support_platform | support_3586 | VERIFY_RECORD_REDACTED | REDACTED |  |
| 13 | VERIFICATION | analytics_platform | analytics_2713 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
