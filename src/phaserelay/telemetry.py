from __future__ import annotations

import csv
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


OBSERVATION_FIELDS = [
    "timestamp", "workflow", "subtask", "task_summary", "chosen_provider",
    "chosen_model_or_tool", "surface", "router_reason", "alternatives_considered",
    "route_role", "outcome", "user_feedback", "verification_result", "failure_mode",
    "tokens_input", "tokens_output", "estimated_cost_usd", "limit_impact",
    "score_delta", "should_update_default", "notes",
]

USAGE_FIELDS = [
    "timestamp", "provider", "model_or_tool", "surface", "workflow", "subtask",
    "task_id", "input_tokens", "output_tokens", "reasoning_tokens", "total_tokens",
    "estimated_cost_usd", "plan_limit_signal", "source", "notes",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def initialize_home(home: Path, defaults: Path, force: bool = False) -> None:
    home.mkdir(parents=True, exist_ok=True)
    telemetry = home / "telemetry"
    telemetry.mkdir(exist_ok=True)
    for name in ("routing-rules.json", "task-matrix.csv", "model-registry.json"):
        target = home / name
        if force or not target.exists():
            shutil.copy2(defaults / name, target)

    scorecard = telemetry / "scorecard.csv"
    if force or not scorecard.exists():
        scorecard.write_text(
            "workflow,subtask,provider,model_or_tool,surface,score,confidence,uses,successes,failures,last_used,last_updated,status,notes\n",
            encoding="utf-8",
        )
    observations = telemetry / "routing-observations.jsonl"
    if force or not observations.exists():
        schema = {"schema_version": "0.1.0", "record_type": "schema", "fields": OBSERVATION_FIELDS}
        observations.write_text(json.dumps(schema) + "\n", encoding="utf-8")
    usage = telemetry / "token-usage.csv"
    if force or not usage.exists():
        usage.write_text(",".join(USAGE_FIELDS) + "\n", encoding="utf-8")


def append_observation(path: Path, values: dict) -> None:
    record = {field: values.get(field, "") for field in OBSERVATION_FIELDS}
    record["timestamp"] = record["timestamp"] or utc_now()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def read_observations(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if item.get("record_type") != "schema":
            rows.append(item)
    return rows


def append_usage(path: Path, values: dict) -> None:
    record = {field: values.get(field, "") for field in USAGE_FIELDS}
    record["timestamp"] = record["timestamp"] or utc_now()
    input_tokens = int(record["input_tokens"] or 0)
    output_tokens = int(record["output_tokens"] or 0)
    reasoning_tokens = int(record["reasoning_tokens"] or 0)
    record["total_tokens"] = int(record["total_tokens"] or input_tokens + output_tokens + reasoning_tokens)
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=USAGE_FIELDS)
        writer.writerow(record)


def report(home: Path) -> dict:
    telemetry = home / "telemetry"
    usage_path = telemetry / "token-usage.csv"
    observation_path = telemetry / "routing-observations.jsonl"
    usage = []
    if usage_path.exists():
        with usage_path.open(newline="", encoding="utf-8") as handle:
            usage = list(csv.DictReader(handle))
    observations = read_observations(observation_path)

    provider_tokens: dict[str, int] = defaultdict(int)
    total_tokens = 0
    total_cost = 0.0
    for row in usage:
        amount = int(float(row.get("total_tokens") or 0))
        total_tokens += amount
        total_cost += float(row.get("estimated_cost_usd") or 0)
        provider_tokens[row.get("provider") or "unknown"] += amount
    outcome_counts: dict[str, int] = defaultdict(int)
    for item in observations:
        outcome_counts[item.get("outcome") or "unknown"] += 1
    return {
        "usage_rows": len(usage),
        "observation_rows": len(observations),
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(total_cost, 6),
        "tokens_by_provider": dict(sorted(provider_tokens.items(), key=lambda item: item[1], reverse=True)),
        "outcomes": dict(outcome_counts),
    }
