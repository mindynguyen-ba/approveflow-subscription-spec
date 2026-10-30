# Confluence Mirror Repository Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure `approveflow-subscription-spec` into a complete Markdown mirror of the 25 current Confluence content IDs while preserving `docs/assets/` and `poc-automation/` byte-for-byte.

**Architecture:** The repository remains a source-backed specification package. Each canonical Confluence page maps to one focused Markdown target, except page `229453`, which maps to three focused data/integration documents; the manifest is the provenance index and the validator enforces structure, counts, evidence labels, links, JSON safety and manifest coverage.

**Tech Stack:** Markdown, YAML manifest, Python standard-library validator/tests, Git, Atlassian Confluence attachments/content API.

**Spec:** `docs/superpowers/specs/2026-10-30-confluence-mirror-restructure-design.md`

## Global Constraints

- Source policy remains `confluence-only`; never use local project documents as content fallback.
- Do not create OpenAPI/Swagger/JSON Schema files, Postman environment files or copied Jira Gherkin.
- Keep `docs/assets/` and `poc-automation/` path, filenames and bytes unchanged.
- Preserve evidence labels: `BASELINED — SIMULATION`, `DESIGNED — NOT EXECUTED`, `NOT RUN` and manual-simulation wording.
- Canonical counts: Decisions 20, Assumptions 25, Clarifications 27, Stories 6, AC defined 40, SQL invariants 8, UAT scenarios 9.
- Leave annotated tag `v1.0.0` unchanged; create `v1.1.0` only after every gate passes.
- Use current Confluence page versions recorded in the approved spec; if any version changed at execution time, refetch and update both content and manifest together.

## Review Focus

- A combined export split across targets must not lose a source header, evidence label, diagram link or canonical ID.
- Markdown moves must not break relative links into `docs/assets/`.
- Manifest validation must allow content ID `229453` on three targets but reject missing/duplicate required targets.
- Existing API prose must not be presented as delivery-level OpenAPI or executed integration evidence.
- Asset/PoC inventories must match before and after migration, including both JSON checksums and all 20 PNG files.

---

### Task 1: Lock the New Repository Contract in Tests

**Files:**
- Modify: `tests/test_validate_repository.py`
- Modify: `scripts/validate_repository.py`

**Interfaces:**
- Consumes: Target structure and source mapping from the approved design.
- Produces: `validate_repository(root: Path) -> list[str]` enforcing the new paths, forbidden legacy paths, manifest target existence/uniqueness and distinct Confluence content-ID coverage.

- [ ] **Step 1: Add failing tests for the new required paths**

Add fixture paths for all approved Markdown targets and assertions that a missing target reports `missing required file: <path>`.

- [ ] **Step 2: Add failing tests for forbidden legacy paths**

Assert that files under `docs/01-scope-and-decisions/`, `docs/02-process-and-states/`, `docs/03-specifications/` and `docs/04-testing-and-uat/` report `superseded documentation path`.

- [ ] **Step 3: Add failing manifest-contract tests**

Assert:

- every required Markdown target appears exactly once;
- every manifest `target` exists;
- 25 distinct numeric content IDs are present;
- content ID `229453` may map to exactly the three approved targets.

- [ ] **Step 4: Run the targeted tests and confirm failure**

Run: `python3 -m unittest tests/test_validate_repository.py -v`

Expected: FAIL on unimplemented required-path/manifest checks.

- [ ] **Step 5: Implement the validator contract with Python standard library only**

Update required files, ID-contract paths and evidence-file paths. Add minimal manifest extraction for `target`, `content_id` and inline `content_ids` fields without adding a YAML dependency.

- [ ] **Step 6: Run unit tests**

Run: `python3 -m unittest tests/test_validate_repository.py -v`

Expected: fixture tests PASS; live repository may still fail until Tasks 2–5 complete.

- [ ] **Step 7: Commit**

```bash
git add scripts/validate_repository.py tests/test_validate_repository.py
git commit -m "test: define Confluence mirror repository contract"
```

### Task 2: Capture Preservation Inventories and Export Missing Business/Requirements Pages

**Files:**
- Create: `docs/01-business-context/business-brief.md`
- Create: `docs/01-business-context/scope-and-metrics.md`
- Create: `docs/01-business-context/plan-catalogue.md`
- Create: `docs/02-requirements-map/main-cockpit.md`
- Create: `docs/02-requirements-map/traceability-map.md`
- Create: `docs/02-requirements-map/coverage-matrix.md`

**Interfaces:**
- Consumes: Confluence current pages `229409`, `229417`, `8192008`, `7110657`, `16351237`, `5341219`; current `docs/03-specifications/user-stories-ac.md` coverage section.
- Produces: Six focused Markdown mirrors with source headers and current page metadata.

- [ ] **Step 1: Capture immutable pre-migration inventories**

Run:

```bash
find docs/assets -type f -print0 | sort -z | xargs -0 shasum -a 256
find poc-automation -type f -print0 | sort -z | xargs -0 shasum -a 256
```

Save outputs outside the repository in a task-specific temporary directory for the final comparison.

- [ ] **Step 2: Read current Confluence versions and full Markdown**

Fetch each content ID listed above. If a version differs from the design, use the fetched version and record the drift for Task 5.

- [ ] **Step 3: Create the three business-context mirrors**

Preserve source semantics and evidence status; do not convert measurement targets into observed results or approved production SLAs.

- [ ] **Step 4: Create Main Cockpit and Traceability Map mirrors**

Preserve lifecycle/revision metadata and the distinction between canonical Main Cockpit and derived Traceability Map.

- [ ] **Step 5: Extract the existing coverage section into `coverage-matrix.md`**

The target must retain `40/40 AC defined` and state that detailed Gherkin remains in Jira.

- [ ] **Step 6: Validate links and source headers for Task 2 files**

Run: `python3 scripts/validate_repository.py .`

Expected: only later-task missing files/legacy-path failures remain; no Task 2 broken link or count failure.

- [ ] **Step 7: Commit**

```bash
git add docs/01-business-context docs/02-requirements-map
git commit -m "docs: add business context and requirements mirrors"
```

### Task 3: Migrate Process, State and Specification Documents

**Files:**
- Move: `docs/02-process-and-states/bpmn-workflows.md` → `docs/03-process-and-states/bpmn-workflows.md`
- Move: `docs/02-process-and-states/state-machines.md` → `docs/03-process-and-states/state-transition-models.md`
- Create: `docs/03-process-and-states/business-rules.md`
- Create: `docs/03-process-and-states/exception-matrix.md`
- Create: `docs/03-process-and-states/end-to-end-system-behavior.md`
- Create: `docs/04-specifications/user-stories.md`
- Create: `docs/04-specifications/functional-requirements.md`
- Move/split: `docs/03-specifications/ux-specifications.md` → `docs/04-specifications/ui-state-specs.md`
- Remove after split: `docs/03-specifications/user-stories-ac.md`

**Interfaces:**
- Consumes: Existing process/state/UX exports and current Confluence pages `98325`, `5373964`, `10092622`, `229437`, `229429`.
- Produces: Eight focused documents with valid asset links and source metadata.

- [ ] **Step 1: Read missing source pages in current Markdown**

Fetch the five missing content IDs and confirm versions match the design or record drift.

- [ ] **Step 2: Move the existing BPMN and state exports**

Keep content and `docs/assets/` links semantically unchanged; update relative paths only if link validation requires it.

- [ ] **Step 3: Add rules, exception and system-behavior mirrors**

Preserve known source inconsistencies as source facts; do not silently reconcile activation-state, grace-wording or enum drift during repository restructuring.

- [ ] **Step 4: Extract Story Index into `user-stories.md`**

Retain six Story boundaries and the explicit statement that detailed Gherkin remains in Jira. Do not duplicate the coverage matrix.

- [ ] **Step 5: Add Functional Requirements mirror and move UX specification**

Retain source links, Screen ID contract and offline wireframe/UI-state previews.

- [ ] **Step 6: Run counts/link checks**

Run: `python3 scripts/validate_repository.py .`

Expected: Decisions/Assumptions/OQ/SQL/UAT targets may remain missing until Task 4; no process/spec link failures.

- [ ] **Step 7: Commit**

```bash
git add docs/03-process-and-states docs/04-specifications docs/02-process-and-states docs/03-specifications
git commit -m "docs: mirror process state and specification pages"
```

### Task 4: Migrate Data, Validation, Governance and Measurement Documents

**Files:**
- Move: `docs/03-specifications/data-dictionary.md` → `docs/05-data-and-integration/erd-and-data-dictionary.md`
- Split/move: `docs/03-specifications/api-contracts.md` → `docs/05-data-and-integration/api-contracts.md` and `docs/05-data-and-integration/sequence-diagrams.md`
- Move: `docs/03-specifications/sql-invariants.md` → `docs/05-data-and-integration/sql-invariants.md`
- Move: `docs/04-testing-and-uat/uat-specification.md` → `docs/06-validation-and-uat/uat-specification.md`
- Move: `docs/01-scope-and-decisions/decisions-log.md` → `docs/07-governance-and-decisions/architecture-decisions.md`
- Move: `docs/01-scope-and-decisions/assumptions-log.md` → `docs/07-governance-and-decisions/assumption-register.md`
- Move: `docs/01-scope-and-decisions/open-questions.md` → `docs/07-governance-and-decisions/open-questions.md`
- Create: `docs/07-governance-and-decisions/change-requests.md`
- Create: `docs/08-measurement-and-evidence/roi-and-metrics-plan.md`
- Create: `docs/08-measurement-and-evidence/communication-and-decision-evidence.md`

**Interfaces:**
- Consumes: Existing data/API/SQL/UAT/governance exports and current Confluence pages `360497`, `66158`, `2981890`.
- Produces: Complete data, validation, governance and evidence mirror; old numbered doc paths removed.

- [ ] **Step 1: Read the three missing source pages in current Markdown**

Confirm versions or record drift for Task 5.

- [ ] **Step 2: Move data dictionary and SQL invariants**

Preserve ERD/DFD image links and exactly eight SQL invariant IDs.

- [ ] **Step 3: Split API versus sequence content**

Keep API inventory/error mapping and `DESIGNED — NOT EXECUTED` disclaimer in `api-contracts.md`. Put SD-01–03 narratives and image links in `sequence-diagrams.md`. Do not create JSON schemas.

- [ ] **Step 4: Move UAT and governance files**

Preserve 9 UAT scenarios, 20 Decisions, 25 Assumptions and 27 Clarifications.

- [ ] **Step 5: Add Change Requests, ROI and Communication Evidence mirrors**

Preserve simulation/not-measured language and source inconsistencies; do not claim production outcomes.

- [ ] **Step 6: Confirm legacy documentation directories are empty and remove them**

Remove only superseded Markdown directories. Never delete `docs/assets/`, `docs/superpowers/` or `poc-automation/`.

- [ ] **Step 7: Run validator and link checks**

Run: `python3 scripts/validate_repository.py .`

Expected: failures may remain only for stale README/manifest until Task 5.

- [ ] **Step 8: Commit**

```bash
git add docs
git commit -m "docs: complete Confluence information architecture mirror"
```

### Task 5: Rebuild Navigation, Provenance and Release Notes

**Files:**
- Modify: `README.md`
- Modify: `docs/source-manifest.yaml`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: Final target paths, fetched page versions, attachment metadata and unchanged PoC/asset inventories.
- Produces: Repository navigation, one-to-one provenance records and `1.1.0` release notes.

- [ ] **Step 1: Update README navigation**

Add all eight document groups, preserve executive summary/evidence status and state that implementation-level OpenAPI and detailed Jira Gherkin are outside this mirror.

- [ ] **Step 2: Rebuild manifest target mapping**

Record all 25 distinct content IDs, exact current versions and every target path. Keep attachment IDs, Figma node IDs and PoC checksums unchanged.

- [ ] **Step 3: Update canonical counts and limitations**

Use 20 Decisions and retain 40/40 AC-defined wording without claiming Gherkin text is packaged.

- [ ] **Step 4: Add `1.1.0` changelog entry**

Describe the information-architecture migration and missing-page exports; do not rewrite the `1.0.0` history.

- [ ] **Step 5: Run unit and full validators**

Run:

```bash
python3 -m unittest tests/test_validate_repository.py -v
python3 scripts/validate_repository.py .
git diff --check
```

Expected: all PASS.

- [ ] **Step 6: Commit**

```bash
git add README.md docs/source-manifest.yaml CHANGELOG.md
git commit -m "docs: finalize Confluence mirror navigation and provenance"
```

### Task 6: Final Integrity Gate and Baseline Tag

**Files:**
- Modify: `MEMORY.md` in the parent BA-kit workspace after repository verification.

**Interfaces:**
- Consumes: Completed repository and pre-migration checksum inventories.
- Produces: Verified clean repository, immutable `v1.1.0` tag and updated session handoff.

- [ ] **Step 1: Compare complete asset and PoC inventories**

Regenerate SHA-256 inventories and compare with Task 2 outputs.

Expected: exact match, no added/removed/changed file under `docs/assets/` or `poc-automation/`.

- [ ] **Step 2: Run final repository verification**

```bash
python3 -m unittest tests/test_validate_repository.py -v
python3 scripts/validate_repository.py .
git diff --check
git status --short --branch
```

Expected: tests PASS, validator PASS, diff check clean; only intended design/plan changes remain if not already committed.

- [ ] **Step 3: Commit design and plan if still uncommitted**

```bash
git add docs/superpowers/specs/2026-10-30-confluence-mirror-restructure-design.md docs/superpowers/plans/2026-10-30-confluence-mirror-restructure.md
git commit -m "docs: record Confluence mirror restructure design"
```

- [ ] **Step 4: Create annotated tag**

```bash
git tag -a v1.1.0 -m "ApproveFlow complete Confluence mirror v1.1.0"
```

Verify `v1.0.0` still resolves to its original tagged commit and `v1.1.0` resolves to the new baseline.

- [ ] **Step 5: Update and validate shared memory**

Update current state, decisions, files, blockers, verification, next actions and handoff in parent `MEMORY.md`.

Run: `python3 scripts/validate_memory.py .` from `/Users/ai_assistant/Documents/BA-kit`.

Expected: `PASS: shared memory contract valid`.

- [ ] **Step 6: Report remote blocker**

Do not push until the user supplies the intended Git remote URL and the target repository is verified.
