# Project-Level Routing Protocol

Use this when the user is building a project, product, demo, creative system, research package, app, website, video workflow, or any multi-phase deliverable.

## Goal

The router should operate across the whole project lifecycle, not only choose one model for one prompt.

For every project, maintain:

- project objective,
- phase map,
- model/tool routing per phase,
- artifacts created,
- verification completed,
- routing observations,
- token/limit notes,
- phase handoffs.

## Project Phases

### 1. Intake and Scope

Primary route: GPT/Codex or Claude for structured clarification and project framing.

Use when:

- the project is ambiguous,
- success criteria are unclear,
- tradeoffs matter.

Output:

- objective,
- constraints,
- definition of done,
- risk areas,
- first routing plan.

### 2. Source and Market Research

Primary route: Perplexity or web search.

Use for:

- company/customer research,
- market research,
- competitor scans,
- current facts,
- model/provider updates,
- legal/financial/current claims.

Output:

- compact sourced evidence bundle,
- source links,
- claim confidence.

### 3. Long Context and Corpus Review

Primary route: Gemini for very large or multimodal context; Claude/GPT for final synthesis.

Use for:

- huge docs,
- many PDFs/pages,
- mixed media,
- long transcripts.

Output:

- extracted facts,
- contradictions,
- useful excerpts,
- questions for final judgment.

### 4. Visual, Video, and Media Analysis

Primary route:

- Gemini for native video/audio understanding,
- GPT/Gemini/Claude vision for image/design facts,
- ffmpeg/contact sheets for frame-level video claims.

Output:

- observed facts,
- timecodes/frame references,
- creative critique,
- recreation plan,
- verification notes.

### 5. Strategy and Creative Direction

Primary route: Claude or GPT frontier.

Use for:

- product direction,
- narrative,
- brand/design strategy,
- roadmap,
- creative concept,
- final synthesis.

Output:

- recommended direction,
- alternatives,
- rationale,
- assumptions,
- decision points.

### 6. Implementation

Primary route: Codex/GPT frontier or Claude Code.

Use for:

- coding,
- repo edits,
- scripts,
- site/app build,
- automation,
- data processing.

Guardrail:

- deterministic tools first for search, tests, builds, file inspection, spreadsheets, and calculations.

Output:

- changed files,
- commands run,
- verification.

### 7. QA and Review

Primary route:

- deterministic tests/build/lint,
- Playwright/browser screenshots,
- GPT/Claude review for risk,
- Gemini/GPT vision for visual QA where needed.

Output:

- pass/fail,
- screenshots or test artifacts,
- issues found,
- residual risks.

### 8. Delivery and Documentation

Primary route: GPT/Claude for concise final packaging.

Use for:

- docs,
- handoffs,
- release notes,
- client-facing summaries,
- user instructions.

Output:

- final artifact summary,
- provenance,
- what was verified,
- what remains open.

### 9. Retrospective and Score Update

Primary route: deterministic telemetry update plus GPT/Claude synthesis.

Use after meaningful project work.

Output:

- routing observations appended,
- token usage logged when available,
- scorecard updates proposed,
- model defaults promoted/demoted only with evidence.

## Project Routing Block

For project work, use this instead of the shorter single-task routing block:

```text
Project routing:
- Intake/scope:
- Source research:
- Long-context/corpus review:
- Visual/video/media analysis:
- Strategy/creative direction:
- Implementation:
- QA/review:
- Delivery/docs:
- Retrospective/scoring:
- Token guardrail:
- Handoff checkpoints:
```

Omit lanes that are irrelevant.

## Automatic Switching Reality

The router should automatically choose the right lane in the plan and use available local tools/connectors where possible. It cannot silently change an external app's selected model unless the current environment exposes that capability.

In Codex, automatic project routing can use multiple execution surfaces:

- current main task for orchestration and integration,
- Codex subagents for bounded parallel work using the model overrides advertised by the active subagent tool,
- the locally authenticated Claude Code CLI for Anthropic-side pair programming, implementation, and review,
- separate Codex tasks/threads for larger project phases,
- existing threads continued with model overrides,
- scheduled automations for recurring watcher/research work,
- deterministic local tools for search, tests, builds, scripts, and verification.

The current chat's underlying model is not mutated mid-turn. Instead, the router can delegate to a subagent/thread/automation with a model override and then integrate the result back into the main project.

For every handoff, log four distinct identities when available:

- execution surface,
- requested model identifier or alias,
- resolved model identifier returned by usage metadata,
- task/worker name.

Never infer that a model is unavailable merely because it is absent from the Codex subagent picker. Probe the provider-specific execution adapter. Conversely, historical success does not prove current availability; experimental/private identifiers such as Fable must pass a cheap live probe before receiving a real phase.

When a required model/tool is not callable from the current environment, create a handoff:

- exact model/tool to use,
- exact prompt/input,
- expected output,
- where to save/paste the result,
- how the router will continue afterward.

## Evidence Rule

Every phase should produce either:

- an artifact,
- a source bundle,
- a test/check result,
- a screenshot/media sample,
- a routing observation,
- or an explicit no-op reason.
