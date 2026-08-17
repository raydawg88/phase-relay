from __future__ import annotations

import csv
import json
from pathlib import Path

from .router import deprecated_model_ids


MATRIX_FIELDS = {
    "workflow", "subtask", "primary_route", "secondary_route", "avoid_or_limit",
    "why", "verification", "source_basis", "status",
}


def validate_csv(path: Path, required: set[str] | None = None) -> list[str]:
    errors = []
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return [f"{path}: empty CSV"]
    width = len(rows[0])
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != width:
            errors.append(f"{path}:{number}: expected {width} columns, found {len(row)}")
    if required and not required.issubset(set(rows[0])):
        missing = sorted(required - set(rows[0]))
        errors.append(f"{path}: missing columns: {', '.join(missing)}")
    return errors


def validate_home(home: Path) -> list[str]:
    errors = []
    rules_path = home / "routing-rules.json"
    matrix_path = home / "task-matrix.csv"
    registry_path = home / "model-registry.json"
    for path in (rules_path, matrix_path, registry_path):
        if not path.exists():
            errors.append(f"missing required file: {path}")
    if errors:
        return errors

    for path in (rules_path, registry_path):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
    errors.extend(validate_csv(matrix_path, MATRIX_FIELDS))
    if errors:
        return errors

    deprecated = deprecated_model_ids(registry_path)
    with matrix_path.open(newline="", encoding="utf-8") as handle:
        for number, row in enumerate(csv.DictReader(handle), start=2):
            routes = f"{row['primary_route']} {row['secondary_route']}".lower()
            for model_id in deprecated:
                if model_id in routes:
                    errors.append(f"{matrix_path}:{number}: deprecated model referenced: {model_id}")

    telemetry = home / "telemetry"
    for name in ("scorecard.csv", "token-usage.csv"):
        path = telemetry / name
        if path.exists():
            errors.extend(validate_csv(path))
    observations = telemetry / "routing-observations.jsonl"
    if observations.exists():
        for number, line in enumerate(observations.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{observations}:{number}: invalid JSONL: {exc}")
    return errors

