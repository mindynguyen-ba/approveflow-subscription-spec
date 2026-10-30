# Business Rules & Decision Tables

> Source: [Business Rules & Decision Tables](https://mindyworkflows.atlassian.net/wiki/pages/98325) · Content ID `98325`



# Purpose

**Module purpose:** Define the Business Rules Catalogue and Decision Tables that govern plan changes, pricing, payment recovery, quota enforcement and data protection. Engineering uses this specification for validation and orchestration; QA uses it to derive unit, integration and acceptance tests.

## 1. Business Rules Catalogue

| **Rule ID** | **Rule Statement** | **Primary Enforcement Layer** | **Source Ref** |
| --- | --- | --- | --- |
| `BR-AUTH-01` | Only a **Workspace Owner** or **Billing Admin** may initiate or confirm a plan change, cancel a scheduled downgrade, or perform payment-recovery actions. | ApproveFlow API / RBAC | `DEC-ROLE-01` |
| `BR-BILL-01` | A billable member is active and non-guest. Guests are not billable. The Billing System is the single source of truth for the billable-member count. | Billing System | `DEC-BILL-01` |
| `BR-CHANGE-01` | Classify a plan change by rank: `Target Rank > Current Rank` = Upgrade; `Target Rank < Current Rank` = Downgrade; equal ranks = `NO_CHANGE` and submission is rejected. | Subscription Core / Web UI | Plan Catalogue |
| `BR-CHANGE-02` | A workspace may have at most one non-terminal Subscription Change Request (**SCR**) (`PENDING` or `SCHEDULED`). An immediate upgrade requires explicit confirmation to cancel an existing scheduled downgrade. | SCR State Engine | `DEC-CR-01` |
| `BR-ELIG-01` | A workspace with a required invoice in `PAST_DUE` may not create a new upgrade or downgrade request until payment recovery succeeds. | Subscription Core | `DEC-ELIG-01` |
| `BR-PRICE-01` | The Billing System calculates member charges, proration, VAT/tax, applicable discounts and the final payable amount. A quote expires after exactly 15 minutes, or immediately when any pricing input changes: target plan, active billable-member count, billing cycle, coupon/discount input, or applicable tax context. Confirmation requires a recalculated quote. | Billing System | `DEC-ARCH-01` · `DEC-PRICE-01` |
| `BR-UPG-01` | An upgrade is complete only after verified payment and successful target-plan entitlement activation. If payment succeeds but activation fails, retain the payment result, set `ACTIVATION_PENDING`, retry activation and never charge again. Duplicate callbacks return the original result through the idempotency key. | ApproveFlow Orchestrator / Entitlement Service | `DEC-UPG-01` · `DEC-UPG-02` |
| `BR-DOWN-01` | A downgrade takes effect only at the current billing-cycle end. The user may cancel it at any time before the Effective Date. | Subscription Core / Scheduler | `DEC-DOWN-01` |
| `BR-DOWN-02` | Apply **Soft Enforcement**: an over-quota workspace may schedule and complete a downgrade. Preserve all existing data; after the Effective Date, block only actions that create usage above the target-plan quota. | Entitlement Service | `DEC-DOWN-02` · `DEC-DATA-01` |
| `BR-ENT-01` | After downgrade, preserve existing configurations. Workflows, integrations or capabilities unsupported by the target plan become paused or read-only according to the entitlement matrix. | Entitlement Service | `DEC-DOWN-03` |
| `BR-GRACE-01` | A verified recurring-payment failure starts a fixed **30-day Grace Period (720 hours)**. Normal workspace access remains available, but new plan changes are blocked. | ApproveFlow State Engine | `DEC-GRACE-01` |
| `BR-REC-01` | If a required invoice remains unpaid after 30 days, set the workspace to `RESTRICTED` and apply read-only access. After all required invoices are paid, set the workspace to `ACTIVE` and restore full access automatically without an additional fee. | ApproveFlow Orchestrator / Access Service | `DEC-REC-01` |

## 2. Decision Tables

Conditions use the **C** prefix

Actions and outcomes use the **A** prefix.

“—” means the condition is not evaluated because an earlier condition already determines the result.

### A. Downgrade Eligibility

Evaluation order: authorization → rank → debt status → request conflict → quota impact.

| **Rule ID** | **C1: Authorized?** | **C2: Lower Rank?** | **C3: Past Due?** | **C4: Pending SCR?** | **C5: Over Quota?** | **A1: Decision** | **A2: Business Outcome** | **API Result** | **Related BR** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DT-DOWN-01` | No | — | — | — | — | Reject | Permission denied | `403 SUB_ACCESS_FORBIDDEN` | `BR-AUTH-01` |
| `DT-DOWN-02` | Yes | No | — | — | — | Reject | Invalid plan transition | `400 SUB_TARGET_PLAN_INVALID` | `BR-CHANGE-01` |
| `DT-DOWN-03` | Yes | Yes | Yes | — | — | Reject | Payment recovery required | `409 SUB_CHANGE_NOT_ELIGIBLE` | `BR-ELIG-01` |
| `DT-DOWN-04` | Yes | Yes | No | Yes | — | Reject | Resolve existing SCR | `409 SUB_CHANGE_REQUEST_CONFLICT` | `BR-CHANGE-02` |
| `DT-DOWN-05` | Yes | Yes | No | No | No | Allow | Standard scheduling at billing-cycle end | `200 OK` | `BR-DOWN-01` |
| `DT-DOWN-06` | Yes | Yes | No | No | Yes | Allow with warning | Schedule with Soft Enforcement | `200 OK` + over-quota warning | `BR-DOWN-02` |

### B. Upgrade Payment & Activation Outcome

Payment outcome is evaluated before entitlement activation. Duplicate callbacks never create another charge or activation.

| **Rule ID** | **C1: Payment Result** | **C2: Duplicate?** | **C3: Entitlement Result** | **A1: SCR State** | **A2: Customer Outcome** | **A3: Next Trigger** | **Related BR** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DT-UPG-01` | Success | No | Success | `APPLIED` | Show payment and activation success; target plan is active. | Send receipt and completion notification. | `BR-UPG-01` |
| `DT-UPG-02` | Success | No | Failed / Timeout | `ACTIVATION_PENDING` | Confirm payment received; activation is still in progress. | Start background activation retry; expose manual retry; escalate on exhaustion. | `BR-UPG-01` |
| `DT-UPG-03` | Failed | No | Not triggered | `PAYMENT_FAILED` | Show failure and retain the current plan. | Allow payment-method update or payment retry. | `BR-UPG-01` |
| `DT-UPG-04` | Pending / Unknown | No | Not triggered | `PAYMENT_PENDING` | Show processing status; retain the current plan. | Wait for the next verified webhook or reconcile payment status. | `BR-UPG-01` |
| `DT-UPG-05` | Success | Yes | Existing result | No state change | Return the original SCR result. | Acknowledge the duplicate; do not charge or activate again. | `BR-CHANGE-02` · `BR-UPG-01` |

## 2. Rule Traceability Matrix

This table is a navigation index. [Requirements Map — Main Cockpit](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/7110657/Main+Cockpit+Change-Ready) remains the single end-to-end traceability source.

| **Business Rule** | **Core Boundary / Behavior** | **Primary BPMN** | **User Story** | **Handled Exception** |
| --- | --- | --- | --- | --- |
| `BR-AUTH-01` | RBAC validation at API entry | Diagrams 2, 3, 4 | `US-02`, `US-04`, `US-05`, `US-06` | Authorization failure |
| `BR-BILL-01` | Billing System owns member count, pricing and invoice status | Diagrams 2, 4 | `US-02`, `US-03`, `US-06` | `EX-INT-01` |
| `BR-CHANGE-01` | Rank-delta classification | Diagrams 2, 3 | `US-01`, `US-02`, `US-04` | No state change |
| `BR-CHANGE-02` | Single non-terminal request and idempotent processing | Diagrams 2, 3 | `US-02`–`US-05` | `EX-UPG-04` |
| `BR-ELIG-01` | Debt-settlement eligibility gate | Diagrams 2, 3 | `US-01`, `US-02`, `US-04` | No state change |
| `BR-PRICE-01` | 15-minute quote TTL and pricing-input invalidation | Diagram 2 | `US-02` | `EX-INT-01` |
| `BR-UPG-01` | Verified payment-to-entitlement orchestration | Diagram 2 | `US-03` | `EX-UPG-01`–`EX-UPG-04` |
| `BR-DOWN-01` | Cycle-end scheduling, cancellation and execution | Diagram 3 | `US-04`, `US-05` | `EX-DOWN-02` |
| `BR-DOWN-02` | Soft quota enforcement with zero data deletion | Diagram 3 | `US-04` | `EX-DOWN-01` |
| `BR-ENT-01` | Preserve data; pause unsupported features | Diagram 3 | `US-04` | `EX-DOWN-02` |
| `BR-GRACE-01` | Fixed 30-day / 720-hour recovery timer | Diagram 4 | `US-06` | `EX-REC-01` |
| `BR-REC-01` | Restrict and restore access from verified invoice status | Diagram 4 | `US-06` | `EX-REC-02`–`EX-REC-03` |

## 3. Related Artefacts

- [Decision Log](https://mindyworkflows.atlassian.net/wiki/x/Y4AD) — source decisions.
- [Process Models](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131226/Process+Models) — operational flow and system boundaries.
- [State Transition Model](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131234/State+Transition+Model+Specification) — lifecycle transitions.
- [Exception Matrix](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/5373964/Exception+Matrix+Failure+Recovery) — exception ownership and recovery.
- [API, SQL & Sequence Analysis](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) — canonical API errors and integration contracts.
