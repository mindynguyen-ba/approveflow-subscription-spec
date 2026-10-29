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
    "docs/01-scope-and-decisions/decisions-log.md",
    "docs/01-scope-and-decisions/assumptions-log.md",
    "docs/01-scope-and-decisions/open-questions.md",
    "docs/02-process-and-states/state-machines.md",
    "docs/02-process-and-states/bpmn-workflows.md",
    "docs/assets/state-machines/state-subscription-lifecycle.png",
    "docs/assets/state-machines/state-change-request-lifecycle.png",
    "docs/assets/bpmn/bpmn-scheduled-downgrade.png",
    "docs/assets/bpmn/bpmn-payment-failure-recovery.png",
    "docs/03-specifications/user-stories-ac.md",
    "docs/03-specifications/data-dictionary.md",
    "docs/03-specifications/api-contracts.md",
    "docs/03-specifications/sql-invariants.md",
    "docs/04-testing-and-uat/uat-specification.md",
    "poc-automation/README.md",
    "poc-automation/postman/approveflow_mocks.json",
    "poc-automation/n8n/workflow_export.json",
)

ID_CONTRACTS = (
    ("DEC", 20, "docs/01-scope-and-decisions/decisions-log.md"),
    ("ASM", 25, "docs/01-scope-and-decisions/assumptions-log.md"),
    ("OQ", 27, "docs/01-scope-and-decisions/open-questions.md"),
    ("US", 6, "docs/03-specifications/user-stories-ac.md"),
    ("SQL", 8, "docs/03-specifications/sql-invariants.md"),
    ("UAT", 9, "docs/04-testing-and-uat/uat-specification.md"),
)

EVIDENCE_FILES = (
    "docs/03-specifications/api-contracts.md",
    "docs/04-testing-and-uat/uat-specification.md",
)

SECRET_KEYS = re.compile(r"(?:api[_-]?key|authorization|password|secret|token)", re.IGNORECASE)
PLACEHOLDERS = ("", "redacted", "changeme", "placeholder")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _record_ids(text: str, prefix: str) -> list[str]:
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


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

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

    stories_path = root / "docs/03-specifications/user-stories-ac.md"
    if stories_path.is_file() and "40/40 AC defined" not in stories_path.read_text(encoding="utf-8"):
        errors.append("AC count: expected evidence '40/40 AC defined'")

    for relative in EVIDENCE_FILES:
        path = root / relative
        if path.is_file() and "DESIGNED — NOT EXECUTED" not in path.read_text(encoding="utf-8"):
            errors.append(f"missing evidence label: {relative}")

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
