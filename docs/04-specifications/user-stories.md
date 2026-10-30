# Jira Story Index

> Source: [Jira Story Index](https://mindyworkflows.atlassian.net/wiki/pages/229437) · Content ID `229437`

Traceable index of the six User Stories maintained in Jira. Detailed story narratives and Gherkin Acceptance Criteria remain in Jira; this page defines the canonical Epic coverage, story boundary, SCR lifecycle outcome and verification target.

**Canonical upgrade boundary:** US-02 ends with a valid 15-minute quote held as `Draft / In-Memory`. US-03 begins when the user explicitly confirms, persists the SCR and moves it to `PAYMENT_PENDING`.

## 1. Domain Terminology Guardrails

- **SCR — Subscription Change Request:** business-domain object representing an end-user request to upgrade or downgrade a subscription. The **S** intentionally distinguishes this entity from project-governance change records.
- **CR in technical contracts:** stable database, API and state-transition identifiers retain the existing `CR` naming for backward compatibility and concise code, including `subscription_change_requests` and `ST-CR-01`–`ST-CR-13`. In business prose, these records are called SCRs.
- **CR / RCR in governance:** Change Record / Requirement Change Request used to control changes to scope, requirements and delivery artifacts. It is not the subscription transaction entity.

## 2. Epic Coverage & Architectural Mapping

| **Epic** | **Capability** | **Primary BPMN** | **Scope & Core Responsibility** |
| --- | --- | --- | --- |
| [**SUB-1**](https://mindyworkflows.atlassian.net/browse/SUB-1) | **Self-Service Upgrade** | Diagram 2 — To-Be Upgrade | Discover plans, validate eligibility, preview proration, confirm payment and activate target-plan entitlements. |
| [**SUB-2**](https://mindyworkflows.atlassian.net/browse/SUB-2) | **Scheduled Downgrade** | Diagram 3 — To-Be Downgrade | Assess quota impact, schedule downgrade at cycle end, apply soft enforcement and allow cancellation before execution. |
| [**SUB-3**](https://mindyworkflows.atlassian.net/browse/SUB-3) | **Payment Failure Recovery** | Diagram 4 — To-Be Recovery | Run the 30-day / 720-hour grace period, support self-service recovery, restrict overdue workspaces to read-only and restore access after payment. |

## 3. User Story Master Index

| **Jira / Story** | **User Story** | **Primary Actor** | **System Behavior** | **SCR Lifecycle Result** | **Verification Target** |
| --- | --- | --- | --- | --- | --- |
| [**SUB-4**](https://mindyworkflows.atlassian.net/browse/SUB-4) US-01 | **View Current Subscription & Available Plans** | All active members | Discovery only. Return the current subscription, plan catalogue, usage and valid actions. | **SCR: N/A** Subscription: no change | Show the correct current plan, usage and action classification: `Upgrade`, `Downgrade` or `Current`. |
| [**SUB-5**](https://mindyworkflows.atlassian.net/browse/SUB-5) US-02 | **Configure & Preview Upgrade Quote** | Workspace Owner Billing Admin | **SB-UPG-01–02**. Verify the user has permission to upgrade, validate eligibility, then request and display the Billing System quote. | **SCR: Draft / In-Memory** No persisted SCR Quote TTL: 15 minutes | Block ineligible or `PAST_DUE` subscriptions. Display billable members, proration, VAT, coupon and final payable amount. Recalculate when the quote expires or pricing inputs change. |
| [**SUB-6**](https://mindyworkflows.atlassian.net/browse/SUB-6) US-03 | **Confirm Upgrade & Process Payment** | Workspace Owner Billing Admin | **SB-UPG-03–08**. Explicit confirmation persists one SCR and opens payment. Verified callbacks drive payment and activation outcomes. | **SCR:** `PAYMENT_PENDING` → `PAYMENT_FAILED` / `ACTIVATION_PENDING` → `ACTIVATION_FAILED` / `APPLIED` Subscription changes only after activation succeeds. | Successful activation applies the target plan. Failed payment keeps the current plan and retries on the same SCR. Failed activation recovers without a second charge. Duplicate submissions and callbacks remain idempotent. |
| [**SUB-7**](https://mindyworkflows.atlassian.net/browse/SUB-7) US-04 | **Validate Usage & Schedule Downgrade** | Workspace Owner Billing Admin | **SB-DOWN-01–03, 05–07**. Validate downgrade impact, schedule execution at cycle end and apply soft enforcement when usage exceeds the target quota. | **SCR:** Draft → `SCHEDULED` → `APPLIED` / `EXECUTION_FAILED` Subscription remains current until execution. | Preserve existing data. After the effective date, over-quota workspaces cannot create new resources until usage returns within the target-plan limit. |
| [**SUB-8**](https://mindyworkflows.atlassian.net/browse/SUB-8) US-05 | **Cancel Scheduled Downgrade** | Workspace Owner Billing Admin | **SB-DOWN-04**. Cancel the scheduled execution before the effective date and de-schedule the job. | **SCR:** `SCHEDULED` → `CANCELLED` (terminal) Subscription remains on the retained plan. | Close the same SCR, preserve current plan and entitlements, and send cancellation confirmation. |
| [**SUB-9**](https://mindyworkflows.atlassian.net/browse/SUB-9) US-06 | **Recover from Recurring Payment Failure** | Billing Admin | **SB-REC-01–06**. Recurring-payment failure changes Subscription and Invoice states directly; it is not a plan-change transaction. | **SCR: N/A** Subscription: `ACTIVE` ↔ `PAST_DUE` → `RESTRICTED` Grace period: 30 days / 720 hours | Successful repayment clears warnings and restores access. Expiry of the grace period moves the workspace to read-only without deleting data. |

## 4. Traceability & Engineering Invariants

1. **One Open SCR per Workspace:** At most one persisted, non-terminal SCR may exist per Workspace at any given time. Open and recoverable states comprise `PAYMENT_PENDING`, `PAYMENT_FAILED`, `ACTIVATION_PENDING`, `ACTIVATION_FAILED`, and `SCHEDULED`. An in-memory pricing preview (quote draft) is transient and does not constitute a persisted SCR.
2. **Explicit Disambiguation:** Use **SCR** (*Subscription Change Request*) exclusively for end-user plan transition transactions. Use **CR / RCR** (*Change Record / Requirement Change Request*) strictly for project governance and scope control. Stable technical contracts and schema identifiers (e.g., `ST-CR-xx`, `subscription_change_requests`) may retain the `CR` prefix, provided their domain meaning is explicitly defined as SCR.
3. **Defect Tagging Discipline:** Every QA defect logged in Jira must explicitly reference at least one canonical Business Rule (`BR-xxx`), Exception Scenario (`EX-xxx`), or State Transition (`ST-CR-xxx`).
4. **Source of Truth Ownership:** Jira is the sole authoritative source for full User Stories, technical tasks, and BDD Acceptance Criteria (Gherkin). This specification index owns end-to-end requirement traceability, story slicing boundaries, and lifecycle mapping; any scope or boundary adjustment must be synchronized across both repositories within the same change-control cycle.

