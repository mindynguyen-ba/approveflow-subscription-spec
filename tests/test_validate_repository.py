import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "validate_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class RepositoryFixture:
    SOURCE_MAPPING = (
        ("README.md", "98315"),
        ("docs/01-business-context/business-brief.md", "229409"),
        ("docs/01-business-context/scope-and-metrics.md", "229417"),
        ("docs/01-business-context/plan-catalogue.md", "8192008"),
        ("docs/02-requirements-map/main-cockpit.md", "7110657"),
        ("docs/02-requirements-map/traceability-map.md", "16351237"),
        ("docs/02-requirements-map/coverage-matrix.md", "5341219"),
        ("docs/03-process-and-states/bpmn-workflows.md", "131226"),
        ("docs/03-process-and-states/state-transition-models.md", "131234"),
        ("docs/03-process-and-states/business-rules.md", "98325"),
        ("docs/03-process-and-states/exception-matrix.md", "5373964"),
        ("docs/03-process-and-states/end-to-end-system-behavior.md", "10092622"),
        ("docs/04-specifications/user-stories.md", "229437"),
        ("docs/04-specifications/functional-requirements.md", "229429"),
        ("docs/04-specifications/ui-state-specs.md", "66150"),
        ("docs/05-data-and-integration/erd-and-data-dictionary.md", "229445"),
        ("docs/05-data-and-integration/api-contracts.md", "229453"),
        ("docs/05-data-and-integration/sequence-diagrams.md", "229453"),
        ("docs/05-data-and-integration/sql-invariants.md", "229453"),
        ("docs/06-validation-and-uat/uat-specification.md", "98340"),
        ("docs/07-governance-and-decisions/architecture-decisions.md", "229475"),
        ("docs/07-governance-and-decisions/assumption-register.md", "131269"),
        ("docs/07-governance-and-decisions/open-questions.md", "360481"),
        ("docs/07-governance-and-decisions/change-requests.md", "360497"),
        ("docs/08-measurement-and-evidence/roi-and-metrics-plan.md", "66158"),
        ("docs/08-measurement-and-evidence/communication-and-decision-evidence.md", "2981890"),
        ("poc-automation/README.md", "14909445"),
    )

    REQUIRED_ASSETS = (
        "docs/assets/bpmn/bpmn-as-is-subscription-management.png",
        "docs/assets/bpmn/bpmn-self-service-upgrade.png",
        "docs/assets/state-machines/state-subscription-lifecycle.png",
        "docs/assets/state-machines/state-change-request-lifecycle.png",
        "docs/assets/bpmn/bpmn-scheduled-downgrade.png",
        "docs/assets/bpmn/bpmn-payment-failure-recovery.png",
        "docs/assets/wireframes/journey-01-user-flow.png",
        "docs/assets/wireframes/journey-01-wireframes.png",
        "docs/assets/wireframes/journey-02-user-flow.png",
        "docs/assets/wireframes/journey-02-wireframes.png",
        "docs/assets/wireframes/journey-03-user-flow.png",
        "docs/assets/wireframes/journey-03-wireframes.png",
        "docs/assets/ui-states/journey-01-ui-states.png",
        "docs/assets/ui-states/journey-02-ui-states.png",
        "docs/assets/ui-states/journey-03-ui-states.png",
        "docs/assets/dfd/logical-dfd-subscription-management.png",
        "docs/assets/erd/core-logical-erd.png",
        "docs/assets/sequence-diagrams/sd-01-upgrade-payment-activation.png",
        "docs/assets/sequence-diagrams/sd-02-payment-recovery-access-restoration.png",
        "docs/assets/sequence-diagrams/sd-03-scheduled-downgrade-execution.png",
    )

    def __init__(self, root: Path):
        self.root = root

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_manifest(self, mapping=None) -> None:
        records = mapping if mapping is not None else self.SOURCE_MAPPING
        lines = ["schema_version: 1", "sources:"]
        for target, content_id in records:
            lines.extend((f'  - target: "{target}"', f'    content_id: "{content_id}"'))
        self.write("docs/source-manifest.yaml", "\n".join(lines) + "\n")

    def build_valid(self) -> None:
        for target, _ in self.SOURCE_MAPPING:
            self.write(target, f"# {Path(target).stem}\n")
        self.write("CHANGELOG.md", "# Changelog\n")
        self.write_manifest()
        for relative in self.REQUIRED_ASSETS:
            self.write(relative, "test image placeholder")
        self.write(
            "docs/07-governance-and-decisions/architecture-decisions.md",
            "\n".join(f"DEC-TEST-{index:02d}" for index in range(1, 21)),
        )
        self.write(
            "docs/07-governance-and-decisions/assumption-register.md",
            "\n".join(f"ASM-TEST-{index:02d}" for index in range(1, 26)),
        )
        self.write(
            "docs/07-governance-and-decisions/open-questions.md",
            "\n".join(f"OQ-TEST-{index:02d}" for index in range(1, 28)),
        )
        self.write(
            "docs/04-specifications/user-stories.md",
            "\n".join(f"US-{index:02d}" for index in range(1, 7)),
        )
        self.write("docs/02-requirements-map/coverage-matrix.md", "40/40 AC defined\n")
        self.write(
            "docs/05-data-and-integration/sql-invariants.md",
            "\n".join(f"SQL-{index:02d}" for index in range(1, 9)),
        )
        self.write("docs/05-data-and-integration/api-contracts.md", "DESIGNED — NOT EXECUTED\n")
        self.write(
            "docs/06-validation-and-uat/uat-specification.md",
            "DESIGNED — NOT EXECUTED\n"
            + "\n".join(f"UAT-{index:02d}" for index in range(1, 10)),
        )
        self.write(
            "poc-automation/postman/approveflow_mocks.json",
            json.dumps({"name": "ApproveFlow mocks", "token": "${POSTMAN_TOKEN}"}),
        )
        self.write(
            "poc-automation/n8n/workflow_export.json",
            json.dumps({"name": "ApproveFlow workflow", "active": False}),
        )


class ValidateRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.fixture = RepositoryFixture(self.root)
        self.fixture.build_valid()

    def tearDown(self):
        self.temp.cleanup()

    def test_reports_missing_required_file(self):
        (self.root / "README.md").unlink()
        self.assertIn("missing required file: README.md", validator.validate_repository(self.root))

    def test_requires_new_mirror_path(self):
        missing = "docs/01-business-context/business-brief.md"
        (self.root / missing).unlink()
        self.assertIn(f"missing required file: {missing}", validator.validate_repository(self.root))

    def test_rejects_superseded_documentation_path(self):
        legacy = "docs/01-scope-and-decisions/decisions-log.md"
        self.fixture.write(legacy, "legacy")
        self.assertIn(f"superseded documentation path: {legacy}", validator.validate_repository(self.root))

    def test_requires_canonical_docs_asset_layout(self):
        missing = "docs/assets/state-machines/state-subscription-lifecycle.png"
        (self.root / missing).unlink()
        self.assertIn(f"missing required file: {missing}", validator.validate_repository(self.root))

    def test_requires_all_seven_diagram_groups_and_ux_specification(self):
        dfd = "docs/assets/dfd/logical-dfd-subscription-management.png"
        ux_spec = "docs/04-specifications/ui-state-specs.md"
        (self.root / dfd).unlink()
        (self.root / ux_spec).unlink()
        errors = validator.validate_repository(self.root)
        self.assertIn(f"missing required file: {dfd}", errors)
        self.assertIn(f"missing required file: {ux_spec}", errors)

    def test_reports_duplicate_stable_id_even_when_total_occurrences_match(self):
        path = self.root / "docs/07-governance-and-decisions/architecture-decisions.md"
        ids = [f"DEC-TEST-{index:02d}" for index in range(1, 20)] + ["DEC-TEST-19"]
        path.write_text("\n".join(ids), encoding="utf-8")
        self.assertIn("duplicate DEC id: DEC-TEST-19", validator.validate_repository(self.root))

    def test_accepts_confluence_table_ids_wrapped_in_backticks(self):
        path = self.root / "docs/07-governance-and-decisions/architecture-decisions.md"
        rows = [f"| `DEC-TEST-{index:02d}` | Decision {index} |" for index in range(1, 21)]
        path.write_text("\n".join(rows), encoding="utf-8")
        self.assertNotIn("DEC count: expected 20, found 0", validator.validate_repository(self.root))

    def test_accepts_sql_ids_in_exported_sql_comments(self):
        path = self.root / "docs/05-data-and-integration/sql-invariants.md"
        rows = [f"-- SQL-{index:02d} · invariant {index}" for index in range(1, 9)]
        path.write_text("\n".join(rows), encoding="utf-8")
        self.assertNotIn("SQL count: expected 8, found 0", validator.validate_repository(self.root))

    def test_reports_canonical_count_mismatch(self):
        path = self.root / "docs/07-governance-and-decisions/assumption-register.md"
        path.write_text("\n".join(f"ASM-TEST-{i:02d}" for i in range(1, 25)), encoding="utf-8")
        self.assertIn("ASM count: expected 25, found 24", validator.validate_repository(self.root))

    def test_manifest_requires_each_source_target_once(self):
        missing = "docs/01-business-context/business-brief.md"
        mapping = tuple(record for record in self.fixture.SOURCE_MAPPING if record[0] != missing)
        self.fixture.write_manifest(mapping)
        self.assertIn(
            f"manifest target count: {missing}: expected 1, found 0",
            validator.validate_repository(self.root),
        )

    def test_manifest_target_must_exist(self):
        manifest = self.root / "docs/source-manifest.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8")
            + '  - target: "docs/missing.md"\n    content_id: "98315"\n',
            encoding="utf-8",
        )
        self.assertIn("manifest target missing file: docs/missing.md", validator.validate_repository(self.root))

    def test_manifest_attachment_target_must_exist(self):
        manifest = self.root / "docs/source-manifest.yaml"
        manifest.write_text(
            manifest.read_text(encoding="utf-8")
            + '    attachments:\n      - id: "att-test"\n'
            + '        target: "docs/assets/missing.png"\n',
            encoding="utf-8",
        )
        self.assertIn(
            "manifest target missing file: docs/assets/missing.png",
            validator.validate_repository(self.root),
        )

    def test_manifest_requires_25_distinct_content_ids(self):
        mapping = tuple(
            (target, "98315" if content_id == "2981890" else content_id)
            for target, content_id in self.fixture.SOURCE_MAPPING
        )
        self.fixture.write_manifest(mapping)
        self.assertIn(
            "manifest content IDs: expected 25 distinct, found 24",
            validator.validate_repository(self.root),
        )

    def test_api_page_must_map_to_three_approved_targets(self):
        mapping = tuple(
            (target, "999999" if target.endswith("sequence-diagrams.md") else content_id)
            for target, content_id in self.fixture.SOURCE_MAPPING
        )
        self.fixture.write_manifest(mapping)
        self.assertIn("manifest content 229453 targets mismatch", validator.validate_repository(self.root))

    def test_manifest_rejects_swapped_source_ids(self):
        swapped = {
            "docs/01-business-context/business-brief.md": "229417",
            "docs/01-business-context/scope-and-metrics.md": "229409",
        }
        mapping = tuple(
            (target, swapped.get(target, content_id))
            for target, content_id in self.fixture.SOURCE_MAPPING
        )
        self.fixture.write_manifest(mapping)
        self.assertIn(
            "manifest source mapping mismatch: docs/01-business-context/business-brief.md: "
            "expected 229409, found 229417",
            validator.validate_repository(self.root),
        )

    def test_reports_broken_relative_markdown_link(self):
        self.fixture.write("README.md", "[Missing](docs/missing.md)\nDESIGNED — NOT EXECUTED\n")
        self.assertIn("broken relative link: README.md -> docs/missing.md", validator.validate_repository(self.root))

    def test_reports_invalid_json(self):
        self.fixture.write("poc-automation/n8n/workflow_export.json", "{invalid")
        errors = validator.validate_repository(self.root)
        self.assertTrue(any(error.startswith("invalid JSON: poc-automation/n8n/workflow_export.json") for error in errors))

    def test_reports_non_placeholder_secret_value(self):
        self.fixture.write(
            "poc-automation/postman/approveflow_mocks.json",
            json.dumps({"api_key": "live-secret-value"}),
        )
        self.assertIn(
            "possible secret: poc-automation/postman/approveflow_mocks.json:api_key",
            validator.validate_repository(self.root),
        )

    def test_requires_not_executed_evidence_label(self):
        target = "docs/06-validation-and-uat/uat-specification.md"
        self.fixture.write(target, "UAT-01 PASS\n")
        self.assertIn(f"missing evidence label: {target}", validator.validate_repository(self.root))

    def test_rejects_source_version_and_status_in_markdown(self):
        self.fixture.write(
            "README.md",
            "> Source: Project Home · Content ID `98315` · Version `20` · Status `current`\n",
        )
        self.assertIn(
            "source metadata includes version/status: README.md",
            validator.validate_repository(self.root),
        )

    def test_valid_repository_has_no_errors(self):
        self.assertEqual([], validator.validate_repository(self.root))


if __name__ == "__main__":
    unittest.main()
