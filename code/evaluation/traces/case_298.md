# case_298 — INCOMPLETE

## Investigation

- intent: DELETE_ACCOUNT — deletion language: 'eras' (LLM agrees)
- subject user_296: 2 email(s), 2 hash(es), 1 phone(s)
- account_service/account_4880: USER_PROFILE → DELETE; state ABSENT (proof evidence_75); linked by batch-delay-match (activity_1670, confidence 1.0); alternatives ['account_6023']; category USER_PROFILE: resource type default
- search_service/search_6282: SEARCH_INDEX_ENTRY → DELETE; state PII (proof evidence_75); linked by identifier match in evidence_75; category SEARCH_INDEX_ENTRY: resource type default
- support_platform/support_643: SUPPORT_MESSAGE → REDACT; state PII (proof evidence_75); linked by identifier match in evidence_75; category SUPPORT_MESSAGE: implied by worker REDACT_RECORD

## Steps

| # | phase | system | resource | operation | state | evidence |
|---|---|---|---|---|---|---|
| 1 | FINDING | search_service | search_6282 | REPORT_REMAINING_RECORD | PRESENT | evidence_75 |
| 2 | FINDING | support_platform | support_643 | REPORT_EXPOSED_PII | PRESENT | evidence_75 |
| 3 | REMEDIATION | search_service | search_6282 | DELETE_RECORD | ABSENT |  |
| 4 | REMEDIATION | support_platform | support_643 | REDACT_RECORD | REDACTED |  |
| 5 | VERIFICATION | account_service | account_4880 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 6 | VERIFICATION | search_service | search_6282 | VERIFY_RECORD_ABSENT | ABSENT |  |
| 7 | VERIFICATION | support_platform | support_643 | VERIFY_RECORD_REDACTED | REDACTED |  |
