# Communication & Decision Evidence

> Source: [Communication & Decision Evidence](https://mindyworkflows.atlassian.net/wiki/pages/2981890) · Content ID `2981890` · Version `6` · Status `current`

**Ambiguity / Open Question → Stakeholder trade-off → Decision (DEC-xx) → Technical slices updated → Cockpit validation**

- Keep assumptions and open questions outside the baseline until resolved.
- Set system boundaries and source-of-truth ownership before detailing UI or API behavior.
- Update requirement, state, integration, UX and validation evidence as one change.

# 2. Architecture & Business Decision Slices

| **Decision** | **Ambiguity & trade-off** | **Decision & rationale** | **Technical trace** |
| --- | --- | --- | --- |
| **DEC-BOUNDARY-01** Payment boundary | **A:** ApproveFlow stores payment methods and executes charges — more control, materially larger security and compliance scope.**B:** Use the existing Payment Processor — external dependency, smaller sensitive-data boundary. | **Choose B.** ApproveFlow initiates payment and consumes verified outcomes; it does not store card data or execute transactions. | [Decision Log](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) · [Scope](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229417/Scope+Stakeholders+Success+Metrics) · [API-04/05 & SD-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) · [UAT-08](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98340/User+Acceptance+Testing+UAT+Specification) |
| **DEC-ARCH-01** Pricing ownership | **A:** Recalculate proration, tax and discount in ApproveFlow — faster local response, duplicated financial rules.**B:** Ask Billing System for the price — one more integration call, one financial source of truth. | **Choose B.** Billing System calculates; ApproveFlow submits inputs and displays the returned breakdown. | [Decision Log](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) · [Pricing rules](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98325/Business+Rules+Decision+Tables) · [API-02 & SQL checks](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) · [Upgrade Preview](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/66150/Wireframes+UI+States) |
| **DEC-STATE-01** Failure granularity | **A:** One generic `Failed` state — simpler model, ambiguous recovery.**B:** Separate failure by stage — more transitions, precise customer and support action. | **Choose B.** Distinguish `Payment Failed`, `Activation Failed` and `Execution Failed`; each has a different recovery rule. Downgrade execution failure remains terminal in the current baseline. | [State Model](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131234/State+Transition+Model+Specification) · [Error Mapping & Sequence](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) · [UAT-03/04/07](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98340/User+Acceptance+Testing+UAT+Specification) · [Main Cockpit](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/7110657/Main+Cockpit+Change-Ready) |
| **DEC-PLAT-01** Platform scope | **A:** Desktop, responsive web and native mobile — broader reach, larger design and validation surface.**B:** Desktop/Web only — narrower release surface, explicit mobile exclusion. | **Choose B.** ApproveFlow MVP covers Desktop/Web. Responsive web and native mobile require separate requirements and validation. | [Decision Log](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) · [Platform Scope](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229417/Scope+Stakeholders+Success+Metrics) · [Wireframes](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/66150/Wireframes+UI+States) |

# 3. Stakeholder Lenses

| **Lens** | **Question the decision must answer** | **Evidence checked** |
| --- | --- | --- |
| Product | What is in MVP, and what is deliberately excluded? | [Business Brief](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229409/Business+Brief) · [Scope & Success Metrics](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229417/Scope+Stakeholders+Success+Metrics) |
| Finance / Billing | Which system owns pricing and payment truth? | [Decision Log](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) · [Business Rules](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98325/Business+Rules+Decision+Tables) |
| Engineering | Where are boundaries, states and integration contracts explicit? | [State Model](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131234/State+Transition+Model+Specification) · [API, SQL & Sequence](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) |
| QA | Can each outcome and invariant be verified? | [Acceptance & UAT](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98340/User+Acceptance+Testing+UAT+Specification) · [SQL checks](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453/API+SQL+Sequence+Analysis) |
| Support / Operations | What happened, what is safe to retry, and what remains unchanged? | [State Model](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131234/State+Transition+Model+Specification) · [Recovery scenarios](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98340/User+Acceptance+Testing+UAT+Specification) |

# 4. Decision Governance

- **Source path:** [Assumptions](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/131269/Assumption+Register+Decision+Traceability) / [Open Questions](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/360481/Open+Questions+Clarifications+Register) → [Decision Log](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229475/Architecture+Business+Decision+Log) → affected technical artefacts → [Main Cockpit](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/7110657/Main+Cockpit+Change-Ready).
- **Change rule:** a conflicting rule reopens the affected slice for impact analysis; the baseline is not silently overwritten.
- **Evidence rule:** each retained decision must link to at least one requirement/design artefact and one validation artefact where applicable.

# 5. Limitations

- No real stakeholder interview, workshop recording, approval or production sign-off is claimed.
- The page demonstrates analysis discipline and traceability, not production delivery experience.
- In a live project, the decision record would also name participants, owner, date and approval authority.

