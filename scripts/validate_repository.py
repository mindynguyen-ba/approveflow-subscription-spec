#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = (
    "README.md",
    "CHANGELOG.md",
    "docs/source-manifest.yaml",
    "docs/01-business-context/business-brief.md",
    "docs/01-business-context/scope-and-metrics.md",
    "docs/01-business-context/plan-catalogue.md",
    "docs/02-requirements-map/main-cockpit.md",
    "docs/02-requirements-map/traceability-map.md",
    "docs/02-requirements-map/coverage-matrix.md",
    "docs/03-process-and-states/bpmn-workflows.md",
    "docs/03-process-and-states/state-transition-models.md",
    "docs/03-process-and-states/business-rules.md",
    "docs/03-process-and-states/exception-matrix.md",
    "docs/03-process-and-states/end-to-end-system-behavior.md",
    "docs/04-specifications/user-stories.md",
    "docs/04-specifications/functional-requirements.md",
    "docs/04-specifications/ui-state-specs.md",
    "docs/05-data-and-integration/erd-and-data-dictionary.md",
    "docs/05-data-and-integration/api-contracts.md",
    "docs/05-data-and-integration/sequence-diagrams.md",
    "docs/05-data-and-integration/sql-invariants.md",
    "docs/06-validation-and-uat/uat-specification.md",
    "docs/07-governance-and-decisions/architecture-decisions.md",
    "docs/07-governance-and-decisions/assumption-register.md",
    "docs/07-governance-and-decisions/open-questions.md",
    "docs/07-governance-and-decisions/change-requests.md",
    "docs/08-measurement-and-evidence/roi-and-metrics-plan.md",
    "docs/08-measurement-and-evidence/communication-and-decision-evidence.md",
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
    "poc-automation/README.md",
    "poc-automation/postman/approveflow_mocks.json",
    "poc-automation/n8n/workflow_export.json",
)

ID_CONTRACTS = (
    ("DEC", 20, "docs/07-governance-and-decisions/architecture-decisions.md"),
    ("ASM", 25, "docs/07-governance-and-decisions/assumption-register.md"),
    ("OQ", 27, "docs/07-governance-and-decisions/open-questions.md"),
    ("US", 6, "docs/04-specifications/user-stories.md"),
    ("SQL", 8, "docs/05-data-and-integration/sql-invariants.md"),
    ("UAT", 9, "docs/06-validation-and-uat/uat-specification.md"),
)

EVIDENCE_FILES = (
    "docs/05-data-and-integration/api-contracts.md",
    "docs/06-validation-and-uat/uat-specification.md",
)

SOURCE_TARGETS = tuple(
    relative for relative in REQUIRED_FILES
    if relative == "README.md" or relative.endswith(".md") and relative != "CHANGELOG.md"
)
SUPERSEDED_DOC_DIRS = (
    "docs/01-scope-and-decisions",
    "docs/02-process-and-states",
    "docs/03-specifications",
    "docs/04-testing-and-uat",
)
API_SOURCE_TARGETS = {
    "docs/05-data-and-integration/api-contracts.md",
    "docs/05-data-and-integration/sequence-diagrams.md",
    "docs/05-data-and-integration/sql-invariants.md",
}

SECRET_KEYS = re.compile(r"(?:api[_-]?key|authorization|password|secret|token)", re.IGNORECASE)
PLACEHOLDERS = ("", "redacted", "changeme", "placeholder")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MANIFEST_SOURCE_TARGET = re.compile(r'^  -\s+target:\s+["\']?([^"\']+?)["\']?\s*$')
MANIFEST_ANY_TARGET = re.compile(r'^\s*-?\s*target:\s+["\']?([^"\']+?)["\']?\s*$')
MANIFEST_CONTENT_ID = re.compile(r'^\s+content_id:\s+["\']?(\d+)["\']?\s*$')


def _record_ids(text: str, prefix: str) -> list[str]:
    if prefix == "US":
        table_ids = re.findall(r"^\s*\|.*?\b(US-[0-9]+)\b", text, re.MULTILINE)
        if table_ids:
            return table_ids
    pattern = re.compile(
        rf"^\s*(?:(?:\|\s*)|(?:--\s+))?(?:`|\*\*)?({prefix}-[A-Z0-9]+(?:[.-][A-Z0-9]+)*)\b",
        re.MULTILINE,
    )
    return pattern.findall(text)


def _is_placeholder(value: object) -> bool:
    if not isinstance(value, str):
        return value is None
    normalized = value.strip().lower()
    return (
        normalized in PLACEHOLDERS
        or normalized.startswith("${")
        or normalized.startswith("{{")
        or normalized.startswith("<") and normalized.endswith(">")
    )


def _secret_paths(value: object, path: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if SECRET_KEYS.search(str(key)) and not _is_placeholder(child):
                findings.append(child_path)
            findings.extend(_secret_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_secret_paths(child, f"{path}[{index}]"))
    return findings


def _validate_json(path: Path, relative: str) -> list[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"invalid JSON: {relative}: {exc}"]
    return [f"possible secret: {relative}:{item}" for item in _secret_paths(payload)]


def _validate_links(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    relative_source = path.relative_to(root).as_posix()
    for raw_target in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
        target = raw_target.strip().split()[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        clean_target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        resolved = (path.parent / clean_target).resolve()
        if not resolved.exists():
            errors.append(f"broken relative link: {relative_source} -> {target}")
    return errors


def _manifest_records(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    pending_target: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        target_match = MANIFEST_SOURCE_TARGET.match(line)
        if target_match:
            pending_target = target_match.group(1)
            continue
        content_match = MANIFEST_CONTENT_ID.match(line)
        if content_match and pending_target:
            records.append((pending_target, content_match.group(1)))
            pending_target = None
    return records


def _manifest_targets(path: Path) -> list[str]:
    return [
        match.group(1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := MANIFEST_ANY_TARGET.match(line))
    ]


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for directory in SUPERSEDED_DOC_DIRS:
        legacy_root = root / directory
        if legacy_root.is_dir():
            for path in legacy_root.rglob("*"):
                if path.is_file():
                    errors.append(f"superseded documentation path: {path.relative_to(root).as_posix()}")

    for prefix, expected, relative in ID_CONTRACTS:
        path = root / relative
        if not path.is_file():
            continue
        ids = _record_ids(path.read_text(encoding="utf-8"), prefix)
        seen: set[str] = set()
        for item in ids:
            if item in seen:
                errors.append(f"duplicate {prefix} id: {item}")
            seen.add(item)
        if len(seen) != expected:
            errors.append(f"{prefix} count: expected {expected}, found {len(seen)}")

    coverage_path = root / "docs/02-requirements-map/coverage-matrix.md"
    if coverage_path.is_file() and "40/40 AC defined" not in coverage_path.read_text(encoding="utf-8"):
        errors.append("AC count: expected evidence '40/40 AC defined'")

    for relative in EVIDENCE_FILES:
        path = root / relative
        if path.is_file() and "DESIGNED — NOT EXECUTED" not in path.read_text(encoding="utf-8"):
            errors.append(f"missing evidence label: {relative}")

    manifest_path = root / "docs/source-manifest.yaml"
    if manifest_path.is_file():
        records = _manifest_records(manifest_path)
        targets = [target for target, _ in records]
        for required in SOURCE_TARGETS:
            count = targets.count(required)
            if count != 1:
                errors.append(f"manifest target count: {required}: expected 1, found {count}")
        for target in sorted(set(_manifest_targets(manifest_path))):
            if not (root / target).is_file():
                errors.append(f"manifest target missing file: {target}")
        content_ids = {content_id for _, content_id in records}
        if len(content_ids) != 25:
            errors.append(f"manifest content IDs: expected 25 distinct, found {len(content_ids)}")
        api_targets = {target for target, content_id in records if content_id == "229453"}
        if api_targets != API_SOURCE_TARGETS:
            errors.append("manifest content 229453 targets mismatch")

    for path in root.rglob("*.json"):
        if ".git" not in path.parts:
            errors.extend(_validate_json(path, path.relative_to(root).as_posix()))

    for path in root.rglob("*.md"):
        if ".git" not in path.parts:
            errors.extend(_validate_links(root, path))

    return sorted(set(errors))


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: repository contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
