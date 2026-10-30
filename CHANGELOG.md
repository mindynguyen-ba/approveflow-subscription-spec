# Changelog

## Unreleased — Confluence baseline export

### Added

- Governance baseline: 20 Decisions, 25 Assumptions and 27 closed Clarifications.
- Process/state baseline with four Confluence-hosted diagram attachments.
- Complete seven-type diagram registry: BPMN, State Machine, Wireframe, UI States, DFD, ERD and Sequence Diagram.
- Six User Stories, 40 defined Acceptance Criteria, data dictionary and API contracts.
- Eight SQL invariants and nine UAT scenarios, explicitly marked `DESIGNED — NOT EXECUTED`.
- Technical PoC documentation from Confluence page `14909445` version 9.
- Postman Collection v2.1 from Confluence attachment `att18481153`, with checksum recorded in the source manifest.
- Dependency-free repository validator and unit-test suite.

### Blocked

- `poc-automation/n8n/workflow_export.json`: no JSON attachment exists in Confluence folder `98311`.
- Release tag and remote push remain blocked until the n8n source artifact is added to Confluence and exported.

