# Confluence Mirror Repository Restructure — Design

## Intent

Restructure `approveflow-subscription-spec` so repository navigation mirrors the numbered Confluence information architecture, while preserving source provenance and exposing the pages currently missing from Git.

The repository is an analysis/specification package, not an implementation contract. Content must remain traceable to current Confluence pages and must not invent OpenAPI schemas, Postman environments, acceptance criteria, execution evidence or production SLAs that the source does not contain.

## Goals

- Mirror each relevant Confluence page into one focused Markdown file.
- Add the missing business, traceability, rule, exception, functional-requirement and measurement documents.
- Split combined exports where two different Confluence pages currently share one repository file.
- Preserve page ID, page version, evidence status and attachment provenance in `docs/source-manifest.yaml`.
- Keep repository-relative links valid after file moves.
- Keep the repository validator aligned with the new contract.

## Non-goals

- Do not change Confluence, Jira, Figma, Postman or n8n content.
- Do not create implementation-level OpenAPI/Swagger/JSON Schema files. Confluence page `229453` explicitly defers them.
- Do not copy detailed Gherkin AC from Jira into the Confluence mirror. The source pages state that Jira remains authoritative for detailed AC wording.
- Do not create `approveflow_environment.json`; no Confluence attachment currently supplies it.
- Do not move, rename or modify files inside `docs/assets/` or `poc-automation/`.
- Do not rewrite or move tag `v1.0.0`; the restructured baseline will use a later tag after verification.

## Chosen Approach

### Approach 1 — Fidelity-first (chosen)

Mirror current Confluence pages as Markdown, preserve assets/PoC byte-for-byte and record any source limitations explicitly. This maximizes traceability and prevents derived artifacts from being mistaken for approved contracts.

### Approach 2 — Structure-first (rejected)

Create every path in the proposed tree, including three API JSON files and a Postman environment. Rejected because those source artifacts do not exist in Confluence and would violate the repository's `confluence-only` policy.

### Approach 3 — Hybrid derived contracts (rejected)

Mirror Markdown and derive provisional machine-readable API files. Rejected for this revision because the derived files would require a separate approval lifecycle, schema validation and ownership model.

## Target Structure

```text
approveflow-subscription-spec/
├── README.md
├── docs/
│   ├── 01-business-context/
│   │   ├── business-brief.md
│   │   ├── scope-and-metrics.md
│   │   └── plan-catalogue.md
│   ├── 02-requirements-map/
│   │   ├── main-cockpit.md
│   │   ├── traceability-map.md
│   │   └── coverage-matrix.md
│   ├── 03-process-and-states/
│   │   ├── bpmn-workflows.md
│   │   ├── state-transition-models.md
│   │   ├── business-rules.md
│   │   ├── exception-matrix.md
│   │   └── end-to-end-system-behavior.md
│   ├── 04-specifications/
│   │   ├── user-stories.md
│   │   ├── functional-requirements.md
│   │   └── ui-state-specs.md
│   ├── 05-data-and-integration/
│   │   ├── erd-and-data-dictionary.md
│   │   ├── api-contracts.md
│   │   ├── sequence-diagrams.md
│   │   └── sql-invariants.md
│   ├── 06-validation-and-uat/
│   │   └── uat-specification.md
│   ├── 07-governance-and-decisions/
│   │   ├── architecture-decisions.md
│   │   ├── assumption-register.md
│   │   ├── open-questions.md
│   │   └── change-requests.md
│   ├── 08-measurement-and-evidence/
│   │   ├── roi-and-metrics-plan.md
│   │   └── communication-and-decision-evidence.md
│   ├── assets/                         # unchanged path and bytes
│   ├── source-manifest.yaml
│   └── superpowers/                    # design and implementation records
└── poc-automation/                     # unchanged path, names and bytes
```

The four extra mirror files—`traceability-map.md`, `end-to-end-system-behavior.md`, `change-requests.md`, and `communication-and-decision-evidence.md`—represent current Confluence pages omitted from the proposed sketch. They are included because fidelity-first means page coverage must not depend on hidden links.

## Source Mapping

| Repository target | Confluence source | Content ID | Current version |
|---|---|---:|---:|
| `README.md` | 01. Project Home & Portfolio Summary | `98315` | 20 |
| `01-business-context/business-brief.md` | Business Brief | `229409` | 14 |
| `01-business-context/scope-and-metrics.md` | Scope, Stakeholders & Success Metrics | `229417` | 14 |
| `01-business-context/plan-catalogue.md` | Plan Catalogue & Entitlement Matrix | `8192008` | 5 |
| `02-requirements-map/main-cockpit.md` | Main Cockpit Change-Ready | `7110657` | 22 |
| `02-requirements-map/traceability-map.md` | Traceability Map | `16351237` | 4 |
| `02-requirements-map/coverage-matrix.md` | Acceptance Criteria Coverage Matrix | `5341219` | 6 |
| `03-process-and-states/bpmn-workflows.md` | Process Models | `131226` | 13 |
| `03-process-and-states/state-transition-models.md` | State Transition Model Specification | `131234` | 18 |
| `03-process-and-states/business-rules.md` | Business Rules & Decision Tables | `98325` | 18 |
| `03-process-and-states/exception-matrix.md` | Exception Matrix & Failure Recovery | `5373964` | 10 |
| `03-process-and-states/end-to-end-system-behavior.md` | End-to-End System Behavior | `10092622` | 11 |
| `04-specifications/user-stories.md` | Jira Story Index | `229437` | 17 |
| `04-specifications/functional-requirements.md` | Functional Requirements | `229429` | 9 |
| `04-specifications/ui-state-specs.md` | Wireframes & UI States | `66150` | 10 |
| `05-data-and-integration/erd-and-data-dictionary.md` | ERD & Data Dictionary | `229445` | 8 |
| `05-data-and-integration/api-contracts.md` | API, SQL & Sequence Analysis | `229453` | 16 |
| `05-data-and-integration/sequence-diagrams.md` | API, SQL & Sequence Analysis | `229453` | 16 |
| `05-data-and-integration/sql-invariants.md` | API, SQL & Sequence Analysis | `229453` | 16 |
| `06-validation-and-uat/uat-specification.md` | User Acceptance Testing Specification | `98340` | 7 |
| `07-governance-and-decisions/architecture-decisions.md` | Architecture & Business Decision Log | `229475` | 16 |
| `07-governance-and-decisions/assumption-register.md` | Assumption Register & Decision Traceability | `131269` | 15 |
| `07-governance-and-decisions/open-questions.md` | Open Questions & Clarifications Register | `360481` | 18 |
| `07-governance-and-decisions/change-requests.md` | Change Requests | `360497` | 5 |
| `08-measurement-and-evidence/roi-and-metrics-plan.md` | ROI & Measurement Plan | `66158` | 7 |
| `08-measurement-and-evidence/communication-and-decision-evidence.md` | Communication & Decision Evidence | `2981890` | 6 |
| `poc-automation/README.md` | 10. Technical PoC — Paid Upgrade Activation Monitoring | `14909445` | 9 |

## Migration Rules

1. Use `git mv` semantics for existing Markdown so history remains readable.
2. Split `user-stories-ac.md` into `user-stories.md` and `coverage-matrix.md` at the existing source boundary.
3. Split the sequence narrative/images out of the existing `api-contracts.md`; retain its API inventory/error mapping in the renamed API target. Move the already separate `sql-invariants.md` without re-extracting or duplicating it. No machine-readable API JSON is created.
4. Fetch missing Markdown from the current Confluence version; do not use local project files as content fallback.
5. Preserve all evidence labels, especially `BASELINED — SIMULATION`, `DESIGNED — NOT EXECUTED`, and `NOT RUN`.
6. Preserve `docs/assets/` and `poc-automation/` path, filenames and bytes. Checksum them before and after migration.
7. Update all repository-relative links, README navigation and manifest targets.
8. Update validator/tests before considering the migration complete.

## Counts and Naming Decisions

- The repository records **20 Decisions**, matching Confluence current version 16; the proposed comment saying 19 is stale.
- The repository records 6 Stories and **40/40 AC defined**, but does not claim the Git mirror contains all Gherkin text because Jira owns detailed AC wording.
- `state-transition-models.md` replaces `state-machines.md` to match the Confluence page semantics.
- `api-contracts.md` remains Markdown and explicitly states that delivery-level OpenAPI is deferred.

## Validation and Completion Gate

The restructure is done only when:

- every target file exists and every old superseded documentation path is absent;
- every required Markdown target appears exactly once in `docs/source-manifest.yaml`, and every manifest target exists;
- the manifest covers all 25 distinct Confluence content IDs; content ID `229453` may map to three focused targets;
- all local Markdown links resolve;
- canonical counts remain Decisions 20, Assumptions 25, Clarifications 27, Stories 6, AC 40, SQL 8 and UAT 9;
- complete SHA-256 inventories for `docs/assets/` and `poc-automation/` match before and after migration byte-for-byte;
- JSON files parse and secret scan remains clean;
- validator unit tests and full repository validator pass;
- `git diff --check` passes and the worktree is clean after commit.

## Risks and Controls

- **Source drift:** refetch page metadata/content immediately before export and record exact versions.
- **Traceability loss during split:** keep source headers in every resulting file and test manifest targets.
- **Broken asset links:** validate all relative Markdown links after moves.
- **False implementation readiness:** preserve evidence disclaimers and do not generate API schemas.
- **Historical tag mutation:** leave `v1.0.0` unchanged; create `v1.1.0` only after the new baseline passes.
