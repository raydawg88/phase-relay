from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .router import DEFAULT_PHASES, build_project_plan, read_matrix, select_route
from .telemetry import append_observation, append_usage, initialize_home, read_observations, report
from .validation import validate_home


DEFAULTS = Path(__file__).resolve().parent / "defaults"


def default_home() -> Path:
    return Path(os.environ.get("PHASERELAY_HOME", Path.home() / ".config" / "phaserelay"))


def active_home(home: Path) -> Path:
    return home if (home / "task-matrix.csv").exists() else DEFAULTS


def output(value: object, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2))
        return
    if isinstance(value, dict):
        for key, item in value.items():
            print(f"{key.replace('_', ' ').title()}: {item}")
    else:
        print(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="phase-relay", description="Adaptive model routing for whole projects.")
    parser.add_argument("--home", type=Path, default=default_home(), help="Configuration and telemetry directory")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create an editable local configuration and empty telemetry store")
    init.add_argument("--force", action="store_true")

    route = sub.add_parser("route", help="Choose a route for one operation")
    route.add_argument("--workflow", required=True)
    route.add_argument("--subtask", required=True)
    route.add_argument("--json", action="store_true")

    plan = sub.add_parser("plan", help="Build a phase-by-phase project routing plan")
    plan.add_argument("--phases", default=",".join(DEFAULT_PHASES), help="Comma-separated phase names")
    plan.add_argument("--json", action="store_true")

    validate = sub.add_parser("validate", help="Validate policy and telemetry files")
    validate.add_argument("--json", action="store_true")

    observe = sub.add_parser("observe", help="Append an outcome used to improve future routing")
    observe.add_argument("--workflow", required=True)
    observe.add_argument("--subtask", required=True)
    observe.add_argument("--provider", required=True)
    observe.add_argument("--model", required=True)
    observe.add_argument("--outcome", required=True, choices=("success", "partial", "failure"))
    observe.add_argument("--route-role", choices=("primary", "secondary", "override"), default="primary")
    observe.add_argument("--score-delta", type=int, default=0)
    observe.add_argument("--feedback", default="")
    observe.add_argument("--verification", default="")
    observe.add_argument("--surface", default="")
    observe.add_argument("--failure-mode", default="")
    observe.add_argument("--notes", default="")

    usage = sub.add_parser("usage", help="Append token/cost usage")
    usage.add_argument("--provider", required=True)
    usage.add_argument("--model", required=True)
    usage.add_argument("--workflow", required=True)
    usage.add_argument("--subtask", required=True)
    usage.add_argument("--input", type=int, default=0)
    usage.add_argument("--output", type=int, default=0)
    usage.add_argument("--reasoning", type=int, default=0)
    usage.add_argument("--cost", type=float, default=0)
    usage.add_argument("--surface", default="")

    summary = sub.add_parser("report", help="Summarize routing outcomes and token usage")
    summary.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    home = args.home
    try:
        if args.command == "init":
            initialize_home(home, DEFAULTS, args.force)
            print(f"Initialized PhaseRelay at {home}")
            return 0
        if args.command == "route":
            source = active_home(home)
            observations = read_observations(home / "telemetry" / "routing-observations.jsonl") if home != DEFAULTS else []
            route = select_route(read_matrix(source / "task-matrix.csv"), args.workflow, args.subtask, observations)
            output(route.to_dict(), args.json)
            return 0
        if args.command == "plan":
            source = active_home(home)
            phases = [phase.strip() for phase in args.phases.split(",") if phase.strip()]
            observations = read_observations(home / "telemetry" / "routing-observations.jsonl") if home != DEFAULTS else []
            plan = build_project_plan(read_matrix(source / "task-matrix.csv"), phases, observations)
            output({"phases": plan}, args.json)
            return 0
        if args.command == "validate":
            source = active_home(home)
            errors = validate_home(source)
            result = {"valid": not errors, "errors": errors, "home": str(source)}
            output(result, args.json)
            return 0 if not errors else 1
        if args.command in {"observe", "usage", "report"} and not home.exists():
            raise RuntimeError(f"Initialize a telemetry home first: phase-relay --home {home} init")
        if args.command == "observe":
            append_observation(home / "telemetry" / "routing-observations.jsonl", {
                "workflow": args.workflow, "subtask": args.subtask,
                "chosen_provider": args.provider, "chosen_model_or_tool": args.model,
                "outcome": args.outcome, "score_delta": args.score_delta,
                "route_role": args.route_role,
                "user_feedback": args.feedback, "verification_result": args.verification,
                "surface": args.surface, "failure_mode": args.failure_mode, "notes": args.notes,
            })
            print("Observation recorded")
            return 0
        if args.command == "usage":
            append_usage(home / "telemetry" / "token-usage.csv", {
                "provider": args.provider, "model_or_tool": args.model,
                "surface": args.surface, "workflow": args.workflow, "subtask": args.subtask,
                "input_tokens": args.input, "output_tokens": args.output,
                "reasoning_tokens": args.reasoning, "estimated_cost_usd": args.cost,
                "source": "manual_cli",
            })
            print("Usage recorded")
            return 0
        if args.command == "report":
            output(report(home), args.json)
            return 0
    except (ValueError, LookupError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"phase-relay: {exc}", file=sys.stderr)
        return 2
    return 1
