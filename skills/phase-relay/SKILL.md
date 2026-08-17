---
name: phase-relay
description: Use for substantial planning, project build-out, model selection, agent orchestration, research, coding, design, media analysis, QA, finance, marketing, or any multi-phase task where work should be routed across models and deterministic tools while tracking quality and token usage.
---

# PhaseRelay

Route by project phase and operation, not by whole prompt.

The objective is better verified output with less avoidable premium-model usage. Retrieval tools gather current facts. Deterministic tools handle exact computation and checks. Multimodal specialists inspect media. Frontier models make high-value judgments. Real outcomes update the route.

## Start A Project

For a substantial project, identify the relevant phases:

- intake,
- research,
- corpus,
- media,
- strategy,
- implementation,
- qa,
- delivery,
- retrospective.

If the PhaseRelay CLI is installed, request the plan before broad execution:

```bash
phase-relay plan --phases research,strategy,implementation,qa,delivery --json
```

Use only relevant phases. If a workflow is more specific, query it directly:

```bash
phase-relay route --workflow "Video analysis" --subtask "frame-level forensic critique" --json
```

Treat the result as a scored default, not an irreversible command. Override it when access, privacy, evidence, task risk, or observed performance requires a different route.

## Execute The Route

Automatic switching means using execution surfaces exposed by the environment:

- deterministic shell, browser, spreadsheet, test, and media-inspection tools;
- bounded subagents with an explicit model override;
- provider CLIs or APIs with an explicit model ID;
- MCP tools and connected apps;
- scheduled jobs;
- explicit handoff artifacts when the target model is not callable.

Do not claim that the current chat model changed mid-turn unless the environment reports that behavior. For delegated work, record execution surface, requested model, resolved model, and task/worker name separately.

If the preferred model is unavailable, use the configured secondary route or create a handoff containing the exact model/tool, prompt/input, expected output, return location, and continuation step.

## Routing Principles

- Source research: search or retrieval first; open and verify important citations.
- Long corpus: long-context model for compression; frontier model for final judgment.
- Video: native multimodal pass first; extract frames for frame-level claims.
- Image/design: establish visual facts before critique or taste judgments.
- Coding: search, tests, build, lint, diffs, and rendered evidence before model review.
- Finance: deterministic calculations plus authoritative current sources.
- Strategy and creative direction: frontier model after evidence is compacted.
- Batch/private work: scripts or local/open models where quality and privacy permit.
- Media generation: specialized generators; score rendered output, not prompts.

## Evidence And Escalation

Escalate to a top model for ambiguous, high-cost, high-risk, externally representative, architectural, or taste-heavy decisions. Do not escalate formatting, retrieval, mechanical extraction, deterministic computation, or raw log reading.

Every completed phase should leave an artifact, source bundle, test result, screenshot/media sample, telemetry event, or explicit no-op reason.

## Feedback Loop

Record meaningful outcomes when the CLI is initialized:

```bash
phase-relay observe \
  --workflow "Coding" \
  --subtask "architecture/debug judgment" \
  --provider "OpenAI" \
  --model "resolved-model-id" \
  --outcome success \
  --score-delta 8 \
  --verification "tests passed"
```

Record exact usage when available with `phase-relay usage`. Use manual limit signals when an app does not expose token counts.

Promote a replacement only after at least three comparable successes, a score advantage of at least ten points, no unresolved privacy/cost issue, and equal or better token impact. Three serious failures for one operation trigger a replacement bakeoff.

## Freshness

Model availability, prices, plans, context windows, and media behavior drift. Validate current policy with:

```bash
phase-relay validate
```

Add new releases as candidates. Apply official deprecations promptly. Do not promote launch claims without observed evidence or a controlled bakeoff.
