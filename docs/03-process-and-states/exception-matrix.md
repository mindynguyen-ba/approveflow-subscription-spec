# Exception Matrix & Failure Recovery

> Source: [Exception Matrix & Failure Recovery](https://mindyworkflows.atlassian.net/wiki/pages/5373964) · Content ID `5373964`

**Module purpose:** Define business exceptions, safe-state handling, customer outcomes and recovery ownership across upgrade, downgrade and recurring-payment recovery.

**Baseline guardrail:** Severity is classified by business impact. Exact timeout, retry, backoff, paging and resolution targets remain operational decisions until approved. Values proposed in review are captured in Section 4 and are not silently promoted to requirements.

## 1. Severity Model

| **Severity** | **Business impact** | **Default handling** |
| --- | --- | --- |
| P1 CRITICAL | Paid/entitled/access states diverge, unauthorized write access may continue, or a plan change is partially applied. | Immediate automated containment and Platform Operations escalation. Paging and response target: **TBD**. |
| P2 MAJOR | The transaction is blocked or degraded, but the last verified business state and data remain safe. | Automated retry or reconciliation where approved; operational alert if the condition persists. Threshold: **TBD**. |
| P3 CONTAINED | User-correctable failure or duplicate input with no state-integrity risk. | Return a clear recovery action, record the event and avoid unnecessary paging. |

HTTP status alone does not determine severity. Severity follows the resulting business-state and access-state risk.

## 2. Master Exception Matrix

| **ID** | **Scenario & severity** | **Detection** | **Canonical response & state** | **User outcome** | **Recovery owner** | **Trace** |
| --- | --- | --- | --- | --- | --- | --- |
| `EX-UPG-01` | **Payment failed** P3 | A verified processor result is failed/declined, and the Payment Attempt is `FAILED`. | Keep the current plan and entitlements. Set the Subscription Change Request (**SCR**) to `PAYMENT_FAILED`. Do not start activation or create another SCR. | Show the failure, allow payment-method update or retry on the same request. | User / Payment Processor | `BR-UPG-01` `DT-UPG-03` `ST-CR-06/11` |
| `EX-UPG-02` | **Payment status unknown** P2 | No verified callback is available within the provider monitoring window, or the provider result remains pending/unknown. | Keep the SCR in `PAYMENT_PENDING`. Do not activate the target plan. Reconcile against the processor before accepting another payment action. | Show processing status and prevent duplicate submission. | Automated reconciliation → Finance Operations | `DT-UPG-04` `NFR-REL-02` `OPEN-OPS-01` |
| `EX-UPG-03` | **Payment succeeded; activation failed** P1 | Payment success is verified, but the Entitlement Service returns failure or the activation attempt times out. | Retain the successful payment. Set the SCR to `ACTIVATION_FAILED`. Retry activation on the same request without charging again; escalate when the approved retry policy is exhausted. | Confirm payment received and show activation recovery status. Expose manual activation retry where authorized. | Automated worker → Platform Operations | `BR-UPG-01` `DT-UPG-02` `ST-CR-09/10` `OPEN-CR-02` |
| `EX-UPG-04` | **Duplicate callback or submission** P3 | The same provider attempt or idempotency key and payload is received again. | Return the stored original result with no state change, new charge or duplicate activation. A reused key with a different payload is rejected as `409 SUB_IDEMPOTENCY_CONFLICT`. | Show the previously recorded outcome. | Automated idempotency control | `BR-CHANGE-02` `BR-UPG-01` `DT-UPG-05` `SQL-05` |
| `EX-DOWN-01` | **Usage or quota context unavailable** P2 | Usage/quota data cannot be loaded or validated before downgrade review. | Do not determine eligibility and do not create a `SCHEDULED` request. Preserve the current plan and last verified state. Return a retryable context-unavailable outcome. | Show a temporary error and keep confirmation disabled. | User retry → Platform Operations if persistent | `BR-DOWN-02` `FR-DOWN-03` `SUB_CONTEXT_UNAVAILABLE` |
| `EX-DOWN-02` | **Downgrade execution failed** P1 | Effective-date revalidation fails, or target-plan entitlement/quota application does not complete successfully. | Do not leave a partially applied plan. Retain the previous effective plan and data, set the SCR to terminal `EXECUTION_FAILED`, notify the user and alert Platform Operations. Automatic retry is not in the approved baseline. | Show downgrade not applied and support follow-up status. | Platform Operations | `BR-DOWN-01` `BR-DOWN-02` `BR-ENT-01` `ST-CR-03` |
| `EX-REC-01` | **Payment-recovery retry failed** P3 | A verified recovery-payment attempt returns failure. | Keep the invoice `PAST_DUE` and the Subscription `PAST_DUE`. Record the failed attempt. The fixed 30-day / 720-hour Grace Period continues from the original verified failure and is never reset. | Show the payment failure and the unchanged recovery deadline. | User / Support | `BR-GRACE-01` `ST-SUB-02/03` |
| `EX-REC-02` | **Automatic restriction failed** P1 | The 30-day timer has expired with a required invoice still unpaid, but read-only enforcement fails or a post-check shows the workspace remains writable. | Keep the Subscription business state `RESTRICTED`. Retry read-only enforcement using the approved operational policy and alert Platform Operations/Security. Do not extend or restart the Grace Period. | Show restricted/payment-recovery status; access enforcement may be temporarily inconsistent. | Automated worker → Platform Operations / Security | `BR-REC-01` `ST-SUB-04` `OPEN-OPS-02` |
| `EX-REC-03` | **Payment recovered; access restoration failed** P1 | All required invoices are paid and the Subscription is `ACTIVE`, but the Access Service still reports read-only/restricted access. | Preserve the verified paid result and `ACTIVE` business state. Retry access restoration without charging again and escalate until access matches the business state. | Confirm payment received and show restoration pending. | Automated worker → Platform Operations | `BR-REC-01` `ST-SUB-05` `OPEN-OPS-02` |
| `EX-INT-01` | **Billing or Payment service unavailable** P2 | Dependency timeout, open circuit, or `HTTP 500/502/503/504`. Escalate to P1 only when the outage is sustained/widespread or state integrity is at risk. | Keep the last verified business state. Do not create a duplicate transaction. Fail closed for new state-changing actions and allow safe retry after dependency recovery. | Show a retry-later message; current workspace data remains unchanged. | Platform Operations / Service owner | `BR-PRICE-01` `BR-UPG-01` `NFR-REL-02` |

## 2. Recovery Invariants

1. **No double charge:** payment, activation and restoration retries reuse the existing business request/result; they never create a second charge implicitly.
2. **Grace Period immutability:** failed retries or payment-method updates do not reset the original 30-day / 720-hour deadline.
3. **No partial downgrade:** a failed effective-date execution must not leave mixed plan, quota or entitlement state; `EXECUTION_FAILED` is terminal in the current baseline.
4. **Business state and access state are checked separately:** `RESTRICTED` with writable access and `ACTIVE` with read-only access are both P1 mismatches.
5. **Minimum audit evidence:** record correlation/request ID, provider attempt ID, entity state before/after, dependency result, retry count, actor/worker, timestamp and final owner.

## 3. Operational Decisions Still Open

| **Decision** | **Review proposal** | **Required approval before implementation** |
| --- | --- | --- |
| `OPEN-OPS-01` Payment-unknown handling | 120-second timeout; reconcile every 5 minutes; maximum 3 attempts. | Approve provider timeout source, polling cadence, stop condition and customer-visible status. |
| `OPEN-CR-02` Activation recovery | 10-second service timeout; backoff at 5s / 30s / 2m; 3 attempts; then DLQ. | Approve retry limit, backoff, DLQ ownership, final terminal state and refund/manual-resolution path. |
| `OPEN-OPS-02` Restriction/restoration recovery | Restriction retry every 15 minutes up to 5 times; restoration P1 target under 15 minutes. | Approve retry schedule, alert channel, paging policy, service target and manual override procedure. |
| `OPEN-OPS-03` Incident routing | P1/P2/P3 mapped directly to paging/logging. | Approve on-call roles, escalation matrix and environment-specific alert thresholds. |

**Do not implement these proposed values as constants yet.** After approval, update Business Rules, State Transition Model, API contracts, Acceptance Criteria, UAT and Process Models in the same Change Request.

## 4. Related Artefacts

- <https://mindyworkflows.atlassian.net/wiki/x/FYAB>
- [State Transition Model Specification](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131234/State+Transition+Model+Specification)
- [API, SQL & Sequence Analysis](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis)
- [Main Cockpit Change-Ready](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/7110657/Main+Cockpit+Change-Ready)
