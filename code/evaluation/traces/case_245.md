# case_245 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'delet' (LLM agrees)
- subject user_243: 1 email(s), 1 hash(es), 1 phone(s)
- account_service/account_5072: USER_PROFILE → DELETE; state ABSENT (proof evidence_78); linked by batch-delay-match (activity_2235, confidence 0.0); alternatives ['account_2481', 'account_1264']; category USER_PROFILE: resource type default
- analytics_platform/analytics_4010: ANALYTICS_PROFILE → ANONYMIZE; state PII (proof evidence_78); linked by identifier match in evidence_78; category ANALYTICS_PROFILE: implied by worker ANONYMIZE_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | analytics_platform | analytics_4010 | REPORT_EXPOSED_PII | PRESENT | evidence_78 |
| 2 | REMEDIATION | analytics_platform | analytics_4010 | ANONYMIZE_RECORD | ANONYMIZED |  |
| 3 | VERIFICATION | account_service | account_5072 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 4 | VERIFICATION | analytics_platform | analytics_4010 | VERIFY_RECORD_ANONYMIZED | ANONYMIZED |  |
