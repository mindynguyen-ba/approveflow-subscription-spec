> Source: [User Acceptance Testing (UAT) Specification](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98340) · Content ID `98340` · Version `7` · Status `current`

**Evidence status:** DESIGNED — NOT EXECUTED

# Purpose

## Acceptance Gate

1. All nine Must-test scenarios (`UAT-01`–`UAT-09`) are PASS.
2. No Blocker or Critical/High defect affecting financial integrity, subscription state or quota enforcement remains open.
3. All eight data-integrity checks (`SQL-01`–`SQL-08`) return `0 rows`.
4. Product Owner approval is recorded before release.

---

## 1. Journey 1 — Self-Service Upgrade (UAT-01–UAT-04)

| **ID** | **Preconditions & Test Data** | **Business Action** | **Expected Business Outcome** | **Traceability** | **Result** |
| --- | --- | --- | --- | --- | --- |
| **UAT-01** | Billing Admin; Basic plan is `ACTIVE`; no Past Due invoice; usage = 18/50 projects and 21/50 GB. | Open Subscription & Billing and review plan, usage and available actions. | Current plan and usage are accurate. Upgrade to Pro and downgrade to Starter actions reflect role and subscription state. | [US-01](https://mindyworkflows.atlassian.net/browse/SUB-4) `AC-PLAN-01.1–01.6` | NOT RUN |
| **UAT-02** | Basic plan is `ACTIVE`; no Past Due invoice; no non-terminal SCR; Pro is eligible. | Select Pro, verify pricing and proration, confirm the upgrade and complete payment successfully. | Exactly one payment is recorded with an idempotency key; Pro entitlements activate immediately; the SCR becomes `APPLIED`. | [US-02](https://mindyworkflows.atlassian.net/browse/SUB-5), [US-03](https://mindyworkflows.atlassian.net/browse/SUB-6) `AC-UPG-02.1–02.6` `AC-UPG-03.2–03.3` [SD-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) | NOT RUN |
| **UAT-03** | Eligible Pro upgrade; Payment Processor returns a failed payment outcome. | Submit payment, review the failure and retry on the same upgrade request. | Basic remains active; the same SCR returns from `PAYMENT_FAILED` to `PAYMENT_PENDING`; no duplicate charge or SCR is created. | [US-03](https://mindyworkflows.atlassian.net/browse/SUB-6) `AC-UPG-03.1, 03.5–03.6` [SQL-04](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) | NOT RUN |
| **UAT-04** | Payment succeeds; Entitlement Service returns an activation failure. | Complete payment and review the failed activation state and recovery action. | The successful charge is recorded once; the current plan remains unchanged; `ACTIVATION_FAILED` and Retry Activation are visible; recovery does not recharge. | [US-03](https://mindyworkflows.atlassian.net/browse/SUB-6) `AC-UPG-03.3–03.6` [SQL-03, SQL-05, SD-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) | NOT RUN |

## 2. Journey 2 — Scheduled Downgrade (UAT-05–UAT-07)

| **ID** | **Preconditions & Test Data** | **Business Action** | **Expected Business Outcome** | **Traceability** | **Result** |
| --- | --- | --- | --- | --- | --- |
| **UAT-05** | Pro plan is `ACTIVE`; Starter is eligible; usage exceeds Starter quota at 18/10 projects; no conflicting SCR. | Review quota impact and schedule downgrade to Starter. | Soft-enforcement warning is visible but scheduling remains allowed. The SCR becomes `SCHEDULED` for cycle end; Pro remains active and retained data is not deleted. | [US-04](https://mindyworkflows.atlassian.net/browse/SUB-7) `AC-DOWN-04.1–04.7` | NOT RUN |
| **UAT-06** | A downgrade SCR is `SCHEDULED` and its effective date has not been reached. | Cancel the scheduled downgrade and confirm the action. | The SCR becomes `CANCELLED`; Pro and its entitlements remain active; no downgrade executes at cycle end. | [US-05](https://mindyworkflows.atlassian.net/browse/SUB-8) `AC-DOWN-05.1–05.5` | NOT RUN |
| **UAT-07** | A downgrade is `SCHEDULED`; before cycle end, the account becomes `PAST_DUE` or the workspace loses eligibility because access is restricted. | Run effective-date revalidation at billing-cycle end. | The downgrade is not applied; the SCR becomes `EXECUTION_FAILED` with a visible reason; the current plan, entitlements and retained data remain intact. | [US-04](https://mindyworkflows.atlassian.net/browse/SUB-7) `AC-DOWN-04.6–04.8` [SQL-08, SD-03](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) | NOT RUN |

## 3. Journey 3 — Payment Failure Recovery (UAT-08–UAT-09)

| **ID** | **Preconditions & Test Data** | **Business Action** | **Expected Business Outcome** | **Traceability** | **Result** |
| --- | --- | --- | --- | --- | --- |
| **UAT-08** | Recurring payment failed; required invoice is `PAST_DUE`; elapsed time is less than 30 days (720 hours). | Review the Grace Period banner, update the payment method through the Payment Processor if required and retry payment. | Workspace access remains available; new plan changes are blocked. Successful recovery makes the invoice `PAID` and the subscription `ACTIVE`. | [US-06](https://mindyworkflows.atlassian.net/browse/SUB-9) `AC-REC-06.1–06.3, 06.5, 06.8` [SD-02](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) | NOT RUN |
| **UAT-09** | A required invoice remains `PAST_DUE` at or beyond 30 days (720 hours). | Attempt workspace access, pay all required Past Due invoices through the hosted payment flow and review restoration. | The workspace is `RESTRICTED` to read-only access with data retained. Full read/write access is restored only after no required Past Due invoice remains; restoration is not duplicated. | [US-06](https://mindyworkflows.atlassian.net/browse/SUB-9) `AC-REC-06.4–06.7, 06.9` [SQL-06, SQL-07, SD-02](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) | NOT RUN |

