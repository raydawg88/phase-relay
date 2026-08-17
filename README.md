# PhaseRelay

**Adaptive model routing for whole projects.**

One model should not research the market, inspect every screenshot, architect the system, write every line, test the interface, and judge its own work. PhaseRelay turns a project into operations, routes each operation to the model or deterministic tool best suited to it, and learns from what actually works.

It is a routing layer for Codex, Claude Code, and agent workflows that care about two things at the same time:

- better output from specialist models and tools;
- less premium-token waste on retrieval, extraction, and mechanical work.

PhaseRelay is not another model leaderboard. It is an evidence loop.

## What It Does

```text
Project request
    |
    +-- research ----------> sourced search / retrieval
    +-- corpus review -----> long-context model
    +-- video analysis ----> multimodal model + extracted frames
    +-- product judgment --> frontier reasoning model
    +-- implementation ----> coding agent + deterministic tools
    +-- QA ----------------> tests, browser evidence, visual review
    +-- retrospective -----> outcome scores + token telemetry
```

PhaseRelay ships with:

- a granular workflow matrix for research, video, design, code, QA, finance, writing, product, marketing, and private batch work;
- phase-by-phase project plans instead of one-model-per-prompt guesses;
- a sourced model registry with deprecation awareness;
- append-only feedback and token telemetry;
- Codex and Claude Code skill instructions;
- a zero-runtime-dependency Python CLI;
- regression tests and policy validation.

## Why PhaseRelay

Most routers optimize one API call. PhaseRelay optimizes the life of a project.

The expensive model gets the decision that deserves it. Search tools gather current evidence. Scripts do exact calculations. Multimodal models inspect media. Coding agents implement. Tests and rendered output verify. The router records whether the route succeeded, failed, burned limits, or needed repeated correction.

New models enter as candidates. They do not become defaults because a launch post says they are brilliant. Promotion requires comparable bakeoffs or observed success.

## Quick Start

```bash
git clone https://github.com/raydawg88/phase-relay.git
cd phase-relay
python3 -m pip install .
phase-relay init
phase-relay validate
```

Route one operation:

```bash
phase-relay route \
  --workflow "Video analysis" \
  --subtask "frame-level forensic critique"
```

Create a whole-project plan:

```bash
phase-relay plan --phases intake,research,corpus,media,strategy,implementation,qa,delivery,retrospective
```

Use `--json` on `route`, `plan`, `validate`, or `report` for agent-friendly output.

## Teach It What Works

Record a result:

```bash
phase-relay observe \
  --workflow "Coding" \
  --subtask "architecture/debug judgment" \
  --provider "OpenAI" \
  --model "Codex frontier" \
  --outcome success \
  --score-delta 8 \
  --verification "tests passed"
```

Record usage:

```bash
phase-relay usage \
  --provider OpenAI \
  --model gpt-example \
  --workflow Coding \
  --subtask implementation \
  --input 12000 \
  --output 2400 \
  --cost 0.18

phase-relay report
```

Your editable policy and telemetry live in `~/.config/phaserelay` by default. Set `PHASERELAY_HOME` or pass `--home` to isolate a team, project, or experiment.

## Agent Installation

```bash
python3 scripts/install_skill.py
```

The installer places the portable `phase-relay` skill in detected Codex and Claude skill directories. The skill tells the orchestrator when to route, what evidence to preserve, how to hand work across execution surfaces, and when not to spend a frontier call.

PhaseRelay cannot magically mutate the model selected in an external product. It can route automatically only through execution surfaces the current environment exposes: subagents, provider CLIs, APIs, MCP tools, scheduled jobs, or explicit handoff artifacts. It reports that boundary instead of faking a handoff.

## Trust Model

Every recommendation carries an evidence status:

- `official`: the provider documents the capability;
- `hypothesis`: plausible, but not yet proven in comparable use;
- `actionable`: a deterministic workflow rule that can be verified;
- `observed`: repeated real-world outcomes support the route.

Frame-level video claims require extracted frames or a documented sampling rate. Financial calculations require deterministic reconciliation. Current facts require source verification. UI claims require rendered or browser evidence. A model never grades itself alone on important work.

## Repository Map

```text
src/phaserelay/          CLI, routing engine, telemetry, validation
src/phaserelay/defaults Public routing matrix, rules, model registry
skills/phase-relay/      Portable Codex and Claude skill
docs/                    Routing, scoring, and update protocols
examples/telemetry/      Empty public-safe telemetry templates
tests/                   Unit and end-to-end regression tests
```

## Status

PhaseRelay is alpha software. The policy engine, project planner, validator, telemetry writer, reporter, installer, and test suite work locally. The included model rankings remain intentionally conservative until more comparable outcome data exists.

Provider plans, pricing, identifiers, and model behavior change quickly. Run the update protocol, validate the registry, and bake off candidates before changing a stable default.

## Contributing

Good contributions bring evidence: a reproducible task, the exact execution surface and model ID, verification artifacts, token/cost data when available, and a clear reason the route should move.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/scoring-and-token-tracking.md](docs/scoring-and-token-tracking.md).

## License

MIT
