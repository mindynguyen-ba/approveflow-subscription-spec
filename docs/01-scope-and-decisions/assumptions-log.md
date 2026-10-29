> Source: [Assumption Register & Decision Traceability](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131269) · Content ID `131269` · Version `15` · Status `current`

**BASELINED REGISTER** — 25/25 assumptions classified: 24 superseded by approved simulation decisions and 1 validated. No assumption remains open.

Assumptions are historical analysis inputs; linked decisions are the current requirement source of truth.

**Alignment risk:** `DEC-GRACE-01` in the Decisions Log still says “one calendar month”; the current cross-artifact implementation baseline is **30 days (720 hours)**. Align the Decisions Log before final governance sign-off.

# 1. Scope & System Architecture

| **ID** | **Initial Assumption** | **Status** | **Current Source of Truth** | **Resolution & Business Impact** |
| --- | --- | --- | --- | --- |
| `ASM-SCOPE-01` | Monthly billing only; annual billing is excluded. | SUPERSEDED | [DEC-SCOPE-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Keeps MVP billing cycles bounded and avoids annual-proration complexity. |
| `ASM-BILL-01` | Billing System calculates charges, proration, tax/VAT, discounts and total. | SUPERSEDED | [DEC-ARCH-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | ApproveFlow displays the authoritative quote and does not duplicate pricing logic. |
| `ASM-PAY-01` | Payment-method update and retry use a processor-hosted portal. | SUPERSEDED | [DEC-BOUNDARY-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Preserves the PCI boundary: ApproveFlow never stores or handles raw card data. |
| `ASM-ROLE-01` | Only Workspace Owners and Billing Admins may manage plan changes. | SUPERSEDED | [DEC-ROLE-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | RBAC blocks Members and Guests from initiating financial changes. |
| `ASM-OPS-01` | Support, Finance and Platform Admin own defined operational fallbacks. | SUPERSEDED | [DEC-OPS-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Assigns recovery ownership for billing, customer and entitlement exceptions. |

# 2. Plan Change & Concurrency Control

| **ID** | **Initial Assumption** | **Status** | **Current Source of Truth** | **Resolution & Business Impact** |
| --- | --- | --- | --- | --- |
| `ASM-CR-01` | Only one non-terminal Subscription Change Request (SCR) is allowed per workspace. | SUPERSEDED | [DEC-CR-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Prevents race conditions and conflicting plan transitions. |
| `ASM-CR-02` | An immediate upgrade requires cancellation of an existing scheduled downgrade. | SUPERSEDED | [DEC-CR-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | The scheduled SCR must close before a new upgrade SCR is created. |
| `ASM-PRICE-01` | The pricing preview contains every applicable billing component. | SUPERSEDED | [DEC-ARCH-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log), [DEC-PRICE-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Makes the financial commitment transparent before confirmation. |
| `ASM-PRICE-02` | The pricing preview expires after 15 minutes or when pricing inputs change. | SUPERSEDED | [DEC-PRICE-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Prevents stale price, member-count or tax inputs from being confirmed. |
| `ASM-UPG-01` | Upgrade completes only after target entitlements activate successfully. | SUPERSEDED | [DEC-UPG-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Separates payment success from entitlement completion: ACTIVATION\_PENDING → APPLIED. |
| `ASM-UPG-02` | Activation failure can be retried without charging again. | SUPERSEDED | [DEC-UPG-02](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Retains the successful payment and makes recovery idempotent. |
| `ASM-DOWN-01` | Downgrade takes effect at the end of the current billing cycle. | SUPERSEDED | [DEC-DOWN-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Preserves the paid benefits of the higher plan until cycle end. |
| `ASM-DOWN-02` | An over-quota workspace may still schedule a downgrade. | SUPERSEDED | [DEC-DOWN-02](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Uses soft enforcement: warn clearly, but do not block scheduling. |
| `ASM-DOWN-03` | Excess data remains stored while unsupported future actions are restricted. | SUPERSEDED | [DEC-DOWN-03](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Preserves existing data and enforces the lower plan prospectively. |
| `ASM-DATA-01` | Downgrade never deletes existing customer data. | SUPERSEDED | [DEC-DATA-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Establishes the data-retention invariant for every downgrade path. |

# 3. Payment Recovery & Access Management

| ID | Initial Assumption | Status | Current Source of Truth | Resolution & Business Impact |
| --- | --- | --- | --- | --- |
| `ASM-ELIG-01` | A workspace with a Past Due invoice cannot create a plan-change request. | SUPERSEDED | [DEC-ELIG-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Stops new billing commitments while required debt remains unresolved. |
| `ASM-GRACE-01` | Grace Period was initially assumed to last one calendar month. | SUPERSEDED | [DEC-GRACE-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Current implementation baseline is 30 days (720 hours); the linked Decisions Log wording still requires alignment. |
| `ASM-GRACE-02` | Current workspace access remains during Grace Period; plan changes are blocked. | SUPERSEDED | [DEC-GRACE-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Protects customer continuity while preventing additional billing-state changes. |
| `ASM-REC-01` | Access restores only when no required invoice remains Past Due. | SUPERSEDED | [DEC-REC-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Requires all mandatory debt to clear before full access is restored. |
| `ASM-REC-02` | Access-restoration failure can be retried without charging again. | SUPERSEDED | [DEC-REC-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Separates payment recovery from access recovery and prevents duplicate charges. |

# 4. Quotas, Metrics & Project Baseline

| **ID** | **Initial Assumption** | **Status** | **Current Source of Truth** | **Resolution & Business Impact** |
| --- | --- | --- | --- | --- |
| `ASM-BILL-02` | Active, non-guest members are billable at preview time. | SUPERSEDED | [DEC-BILL-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Defines the billable population used by pricing and proration. |
| `ASM-QUOTA-01` | Monthly quotas reset at the billing-cycle boundary. | SUPERSEDED | [DEC-QUOTA-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Aligns recurring quota windows with subscription billing. |
| `ASM-QUOTA-02` | Unlimited means no plan-enforced hard quota in the MVP. | SUPERSEDED | [DEC-QUOTA-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Avoids introducing an undefined fair-use threshold in phase one. |
| `ASM-MET-01` | No verified production baseline exists for this simulation project. | VALIDATED | [ROI & Measurement Plan](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/66158/ROI+Measurement+Plan) | Confirms that portfolio metrics are analytical targets, not production evidence. |
| `ASM-MET-02` | Median upgrade activation target is five minutes. | SUPERSEDED | [DEC-MET-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | Defines a measurable service objective from payment success to entitlement activation. |

