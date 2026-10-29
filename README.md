# ApproveFlow Subscription Specification

> Repository baseline exported exclusively from Confluence folder `98311`.
>
> Evidence status: **BASELINED — SIMULATION** / **DESIGNED — NOT EXECUTED** unless a source section states otherwise.

> **Package status: BLOCKED.** Confluence currently has no Postman collection JSON or n8n workflow JSON attachment. Add both files to the Technical PoC page before creating the release tag.

## Repository navigation

- [Scope and decisions](docs/01-scope-and-decisions/decisions-log.md)
- [Process and states](docs/02-process-and-states/state-machines.md)
- [Specifications](docs/03-specifications/user-stories-ac.md)
- [Testing and UAT](docs/04-testing-and-uat/uat-specification.md)
- [PoC automation](poc-automation/README.md)
- [Source manifest](docs/source-manifest.yaml)

---

## Confluence baseline

> Source: [01. Project Home & Portfolio Summary](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98315) · Content ID `98315` · Version `20` · Status `current`

**ApproveFlow — B2B SaaS Subscription Engine**  
A traceable requirement baseline and architectural specification for self-service subscription lifecycle.

BASELINED — SIMULATION **Ready for Engineering walkthrough; not production-ready evidence.**

# 1. Project Snapshot & Metadata

| **Field** | **Specification Value** |
| --- | --- |
| Product | ApproveFlow — B2B client approval platform |
| Domain | SaaS subscription billing, payment recovery, entitlement and access lifecycle |
| Project type | IT Business Analysis portfolio simulation |
| Author role | Technical Business Analyst |
| Primary platform | Desktop Web; modern browser experience |
| Delivery phase | Requirement baseline and engineering hand-off |
| Baseline status | BASELINED — SIMULATION |
| Verified delivery links | [Jira Backlog](https://mindyworkflows.atlassian.net/jira/software/projects/SUB/boards/2?filter=&groupBy=none&atlOrigin=eyJpIjoiNWJkMmQyNThlODE4NGY3N2I3ZmFiNDUwNjZmZmFmOGQiLCJwIjoiaiJ9) · [Figma Canvas](https://www.figma.com/design/ZBPovUXDJwxaT3sJhn2Zu9/ApproveFlow-%E2%80%94-SaaS-Subscription-Management?m=auto&t=KIGQ4IVQoEtASNq1-6) · [Postman Mock Collection](https://mindy-workflows-4402981.postman.co/workspace/af7a4bfd-a892-4d38-8534-cee67ef4f9e4/collection/59058682-f1c3c4a6-ed79-43f7-99f2-5cd9b1b03669) |

# 2. Executive Summary & Business Outcomes

| **View** | **Statement** |
| --- | --- |
| Current state | Subscription changes and recurring-payment recovery rely on manual Support, Finance and Operations hand-offs, increasing latency and inconsistency risk. |
| Target state | Authorized Workspace Owners and Billing Admins can upgrade, schedule or cancel a downgrade, and recover failed recurring payments through traceable state-driven workflows. |
| Business objective | Reduce routine assisted handling while protecting pricing fidelity, payment idempotency, entitlement accuracy, recovery timing and customer data. |

## Measurable Success Targets

**Measurement status:** targets are baselined for future delivery measurement; the portfolio simulation has no production baseline.

| **ID** | **Metric / Guardrail** | **Target** | **Evidence Status** |
| --- | --- | --- | --- |
| `BSM-01` | Self-Service Completion Rate | ≥ 80% | Target only — post-release measurement required |
| `BSM-02` | Support-Assisted Plan-Change Rate | ≤ 20% | Target only — post-release measurement required |
| `BSM-03` | Median Upgrade Activation Time | ≤ 5 minutes | T01 mock run: 45s; not production evidence |
| `BSM-06` | Entitlement Activation Accuracy | 100% | Target only |
| `QG-01` | Duplicate charges | 0 incidents | Design invariant; implementation validation pending |
| `QG-06` | Data loss caused by downgrade | 0 records | Design invariant; SQL/UAT execution pending |

Canonical definitions: [Scope, Stakeholders & Success Metrics](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229417/Scope+Stakeholders+Success+Metrics) · [ROI & Measurement Plan](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/66158/ROI+Measurement+Plan)

# 3. Scope, Boundaries & Architectural Decisions

| **Capability** | **In Scope** | **Boundary / Out of Scope** | **Decision Rationale** |
| --- | --- | --- | --- |
| Self-Service Upgrade | Eligible higher tier, authoritative pricing preview, hosted payment and entitlement activation after verified payment. | Desktop Web only; responsive mobile and native apps excluded. | Focuses the MVP on the B2B billing-admin journey. |
| Scheduled Downgrade | Quota-impact review, cycle-end scheduling, pre-effective-date cancellation and soft enforcement. | No immediate mid-cycle downgrade; annual billing excluded. | Preserves paid value and avoids refund/proration complexity. |
| Payment Failure Recovery | Retry payment, processor-hosted payment-method update, 30-day/720-hour Grace Period, restriction and restoration. | Payment Processor implementation and raw card data remain external. | Keeps sensitive card data outside the ApproveFlow boundary; this is not a PCI certification claim. |
| Pricing Calculation | ApproveFlow requests, receives, validates and displays pricing results. | Billing System calculates members, proration, tax/VAT, discounts and totals. | One financial source of truth prevents duplicated pricing logic. |
| Entitlement & Data | Apply plan capabilities, quota and access outcomes after approved state transitions. | Downgrade or restriction must not delete retained customer data. | Soft enforcement restricts new over-quota activity while preserving data. |

**Critical invariants:** one non-terminal Subscription Change Request (SCR) per workspace; no second charge during activation retry; upgrade completes only after entitlement activation; access restores only when no required invoice remains `PAST_DUE`.

**Decision source**: [Architecture & Business Decision Log — 20/20 decisions](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log)

# 4. Plan Structure & Commercial Model

| **Plan** | **Rank** | **Price / Active Member / Month** | **Target Segment** |
| --- | --- | --- | --- |
| Starter | 1 | 39,000 VND | Small teams getting started |
| Basic | 2 | 79,000 VND | Growing teams managing multiple projects |
| Pro | 3 | 149,000 VND | Teams needing advanced automation and governance |

- **Billing:** monthly only, VND; catalogue prices exclude VAT.
- **Upgrade:** immediate only after verified payment and successful entitlement activation.
- **Downgrade:** scheduled at billing-cycle end; existing data is preserved.

**Configuration source**: [Plan Catalogue & Entitlement Matrix](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/8192008/Plan+Catalogue+Entitlement+Matrix)

# 5. Core Capabilities & User Story Mapping

| **Epic / Capability** | **Business Outcome** | **User Stories** |
| --- | --- | --- |
| [Epic 1 — Self-Service Upgrade](https://mindyworkflows.atlassian.net/browse/SUB-1) | Review authoritative pricing, pay safely and receive the purchased entitlement without duplicate charge. | [US-01 — View Subscription & Plans](https://mindyworkflows.atlassian.net/browse/SUB-4) [US-02 — Preview & Confirm Upgrade](https://mindyworkflows.atlassian.net/browse/SUB-5) [US-03 — Complete Upgrade & View Outcome](https://mindyworkflows.atlassian.net/browse/SUB-6) |
| [Epic 2 — Scheduled Downgrade](https://mindyworkflows.atlassian.net/browse/SUB-2) | Assess quota impact, schedule the lower tier and cancel before the effective date. | [US-04 — Schedule Downgrade](https://mindyworkflows.atlassian.net/browse/SUB-7) [US-05 — Cancel Scheduled Downgrade](https://mindyworkflows.atlassian.net/browse/SUB-8) |
| [Epic 3 — Payment Failure Recovery](https://mindyworkflows.atlassian.net/browse/SUB-3) | Recover recurring payment within Grace Period and restore access after required debt is cleared. | [US-06 — Recover from Payment Failure](https://mindyworkflows.atlassian.net/browse/SUB-9) |

**Baseline coverage:** 3 Epics · 6 User Stories · 40 Acceptance Criteria.

# 6. Project Artifact Map & Verification Status

| **Layer** | **Canonical Artefact** | **Coverage** | **Verification Status** |
| --- | --- | --- | --- |
| Vision, scope & governance | [Business Brief](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229409/Business+Brief) · [Decision Log](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) | 20 approved simulation decisions | BASELINED |
| Process & state | [BPMN Process Models](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131226/Process+Models) · [State Transition Model](https://mindyworkflows.atlassian.net/wiki/x/ogAC) | As-Is + 3 To-Be workflows; Subscription and SCR FSMs | BASELINED |
| Requirements & traceability | [Functional Requirements](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229429/Functional+Requirements) · [Requirements Map — Main Cockpit](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/7110657/Main+Cockpit+Change-Ready) | 6 Stories / 40 AC; end-to-end trace | BASELINED |
| UX & interaction | [Wireframes & UI States](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/66150/Wireframes+UI+States) | Default, loading, error, blocked and success states across 3 journeys | BASELINED |
| Data & rules | [ERD & Data Dictionary](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229445/ERD+Data+Dictionary) · [Business Rules & Decision Tables](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98325/Business+Rules+Decision+Tables) | Logical model, enums, invariants and decision logic | BASELINED — SIMULATION |
| API, sequence & SQL | [API, SQL & Sequence Analysis](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) | API-01–08, SD-01–03, SQL-01–08 | DESIGNED — NOT EXECUTED |
| Business acceptance | [UAT Specification](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98340/User+Acceptance+Testing+UAT+Specification) | 9 Must scenarios and sign-off gates | DESIGNED — NOT EXECUTED |
| Technical prototype | [Paid Upgrade Activation Monitoring PoC](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/14909445/10.+Technical+PoC+Paid+Upgrade+Activation+Monitoring) | 8 author-run mock scenarios; limited US-03 monitoring slice | MANUAL SIMULATION EXECUTED |

# 7. Current Readiness & Engineering Hand-off

**Ready for walkthrough**

- Scope, boundaries and 20 decisions are baselined.
- Process, state, rule, requirement, UX and logical data models are traceable.
- 6 Stories and 40 AC provide implementation and QA entry points.

**Evidence still required**

- Executed API integration and SQL invariant results.
- UAT execution and business sign-off.
- Independent, accessible PoC run artefacts.
- Production metrics, security validation and operational readiness.

## Hand-off Contract

| **Before implementation** | **During delivery** | **Release gate** |
| --- | --- | --- |
| Engineering confirms feasibility, service ownership, API error contracts, retry/backoff and observability. | Dev/QA preserve traceability from decision and rule through Story/AC, state transition, test and defect. | No production-readiness claim until integration, SQL, UAT, security and operational evidence are executed and reviewable. |

# 8. Portfolio Competencies Demonstrated

| **Competency** | **Evidence** |
| --- | --- |
| Requirements Engineering & Traceability | [Requirements Map — Main Cockpit](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/7110657/Main+Cockpit+Change-Ready) traces 5 business objectives, 12 business rules and 34 functional requirements through 3 Epics, 6 Jira Stories and 40 acceptance criteria to SQL-01–08 and 9 UAT scenarios. |
| Process, State & Boundary Modeling | [4 BPMN collaboration models](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131226/Process+Models) (1 As-Is, 3 To-Be), [2 domain state machines](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131234/State+Transition+Model+Specification) (Subscription and SCR) and [3 sequence diagrams](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) cover system ownership, asynchronous callbacks, retry, timeout and exception paths. |
| Data Integrity & Integration Reasoning | [Logical ERD and Data Dictionary](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229445/ERD+Data+Dictionary) plus [API-01–08 and SQL-01–08](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) specify payment idempotency, conditional invoice/SCR parentage, entitlement consistency and the zero-data-loss downgrade invariant. |
| Engineering Integrity | [20/20 simulation decisions](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) are baselined; the [Technical PoC records 8/8 author-run mock scenarios](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/14909445/10.+Technical+PoC+Paid+Upgrade+Activation+Monitoring); API/SQL validation and 9 UAT scenarios remain DESIGNED — NOT EXECUTED, with no production-readiness claim. |

