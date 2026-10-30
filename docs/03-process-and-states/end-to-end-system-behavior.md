# End-to-End System Behavior

> Source: [End-to-End System Behavior](https://mindyworkflows.atlassian.net/wiki/pages/10092622) · Content ID `10092622` · Version `11` · Status `current`

> **Purpose.** Translate approved rules, decisions, state transitions and exceptions into end-to-end behavior for implementation review, integration testing and E2E test design.

**How to read this page.** Each row separates the state of the Subscription Change Request (**SCR**) from the state of the **Subscription**. “Observable output” records what a caller, user or operator can verify. Exact payloads, error codes and endpoint semantics remain canonical in [API, SQL & Sequence Analysis](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis).

**Specification boundary.** This page does not invent implementation thresholds. Checkout field names, timeout values, retry counts/backoff and incident SLA/severity must come from an approved API or operational decision. Until then, behavior is defined by safe state retention, idempotency and recoverability.

**Canonical inputs:** [Business Rules & Decision Tables](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98325/Business+Rules+Decision+Tables) · [State Transition Model](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131234/State+Transition+Model+Specification) · [Exception Matrix](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/5373964/Exception+Matrix+Failure+Recovery) · [Process Models](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131226/Process+Models)

## 1. Self-Service Upgrade

Immediate upgrade after verified payment and successful entitlement activation.

| **ID** | **Trigger / Pre-condition** | **Expected execution & side effects** | **Entity state result** | **Observable output** | **Trace** |
| --- | --- | --- | --- | --- | --- |
| **SB-UPG-01** | Authorized user selects a higher-ranked plan. | - Validate role, subscription status and existing non-terminal SCR. - Return eligibility and blocking reasons; do not mutate business state. | - **SCR:** — - **Subscription:** No change | API-02 eligibility result and `blocking_reasons`. | `BR-AUTH-01` · `BR-CHANGE-01` · `BR-ELIG-01` · `API-02` |
| **SB-UPG-02** | Upgrade is eligible. | - Request pricing from Billing System; ApproveFlow does not recalculate proration, tax/VAT or discount. - Return a time-bounded preview with quota impact and effective timing. | - **SCR:** — - **Subscription:** No change | `preview_id`, pricing, quota impact, `effective_at`, `valid_until`. | `BR-PRICE-01` · `API-02` · `DEC-ARCH-01` |
| **SB-UPG-03** | User confirms a valid preview. | - Revalidate authorization, eligibility and preview validity. - Create one Upgrade SCR using an idempotency key and initiate payment. | - **SCR:** `PAYMENT_PENDING` - **Subscription:** `ACTIVE` — current plan | `change_request_id`, `status`, `effective_at`; payment initiation handed to the processor flow. | `ST-CR-05` · `BR-UPG-01` · `API-03` |
| **SB-UPG-04** | Verified upgrade payment result is failed. | - Mark Payment Attempt failed and retain current plan and entitlements. - Expose retry path without creating a duplicate SCR. | - **SCR:** `PAYMENT_FAILED` - **Subscription:** `ACTIVE` — current plan - **Payment Attempt:** `FAILED` | API-05 acknowledgement; failed status and retry action available to UI. | `DT-UPG-03` · `ST-CR-06` · `EX-UPG-01` · `API-05` |
| **SB-UPG-05** | Verified upgrade payment result is successful. | - Verify callback signature and deduplicate the event. - Record payment success and start target-entitlement activation; payment success alone does not complete the upgrade. | - **SCR:** `ACTIVATION_PENDING` - **Subscription:** `ACTIVE` — current plan - **Payment Attempt:** `SUCCESS` | API-05 acknowledgement with `accepted`, `duplicate` and `processing_status`. | `ST-CR-07` · `QG-01` · `API-05` |
| **SB-UPG-06** | Target-entitlement activation succeeds. | - Apply target plan, quotas and feature entitlements. - Complete the SCR and notify the authorized billing user. | - **SCR:** `APPLIED` — terminal - **Subscription:** `ACTIVE` — target plan | Applied status visible through subscription context / SCR status. | `DT-UPG-01` · `ST-CR-08` · `API-05` · `API-06` |
| **SB-UPG-07** | Entitlement activation fails after payment success. | - Retain the successful payment and current plan; never charge again for recovery. - Record the exception, keep recovery retriable and alert Platform Admin. | - **SCR:** `ACTIVATION_FAILED` - **Subscription:** `ACTIVE` — current plan | API-05 callback remains accepted; failure is recorded as a downstream business exception. | `DT-UPG-02` · `EX-UPG-03` · `ST-CR-09` · `API-05` |
| **SB-UPG-08** | User retries a failed upgrade payment. | - Reuse the existing SCR. - Create/re-initiate payment using idempotency controls; do not create a second SCR. | - **SCR:** `PAYMENT_PENDING` - **Subscription:** `ACTIVE` — current plan | Existing `change_request_id` with new payment-attempt context. | `ST-CR-11` · `BR-UPG-01` · `BR-CHANGE-02` · `API-03` |

## 2. Scheduled Downgrade

Downgrade is scheduled for billing-cycle end; current plan remains in force until successful execution.

| **ID** | **Trigger / Pre-condition** | **Expected execution & side effects** | **Entity state result** | **Observable output** | **Trace** |
| --- | --- | --- | --- | --- | --- |
| **SB-DOWN-01** | Authorized user selects a lower-ranked plan. | - Validate role, payment status, pending request and target-plan eligibility. - Return billing-cycle-end effective date and quota impact. | - **SCR:** — - **Subscription:** No change | API-02 eligibility, `quota_impact`, `effective_at` and blocking reasons. | `DT-DOWN-01–06` · `API-02` |
| **SB-DOWN-02** | User confirms an eligible downgrade. | - Create one SCR with billing-cycle-end effective date. - Schedule execution for that effective time; current plan remains active. | - **SCR:** `SCHEDULED` - **Subscription:** `ACTIVE` — current plan | `change_request_id`, `status`, `effective_at`. | `ST-CR-01` · `BR-DOWN-01` · `API-03` |
| **SB-DOWN-03** | Current usage exceeds the target-plan quota. | - Allow scheduling under soft enforcement. - Warn which usage-increasing actions or unsupported features will be restricted after the effective date; retain existing data. | - **SCR:** `SCHEDULED` - **Subscription:** `ACTIVE` — current plan | Quota impact and user-facing warning; effective date remains unchanged. | `BR-DOWN-02` · `DT-DOWN-06` · `API-02` |
| **SB-DOWN-04** | User cancels before the effective date while request is scheduled. | - De-schedule the execution job. - Cancel the SCR and retain current plan and entitlements. | - **SCR:** `CANCELLED` — terminal - **Subscription:** `ACTIVE` — current plan | Cancel response includes `status`, `current_plan_retained` and `cancelled_at`. | `ST-CR-02` · `BR-DOWN-01` · `API-03` |
| **SB-DOWN-05** | Effective date arrives and revalidation fails. | - Do not partially apply the downgrade. - Retain current plan and entitlements; record failure and notify the user / operational owner. | - **SCR:** `EXECUTION_FAILED` - **Subscription:** `ACTIVE` — current plan | Failure outcome is persisted and visible for support and status queries. | `ST-CR-03` · `EX-DOWN-02` · `API-06` |
| **SB-DOWN-06** | Effective date arrives and revalidation passes. | - Apply target plan, quotas and feature entitlements atomically. - Complete the SCR and notify the billing user. | - **SCR:** `APPLIED` — terminal - **Subscription:** `ACTIVE` — target plan | Applied plan and completed request visible through context / status queries. | `ST-CR-04` · `BR-DOWN-01` · `API-06` |
| **SB-DOWN-07** | Existing usage remains above the new entitlement after application. | - Preserve existing customer data. - Block usage-increasing actions and pause unsupported features according to entitlement policy. | - **SCR:** `APPLIED` - **Subscription:** `ACTIVE` — target plan - **Entitlement:** soft restrictions enforced | Current usage remains visible; restricted actions return the canonical entitlement outcome. | `BR-DOWN-02` · `BR-ENT-01` · `DEC-DATA-01` |

## 3. Recurring Payment Failure & Recovery

Debt recovery uses a fixed **30-day (720-hour)** grace period, preserves data and keeps payment handling inside the approved external-system boundary.

| **ID** | **Trigger / Pre-condition** | **Expected execution & side effects** | **Entity state result** | **Observable output** | **Trace** |
| --- | --- | --- | --- | --- | --- |
| **SB-REC-01** | Verified recurring-payment result is failed. | - Mark the required invoice Past Due. - Start a fixed 30-day (720-hour) grace clock and notify Billing Admin. | - **SCR:** N/A - **Subscription:** `PAST_DUE` - **Invoice:** `PAST_DUE` | Subscription context returns invoice status and `grace_expires_at`. | `BR-GRACE-01` · `ST-SUB-02` · `API-01` · `API-05` |
| **SB-REC-02** | Workspace is within the 30-day (720-hour) grace period. | - Retain normal workspace access. - Block new plan changes; allow processor-hosted payment-method update and payment retry. | - **SCR:** N/A - **Subscription:** `PAST_DUE` | API-01 exposes grace expiry; API-04 may create one `INITIATED` Payment Attempt. | `BR-GRACE-01` · `BR-ELIG-01` · `API-01` · `API-04` |
| **SB-REC-03** | All required invoices are paid before grace expiry. | - Cancel scheduled restriction. - Clear warning state and restore normal billing eligibility. | - **SCR:** N/A - **Subscription:** `ACTIVE` - **Invoice:** `PAID` | Verified callback acknowledgement; API-01 subsequently returns active status and no grace expiry. | `ST-SUB-03` · `BR-REC-01` · `API-05` |
| **SB-REC-04** | Grace reaches 30 days (720 hours) with at least one required invoice unpaid. | - Restrict the workspace to read-only access. - Preserve all customer data and keep the payment-recovery path available. | - **SCR:** N/A - **Subscription:** `RESTRICTED` - **Invoice:** `PAST_DUE` | Restricted subscription / access status and payment-required UI state. | `BR-REC-01` · `ST-SUB-04` |
| **SB-REC-05** | All required invoices are paid after restriction. | - Create the eligible access-restoration transition. - Restore normal workspace access automatically after verified payment. | - **SCR:** N/A - **Subscription:** `ACTIVE` - **Invoice:** `PAID` | API-05 acknowledgement; restored status visible through API-01. | `BR-REC-01` · `ST-SUB-05` · `API-05` |
| **SB-REC-06** | Verified payment succeeds but automatic access restoration fails. | - Keep payment and invoice success; do not charge again. - Keep access restricted, record the operational exception, retry safely and alert Platform Admin. | - **SCR:** N/A - **Subscription:** `RESTRICTED` until restoration succeeds - **Invoice:** `PAID` | API-05 callback remains accepted; restoration failure is recorded separately. | `EX-REC-03` · `API-05` |

## 4. Master System Invariants

1. **Single active SCR.** A subscription may have at most one non-terminal SCR.
2. **No in-flight entitlement fluctuation.** Current plan and entitlements remain unchanged until upgrade activation succeeds or a scheduled downgrade executes successfully.
3. **Financial idempotency.** Repeated requests or callbacks must not create duplicate SCRs, charges or entitlement activation.
4. **No data loss.** Downgrade, Past Due and Restricted states must not delete existing customer data.
5. **Fail-safe asynchronous recovery.** A timeout or downstream failure must retain the last verified state. Recovery after a successful charge must be retriable without charging again.
6. **Verified external outcomes only.** Payment and access state change only after authenticated, deduplicated outcomes from the responsible external system.

## 5. Verification Focus

| **Question** | **Required evidence** |
| --- | --- |
| Was the correct entity updated? | SCR, Subscription, Invoice, Payment Attempt, Entitlement Activation or Access Transition state. |
| Was the outcome externally observable? | API response/callback acknowledgement, user notification, status query or operator alert. |
| Was the action idempotent? | Same request/event returns or preserves the original outcome without duplicate charge or activation. |
| Was failure safe? | Last verified plan/access/payment state is retained and recovery remains possible. |

