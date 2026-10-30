# Functional Requirements

> Source: [Functional Requirements](https://mindyworkflows.atlassian.net/wiki/pages/229429) · Content ID `229429`

**Module purpose:** Translate approved System Behaviors into testable Functional Requirements grouped by User Story. Detailed BDD Acceptance Criteria remain in Jira.

**Reading model:** Story Goal → Functional Requirement → Core Trace → Lifecycle / Exception references.

**Terminology:** Subscription Change Request (**SCR**) is the business entity for one upgrade or downgrade transaction. Stable technical identifiers retain `CR`, such as `ST-CR-05`.

## 1. US-01 — View Current Subscription & Available Plans

**Story goal:** Allow users to understand the current subscription, usage and available plan-change options.

| **FR ID** | **Functional Requirement** | **Core Trace** |
| --- | --- | --- |
| `FR-PLAN-01` | The system shall display the workspace’s current plan, price, billing cycle and next billing date. | Read-only subscription query |
| `FR-PLAN-02` | The system shall display current usage against each applicable plan quota, including members, projects and storage. | Usage and entitlement query |
| `FR-PLAN-03` | The system shall display available plans, prices, quotas, feature entitlements and plan rank. | Plan Catalogue |
| `FR-PLAN-04` | The system shall display only plan-change actions permitted for the user’s role and valid for the current plan and Subscription state. | `BR-AUTH-01` · `BR-CHANGE-01` |

**Traceability:** Subscription `ACTIVE | PAST_DUE | RESTRICTED`; SCR: N/A; exception `EX-INT-01`; Jira [SUB-4](https://mindyworkflows.atlassian.net/browse/SUB-4).

## 2. US-02 — Configure & Preview Upgrade Quote

**Story goal:** Allow a Workspace Owner or Billing Admin to review a transparent upgrade quote before deciding to pay.

| **FR ID** | **Functional Requirement** | **Core Trace** |
| --- | --- | --- |
| `FR-UPG-01` | The system shall validate that the target plan has a higher rank than the current plan. | `BR-CHANGE-01` |
| `FR-UPG-02` | The system shall verify the user has permission to upgrade and block quote generation when a required invoice is `PAST_DUE` or another non-terminal SCR exists. | `BR-AUTH-01` · `BR-ELIG-01` · `BR-CHANGE-02` |
| `FR-UPG-03` | The system shall request and display the Billing System calculation for billable members, remaining credit, proration, tax/VAT, applicable discounts and final payable amount. | `BR-BILL-01` · `BR-PRICE-01` |
| `FR-UPG-04` | The system shall display the new billing period, immediate effective timing and the quote’s 15-minute validity window. | `BR-PRICE-01` |
| `FR-UPG-05` | The system shall recalculate the quote when it expires or any pricing input changes before confirmation. | `BR-PRICE-01` · `EX-INT-01` |

**Traceability:** Quote Draft: transient / in-memory; persisted SCR: none; exception `EX-INT-01`; Jira [SUB-5](https://mindyworkflows.atlassian.net/browse/SUB-5).

## 3. US-03 — Confirm Upgrade & Process Payment

**Story goal:** Persist the upgrade transaction, process payment safely, activate the target plan and prevent duplicate financial outcomes.

| **FR ID** | **Functional Requirement** | **Core Trace** |
| --- | --- | --- |
| `FR-UPG-06` | On explicit confirmation of a valid quote, the system shall create one Upgrade SCR in `PAYMENT_PENDING` and initiate the processor-hosted payment flow. | `SB-UPG-03` · `ST-CR-05` |
| `FR-UPG-07` | The system shall accept payment outcomes only from verified Payment Processor callbacks and shall deduplicate them using the idempotency key. | `QG-01` · `EX-UPG-04` |
| `FR-UPG-08` | When payment fails, the system shall retain the current plan, move the SCR to `PAYMENT_FAILED` and allow retry on the same SCR. | `SB-UPG-04` · `ST-CR-06/11` · `EX-UPG-01` |
| `FR-UPG-09` | When payment succeeds, the system shall record the successful Payment Attempt, move the SCR to `ACTIVATION_PENDING` and request target-plan entitlement activation. | `SB-UPG-05` · `ST-CR-07` |
| `FR-UPG-10` | The system shall move the SCR to `APPLIED` only after successful entitlement activation. If activation fails, it shall move to `ACTIVATION_FAILED`, retry activation on the same SCR and never charge again. | `SB-UPG-06/07` · `ST-CR-08/09/10` · `EX-UPG-03` |

**Traceability:** SCR `PAYMENT_PENDING → PAYMENT_FAILED | ACTIVATION_PENDING → ACTIVATION_FAILED | APPLIED`; exceptions `EX-UPG-01`–`EX-UPG-04`; Jira [SUB-6](https://mindyworkflows.atlassian.net/browse/SUB-6).

## 4. US-04 — Validate Usage & Schedule Downgrade

**Story goal:** Assess downgrade impact and schedule an eligible lower plan for the current billing-cycle end without deleting customer data.

| **FR ID** | **Functional Requirement** | **Core Trace** |
| --- | --- | --- |
| `FR-DOWN-01` | The system shall validate that the target plan has a lower rank than the current plan. | `BR-CHANGE-01` |
| `FR-DOWN-02` | The system shall verify the user has permission to downgrade and block scheduling when a required invoice is `PAST_DUE` or another non-terminal SCR exists. | `BR-AUTH-01` · `BR-ELIG-01` · `DT-DOWN-01–04` |
| `FR-DOWN-03` | The system shall compare current usage with the target-plan quotas. | `BR-DOWN-02` · `EX-DOWN-01` |
| `FR-DOWN-04` | The system shall display quotas, features, workflows and integrations affected by the downgrade. | `BR-ENT-01` |
| `FR-DOWN-05` | The system shall allow an over-quota workspace to schedule the downgrade with a clear warning. After the Effective Date, Soft Enforcement shall preserve existing data and block only usage-increasing or unsupported actions. | `BR-DOWN-02` · `DT-DOWN-06` · `DEC-DATA-01` |
| `FR-DOWN-06` | On confirmation, the system shall create one SCR in `SCHEDULED`, store its Effective Date and retain the current plan until execution. | `SB-DOWN-02` · `ST-CR-01` |
| `FR-DOWN-07` | At the Effective Date, the system shall first revalidate eligibility. If revalidation passes, it shall atomically apply the target plan, quota and entitlements and move the SCR to `APPLIED`; otherwise it shall retain the previous effective plan and move the SCR to `EXECUTION_FAILED`. | `SB-DOWN-05/06/07` · `ST-CR-03/04` · `EX-DOWN-02` |

**Traceability:** SCR `SCHEDULED → APPLIED | EXECUTION_FAILED`; exceptions `EX-DOWN-01`, `EX-DOWN-02`; Jira [SUB-7](https://mindyworkflows.atlassian.net/browse/SUB-7).

## 5. US-05 — Cancel Scheduled Downgrade

**Story goal:** Allow an authorized user to cancel a scheduled downgrade before it takes effect.

| **FR ID** | **Functional Requirement** | **Core Trace** |
| --- | --- | --- |
| `FR-DOWN-08` | The system shall display the cancel action only when the SCR is `SCHEDULED` and the current time is before its Effective Date. | `BR-AUTH-01` · `BR-DOWN-01` |
| `FR-DOWN-09` | On confirmed cancellation, the system shall de-schedule the execution job and move the SCR to terminal state `CANCELLED`. | `SB-DOWN-04` · `ST-CR-02` |
| `FR-DOWN-10` | The system shall prevent Effective-Date execution of a cancelled downgrade and release the workspace to create a new eligible SCR. | `BR-CHANGE-02` · `ST-CR-02` |
| `FR-DOWN-11` | The system shall retain the current plan and entitlements and notify the user that cancellation succeeded. | `SB-DOWN-04` |

**Traceability:** SCR `SCHEDULED → CANCELLED`; late cancellation is rejected by the `BR-DOWN-01` / `ST-CR-02` guard; Jira [SUB-8](https://mindyworkflows.atlassian.net/browse/SUB-8).

## 6. US-06 — Grace Period & Recurring Payment Recovery

**Story goal:** Manage overdue invoices through a fixed 30-day recovery window, controlled restriction and automatic access restoration.

| **FR ID** | **Functional Requirement** | **Core Trace** |
| --- | --- | --- |
| `FR-REC-01` | After verified recurring-payment failure, the system shall set the required invoice and Subscription to `PAST_DUE` and start a fixed 30-day Grace Period (720 hours). | `BR-GRACE-01` · `ST-SUB-02` |
| `FR-REC-02` | During the Grace Period, the system shall retain normal workspace access, display payment status and the recovery deadline, and block new plan-change requests. | `SB-REC-02` · `BR-ELIG-01` |
| `FR-REC-03` | The system shall allow a Billing Admin to initiate a processor-hosted payment-method update or payment retry; ApproveFlow shall not collect raw payment credentials. | `NFR-SEC-02` |
| `FR-REC-04` | When all required invoices are paid within the Grace Period, the system shall cancel the restriction timer, clear the warning and return the Subscription to `ACTIVE`. | `SB-REC-03` · `ST-SUB-03` |
| `FR-REC-05` | If any required invoice remains unpaid after 30 days (720 hours), the system shall move the Subscription to `RESTRICTED`, apply read-only access and preserve all data. | `SB-REC-04` · `ST-SUB-04` |
| `FR-REC-06` | After all required invoices are paid following restriction, the system shall set the Subscription to `ACTIVE` and automatically restore full access without an additional fee. | `SB-REC-05/06` · `ST-SUB-05` |

**Traceability:** Subscription `ACTIVE ↔ PAST_DUE → RESTRICTED → ACTIVE`; SCR: N/A; exceptions `EX-REC-01`–`EX-REC-03`; Jira [SUB-9](https://mindyworkflows.atlassian.net/browse/SUB-9).

## 7. Cross-Cutting Requirements

### 7.1. Shared Functional Requirements

| **FR ID** | **Functional Requirement** | **Applicable Stories** |
| --- | --- | --- |
| `FR-STATUS-01` | The system shall display the current business state and latest verified outcome for each persisted SCR, Subscription recovery process or access transition. | `US-03`–`US-06` |
| `FR-NOT-01` | The system shall notify affected users of significant payment, plan-change and access outcomes. | `US-03`–`US-06` |
| `FR-AUD-01` | The system shall record actor, workspace, action, timestamp, request/correlation ID and result for every state-changing plan or payment action. | `US-03`–`US-06` |

### 7.2. Non-Functional Requirements

| **NFR ID** | **Quality Attribute** | **Requirement & Boundary** | **Verification** |
| --- | --- | --- | --- |
| `NFR-SEC-01` | Role-based security | The API shall enforce role-based permissions (RBAC— Role-Based Access Control) for plan-change and payment-recovery actions; permitted roles are Workspace Owner and Billing Admin. | Automated authorization tests |
| `NFR-SEC-02` | Payment-data security | ApproveFlow shall not store, transmit or log raw card credentials such as PAN or CVV. | Contract review and security test |
| `NFR-REL-01` | Financial idempotency | Repeated submissions and callbacks shall not create duplicate SCRs, charges or entitlement activations. | Concurrency and duplicate-event tests |
| `NFR-REL-02` | Fail-safe recovery | Timeout or unknown outcomes shall preserve the last verified business state until reconciliation produces a verified result. | Exception and reconciliation tests |
| `NFR-PERF-01` | Activation SLA | Median upgrade activation time shall not exceed five minutes, measured from receipt of a verified payment-success webhook until target-plan entitlements are active. Time spent by the user in the processor-hosted payment flow is excluded. | `BSM-03` performance benchmark |
| `NFR-AUD-01` | Auditability | Audit records for state-changing actions shall contain actor/worker, workspace, request/correlation ID, before/after state, timestamp and result. | Audit-record verification |
| `NFR-DATA-01` | Data preservation | Downgrade, `PAST_DUE` and `RESTRICTED` handling shall never delete existing customer data. | Data-retention and migration tests |

Infrastructure sizing, detailed availability targets and unapproved retry, backoff or monitoring thresholds remain delivery-team design decisions.
