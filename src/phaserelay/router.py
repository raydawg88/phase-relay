from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


PHASE_MAP = {
    "intake": ("Project orchestration", "intake and scope"),
    "research": ("Customer research", "source discovery and citation gathering"),
    "corpus": ("Long document synthesis", "very large corpus compression"),
    "media": ("Video analysis", "native first-pass visual/audio understanding"),
    "strategy": ("Product planning", "strategy and roadmap synthesis"),
    "implementation": ("Coding", "architecture/debug judgment"),
    "qa": ("QA testing", "test-plan design"),
    "delivery": ("Project delivery", "documentation and handoff"),
    "retrospective": ("Agent/model orchestration", "routing telemetry and scoring"),
}

DEFAULT_PHASES = tuple(PHASE_MAP)


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def tokens(value: str) -> set[str]:
    return set(normalize(value).split())


@dataclass(frozen=True)
class Route:
    workflow: str
    subtask: str
    primary_route: str
    secondary_route: str
    avoid_or_limit: str
    why: str
    verification: str
    source_basis: str
    status: str
    match_score: float
    adaptive_score: float
    decision: str
    observations_considered: int

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)


def read_matrix(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _match_score(workflow: str, subtask: str, row: dict[str, str]) -> float:
    workflow_query = tokens(workflow)
    subtask_query = tokens(subtask)
    workflow_row = tokens(row["workflow"])
    subtask_row = tokens(row["subtask"])

    def jaccard(left: set[str], right: set[str]) -> float:
        return len(left & right) / len(left | right) if left or right else 0.0

    workflow_score = jaccard(workflow_query, workflow_row)
    subtask_score = jaccard(subtask_query, subtask_row)
    return round((workflow_score * 0.45) + (subtask_score * 0.55), 4)


def select_route(
    matrix: list[dict[str, str]],
    workflow: str,
    subtask: str,
    observations: list[dict] | None = None,
) -> Route:
    if not workflow.strip() or not subtask.strip():
        raise ValueError("workflow and subtask are required")

    exact = [
        row
        for row in matrix
        if normalize(row["workflow"]) == normalize(workflow)
        and normalize(row["subtask"]) == normalize(subtask)
    ]
    if exact:
        selected = exact[0]
        score = 1.0
    else:
        ranked = sorted(
            ((_match_score(workflow, subtask, row), row) for row in matrix),
            key=lambda item: item[0],
            reverse=True,
        )
        score, selected = ranked[0]
        if score < 0.18:
            raise LookupError(
                "No confident route found. Add this operation to the task matrix or provide a more specific workflow/subtask."
            )

    base_scores = {"official": 65.0, "actionable": 75.0, "hypothesis": 60.0}
    primary = selected["primary_route"]
    secondary = selected["secondary_route"]
    adaptive_score = base_scores.get(selected["status"], 55.0)
    decision = "policy_default"
    relevant = []
    for item in observations or []:
        if normalize(str(item.get("workflow", ""))) != normalize(selected["workflow"]):
            continue
        if normalize(str(item.get("subtask", ""))) != normalize(selected["subtask"]):
            continue
        relevant.append(item)

    primary_events = [item for item in relevant if item.get("route_role", "primary") == "primary"]
    secondary_events = [item for item in relevant if item.get("route_role") == "secondary"]
    primary_score = adaptive_score + sum(float(item.get("score_delta") or 0) for item in primary_events)
    secondary_score = 50.0 + sum(float(item.get("score_delta") or 0) for item in secondary_events)
    primary_failures = sum(item.get("outcome") == "failure" for item in primary_events)
    secondary_successes = sum(item.get("outcome") == "success" for item in secondary_events)

    if primary_failures >= 3:
        primary, secondary = secondary, primary
        adaptive_score = secondary_score
        decision = "primary_suspended_after_three_failures"
    elif secondary_successes >= 3 and secondary_score >= primary_score + 10:
        primary, secondary = secondary, primary
        adaptive_score = secondary_score
        decision = "secondary_promoted_by_observed_score"
    else:
        adaptive_score = primary_score
        if relevant:
            decision = "policy_default_adjusted_by_observations"

    return Route(
        workflow=selected["workflow"],
        subtask=selected["subtask"],
        primary_route=primary,
        secondary_route=secondary,
        avoid_or_limit=selected["avoid_or_limit"],
        why=selected["why"],
        verification=selected["verification"],
        source_basis=selected["source_basis"],
        status=selected["status"],
        match_score=score,
        adaptive_score=round(adaptive_score, 2),
        decision=decision,
        observations_considered=len(relevant),
    )


def build_project_plan(
    matrix: list[dict[str, str]], phases: list[str], observations: list[dict] | None = None
) -> list[dict]:
    plan = []
    for phase in phases:
        key = normalize(phase).replace(" ", "_")
        aliases = {
            "source_research": "research",
            "long_context": "corpus",
            "visual_video_media_analysis": "media",
            "creative_direction": "strategy",
            "review": "qa",
            "docs": "delivery",
        }
        key = aliases.get(key, key)
        if key not in PHASE_MAP:
            raise ValueError(f"Unknown phase: {phase}")
        workflow, subtask = PHASE_MAP[key]
        route = select_route(matrix, workflow, subtask, observations)
        plan.append({"phase": key, "route": route.to_dict()})
    return plan


def deprecated_model_ids(registry_path: Path) -> set[str]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    deprecated = set()
    for provider in registry.get("models", []):
        for item in provider.get("deprecations", []):
            if item.get("model_id"):
                deprecated.add(item["model_id"].lower())
    return deprecated
