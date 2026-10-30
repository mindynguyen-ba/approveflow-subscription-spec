# Scope, Stakeholders & Success Metrics

> Source: [Scope, Stakeholders & Success Metrics](https://mindyworkflows.atlassian.net/wiki/pages/229417) · Content ID `229417`

## In-Scope Workflows

| **Capability** | **Scope** |
| --- | --- |
| Core Plan Overview | View the active tier, renewal date, billing/payment status, quota consumption, plan comparison and change history for Starter, Basic and Pro. |
| Self-Service Upgrade | Select an eligible higher tier, request a prorated preview from the Billing System, pay through the hosted processor, and activate entitlements only after verified payment success. A failed upgrade keeps the current plan active and does not start Grace Period. |
| Scheduled Downgrade | Select an eligible lower tier, review quota impact, schedule or cancel the change before processing, keep the current plan until the cycle boundary, preserve existing data, and restrict only new quota-consuming activity when the target limit is exceeded. |
| Payment Recovery & Grace Period | Detect recurring-payment failure, run a one-month Grace Period, support retry and processor-hosted payment-method update, restrict access after expiry, and restore access after overdue and current invoices are settled. |
| Cross-Capability Controls | Authorize Workspace Owner and Billing Admin actions; allow only one active Subscription Change Request (**SCR**) per workspace; prevent duplicate payment submission and charges; record actor, timestamp, current tier, target tier and outcome; provide safe errors and notifications. |

## Explicit Out of Scope

| **Area** | **Excluded from MVP** |
| --- | --- |
| Commercial & Billing | Annual billing or cycle conversion, annual commitments, multi-currency, standalone discount/tax/VAT calculation, statutory tax invoices, accounting reconciliation, direct refunds and usage-overage charging. ApproveFlow may display values returned by the Billing System. |
| Infrastructure & Security | Raw card-data storage, custom payment-gateway or provider-infrastructure development, and production accounting-system integration. |
| Platforms | Responsive mobile web and native iOS/Android applications. The MVP is Desktop Web only. |

- As-Is Subscription Management Process and three To-Be process models: Upgrade, Scheduled Downgrade, and Payment Failure & Recovery.
- Subscription and SCR state models, decision tables, Business Rule Catalogue, Functional Requirements and Stories.
- Wireframes and UI states, ERD and Data Dictionary, API and Sequence Analysis.
- Acceptance Criteria, UAT scenarios, traceability views and Measurement Plan.

# 2. Constraints & Platform

| **ID** | **Constraint** | **Category** | **Impact** | **Trace Ref** |
| --- | --- | --- | --- | --- |
| `CON-SCOPE-01` | Monthly billing and monthly plan changes only. | Scope | No annual pricing, conversion or commitment workflows. | `DEC-SCOPE-01` |
| `CON-PLAN-01` | Starter, Basic and Pro tiers only. | Product | Custom, legacy and enterprise tiers are excluded. | Plan Catalogue |
| `CON-COMM-01` | Prices are in VND and catalogue prices exclude VAT. | Commercial | Pricing preview displays applicable VAT separately. | Plan Catalogue |
| `CON-ARCH-01` | Billing System is the financial source of truth. | Architecture | ApproveFlow requests, receives and displays billable-member count, proration, tax/VAT, discounts, totals and invoice state; it does not calculate them. | `DEC-ARCH-01` |
| `CON-INT-01` | Payment Processor owns transactions and payment-method data. | Integration / Security | ApproveFlow uses existing APIs or hosted pages and never builds a gateway or stores card data. | `DEC-BOUNDARY-01` |
| `CON-PLAT-01` | Desktop Web only. | Platform | No mobile-specific layout, responsive behavior or acceptance testing. | `DEC-PLAT-01` |

## Platform Support Matrix

| **Platform** | **Supported Roles** | **Scope** |
| --- | --- | --- |
| Desktop Web | Workspace Owner, Billing Admin | Full subscription, billing and recovery workflows. |
| Mobile Web / Native Apps | None | **Out of Scope** — no optimized layouts or acceptance testing. |

# 3. Governance: Stakeholders & Roles

## Stakeholder Matrix

| **Stakeholder** | **Primary Need / Responsibility** | **Influence** |
| --- | --- | --- |
| Workspace Owner | Controls subscription and cost; approves and performs plan changes. | High |
| Billing Admin | Runs plan-change, billing and payment-recovery operations. | High |
| Agency Member | Uses entitled features and responds to contextual quota restrictions. | Low |
| Customer Support | Investigates failed requests and recovery exceptions. | Medium |
| Finance / Billing Owner | Owns pricing, proration and recovery policy correctness. | High |
| Product Owner | Owns MVP scope, priority and business decisions. | High |
| Platform Operations | Maintains plan, quota and entitlement configuration. | Medium |
| Business Analyst | Maintains requirement clarity, decisions and traceability. | Medium |
| Development Team | Confirms feasibility and implements approved behavior. | Medium |
| QA | Designs and executes validation scenarios. | Medium |

## System Dependencies

- **Billing System:** invoice states, billable-member count, line items, proration, discounts, tax/VAT and final payable amount.
- **Payment Processor:** tokenized payment data, hosted payment-method update, authentication and transaction execution.
- **Entitlement Service:** applies tier capabilities and quota limits.
- **Usage Service:** supplies current quota consumption.
- **Notification Service:** sends subscription and payment-status notifications.

## Role-Based Access Matrix

| **Capability** | **Workspace Owner** | **Billing Admin** | **Agency Member** |
| --- | --- | --- | --- |
| View plan details, billing status and billing-level quota | Yes | Yes | No |
| View contextual quota warnings | Yes | Yes | Yes |
| Upgrade plan and confirm payment | Yes | Yes | No |
| Schedule or cancel a future downgrade | Yes | Yes | No |
| Retry payment or open processor-hosted payment update | Yes | Yes | No |
| View SCR history | Yes | Yes | No |
| Use active workspace entitlements | Yes | Yes | Yes |

# 4. Business Success Metrics

**Measurement status:** Portfolio simulation has no production baseline. BSM-05 and BSM-08 establish their target from the first reliable post-release measurement window; detailed formulas remain in the Measurement Plan.

| **ID** | **Alignment** | **Metric** | **Target** | **Data Source** | **Review Window** |
| --- | --- | --- | --- | --- | --- |
| `BSM-01` | `BO-01` | Self-Service Completion Rate | ≥ 80% | SCR events | Monthly |
| `BSM-02` | `BO-01` | Support-Assisted Plan-Change Rate | ≤ 20% | Support tickets + SCRs | Monthly |
| `BSM-03` | `BO-02` | Median Upgrade Activation Time | ≤ 5 minutes | Payment Attempt + Entitlement Activation | Weekly, then monthly |
| `BSM-04` | `BO-03` | Scheduled Downgrade Completion Rate | ≥ 95% | SCRs at effective date | Monthly |
| `BSM-05` | `BO-04` | Payment Recovery Within Grace Period | Establish from baseline | Invoice + Payment Attempt | Monthly |
| `BSM-06` | `BO-02` | Entitlement Activation Accuracy | 100% | Subscription + Entitlement Activation | Monthly |
| `BSM-07` | `BO-05` | Restriction Timing Accuracy | 100% | Grace Period expiry + Access Transition | Monthly |
| `BSM-08` | `BO-05` | Median Access Restoration Time | Establish from baseline | Payment Attempt + Access Transition | Monthly |

Formula definitions and post-release evaluation are maintained in [ROI & Measurement Plan](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/66158/ROI+Measurement+Plan).

# 5. Quality Guardrails / System Invariants

These invariants must remain intact from Business Rule through implementation and validation.

| **ID** | **Invariant** | **Target** | **Verification** |
| --- | --- | --- | --- |
| `QG-01` | **Zero duplicate charges:** repeated submission or retry must not create a second charge. | 0 incidents | Idempotency and webhook-deduplication scenarios |
| `QG-02` | **Zero invalid downgrades:** no downgrade is applied when eligibility, state or effective-date rules fail. | 0 incidents | Eligibility and state-transition scenarios |
| `QG-03` | **Pricing-preview fidelity:** approved proration examples match Billing System results. | 100% accuracy | Calculation test dataset |
| `QG-04` | **Entitlement consistency:** plan and entitlement outcomes match approved rules. | 100% accuracy | UAT scenarios and entitlement checks |
| `QG-05` | **Grace Period compliance:** access is not restricted before expiry and follows the approved recovery policy. | 100% accuracy | Recovery timing scenarios |
| `QG-06` | **Zero data loss on downgrade:** existing customer data is never deleted directly by a downgrade. | 0 records | Downgrade data-integrity scenarios |

