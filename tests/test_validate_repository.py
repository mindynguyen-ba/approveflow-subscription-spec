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
    REQUIRED_TEXT = {
        "README.md": "# ApproveFlow\n\nDESIGNED — NOT EXECUTED\n",
        "docs/source-manifest.yaml": "source_folder_id: '98311'\n",
        "docs/01-scope-and-decisions/decisions-log.md": "",
        "docs/01-scope-and-decisions/assumptions-log.md": "",
        "docs/01-scope-and-decisions/open-questions.md": "",
        "docs/02-process-and-states/state-machines.md": "",
        "docs/02-process-and-states/bpmn-workflows.md": "",
        "docs/03-specifications/user-stories-ac.md": "40/40 AC defined\n",
        "docs/03-specifications/data-dictionary.md": "",
        "docs/03-specifications/api-contracts.md": "DESIGNED — NOT EXECUTED\n",
        "docs/03-specifications/sql-invariants.md": "",
        "docs/04-testing-and-uat/uat-specification.md": "DESIGNED — NOT EXECUTED\n",
        "poc-automation/README.md": "Mock-only prototype.\n",
        "CHANGELOG.md": "# Changelog\n",
    }

    def __init__(self, root: Path):
        self.root = root

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def build_valid(self) -> None:
        for relative, content in self.REQUIRED_TEXT.items():
            self.write(relative, content)
        self.write(
            "docs/01-scope-and-decisions/decisions-log.md",
            "\n".join(f"DEC-TEST-{index:02d}" for index in range(1, 21)),
        )
        self.write(
            "docs/01-scope-and-decisions/assumptions-log.md",
            "\n".join(f"ASM-TEST-{index:02d}" for index in range(1, 26)),
        )
        self.write(
            "docs/01-scope-and-decisions/open-questions.md",
            "\n".join(f"OQ-TEST-{index:02d}" for index in range(1, 28)),
        )
        self.write(
            "docs/03-specifications/user-stories-ac.md",
            "\n".join(f"US-{index:02d}" for index in range(1, 7))
            + "\n40/40 AC defined\n",
        )
        self.write(
            "docs/03-specifications/sql-invariants.md",
            "\n".join(f"SQL-{index:02d}" for index in range(1, 9)),
        )
        self.write(
            "docs/04-testing-and-uat/uat-specification.md",
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

    def test_reports_duplicate_stable_id_even_when_total_occurrences_match(self):
        path = self.root / "docs/01-scope-and-decisions/decisions-log.md"
        ids = [f"DEC-TEST-{index:02d}" for index in range(1, 20)] + ["DEC-TEST-19"]
        path.write_text("\n".join(ids), encoding="utf-8")
        errors = validator.validate_repository(self.root)
        self.assertIn("duplicate DEC id: DEC-TEST-19", errors)

    def test_accepts_confluence_table_ids_wrapped_in_backticks(self):
        path = self.root / "docs/01-scope-and-decisions/decisions-log.md"
        rows = [f"| `DEC-TEST-{index:02d}` | Decision {index} |" for index in range(1, 21)]
        path.write_text("\n".join(rows), encoding="utf-8")
        errors = validator.validate_repository(self.root)
        self.assertNotIn("DEC count: expected 20, found 0", errors)

    def test_accepts_sql_ids_in_exported_sql_comments(self):
        path = self.root / "docs/03-specifications/sql-invariants.md"
        rows = [f"-- SQL-{index:02d} · invariant {index}" for index in range(1, 9)]
        path.write_text("\n".join(rows), encoding="utf-8")
        errors = validator.validate_repository(self.root)
        self.assertNotIn("SQL count: expected 8, found 0", errors)

    def test_reports_canonical_count_mismatch(self):
        path = self.root / "docs/01-scope-and-decisions/assumptions-log.md"
        path.write_text("\n".join(f"ASM-TEST-{i:02d}" for i in range(1, 25)), encoding="utf-8")
        self.assertIn("ASM count: expected 25, found 24", validator.validate_repository(self.root))

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
        self.fixture.write("docs/04-testing-and-uat/uat-specification.md", "UAT-01 PASS\n")
        errors = validator.validate_repository(self.root)
        self.assertIn("missing evidence label: docs/04-testing-and-uat/uat-specification.md", errors)

    def test_valid_repository_has_no_errors(self):
        self.assertEqual([], validator.validate_repository(self.root))


if __name__ == "__main__":
    unittest.main()
