# Business Brief

> Source: [Business Brief](https://mindyworkflows.atlassian.net/wiki/pages/229409) · Content ID `229409`

ApproveFlow is a fictional B2B client-approval platform for teams managing social media and content operations. This Business Brief defines an MVP that enables authorized Workspace Owners and Billing Admins to manage eligible subscription changes through a transparent self-service experience, reducing operational dependency on Customer Support, Finance and Operations.

- **Core scope:** Self-Service Upgrade, Scheduled Downgrade and Payment Failure Recovery.
- **Architectural boundary:** ApproveFlow is the customer-facing workflow, orchestration and state-management layer. It does not replace the Billing System or Payment Processor.

# 2. Product Context & Entitlement Structure

ApproveFlow allows agencies and content teams to prepare content, submit it for client review, collect feedback and track approval status within a shared multi-tenant workspace. Each workspace operates under a subscription plan that controls feature access and usage quotas.

| **Plan-controlled entitlements** | **Roles and permissions** |
| --- | --- |
| - Active projects and storage allowance. - Workspace members and client approvers. - Approval-history retention. | - **Workspace Owner / Billing Admin:** manage eligible plan changes and billing actions. - **Agency Member:** uses active entitlements but cannot perform billing-level actions. |

# 3. Strategic Alignment Matrix

**Core problem:** subscription plan changes are not sufficiently self-service. **Supporting problem:** payment failure and workspace-access recovery require manual operational handling.

| **Objective / Source** | **Current pain point** | **Business impact** | **Target state** | **Success metric** |
| --- | --- | --- | --- | --- |
| **BO-01**BP-01, BP-02 | **Manual, opaque plan changes.** Eligible customers must contact Support and have limited visibility into price, quota impact, effective date and request status. | Longer completion time, repeated contact, abandoned requests, billing disputes and higher Support workload. | Authorized users can complete eligible plan changes independently after reviewing price, quota and effective-date impact, then track the resulting status. | - Self-Service Completion Rate - Support-Assisted Plan-Change Rate |
| **BO-02**BP-03 | **Delayed entitlement activation.** Upgrade payment and entitlement activation require coordination across systems or internal teams. | Delayed access to paid features and risk of incorrect entitlements. | Successful payment results in prompt and accurate entitlement activation. | - Median Upgrade Activation Time - Entitlement Activation Accuracy |
| **BO-03**BP-04 | **Manual downgrade handling.** Downgrade eligibility, scheduling and execution may be handled manually. | Incorrect effective dates, invalid downgrade states and inconsistent quota enforcement. | Eligible downgrades are scheduled and executed reliably at the correct billing-cycle boundary. | - Scheduled Downgrade Completion Rate - Invalid Downgrade Execution Rate |
| **BO-04**BP-05 | **Fragmented payment recovery.** Failed recurring payments are followed up through email, CRM or spreadsheets. | Missed deadlines, inconsistent follow-up and unnecessary operational effort. | Billing Admins can view the failure, update payment details through the Payment Processor and retry payment without Customer Support coordination. | - Payment Recovery Within Grace Period - Support-Assisted Recovery Rate |
| **BO-05**BP-06 | **Inconsistent access control.** Workspace restriction and restoration depend on manual coordination with Platform Admins. | Customers may retain access too long or wait unnecessarily after paying. | Workspace restriction and restoration occur automatically according to payment and Grace Period status. | - Restriction Accuracy - Median Access Restoration Time |

# 4. Scope & System Boundaries

## In scope — orchestrated by ApproveFlow

- Self-service plan comparison, eligibility and price, quota and effective-date preview.
- Upgrade submission, Scheduled Downgrade and cancellation.
- Subscription-change and payment-failure status visibility.
- Customer-facing payment-method update and retry orchestration through the Payment Processor.
- Grace Period deadline tracking, automatic workspace restriction and eligible access restoration.

## Retained systems — source of truth

- **Billing System:** owns invoice generation, price, proration, discount, tax/VAT, totals and financial ledger records.
- **Payment Processor:** owns payment-method storage and transaction execution. ApproveFlow only initiates requests and handles verified outcomes.

## Explicit exclusions

- Building a new payment gateway or storing payment credentials inside ApproveFlow.
- Replacing the Billing System or redesigning the complete invoicing process.
- Accounting reconciliation, tax filing, refund processing or dispute tooling.
- Native mobile client support; the MVP is scoped to Desktop Web.

**Detailed scope:** [Scope, Stakeholders & Success Metrics](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229417/Scope+Stakeholders+Success+Metrics)

# 5. Assumptions & Governance Note

This brief establishes analysis hypotheses for a fictional portfolio simulation. Pain points, impacts and unverified baselines are assumptions—not verified production findings.

Unverified statements are maintained in the Assumption Register and resolved through Open Questions, supporting evidence and recorded decisions. Baselined requirements and traceability are governed through the Decision Log and Requirements Traceability Cockpit.

- [Assumptions](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131269/Assumption+Register+Decision+Traceability)
- [Open Questions](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/360481/Open+Questions+Clarifications+Register)
- [Decisions Log](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log)
