# Research Plan

## Objective

Build a sourced, granular model-routing matrix that reduces usage-limit burn while improving output quality for recurring workflows.

## Research Standards

- Prefer official product docs, model cards, system cards, pricing pages, and provider help pages.
- Use benchmarks only as secondary evidence because creative direction, video critique, planning, coding agents, and business context are poorly represented by public benchmarks.
- Separate confirmed capability, observed user preference, and hypotheses needing a bakeoff.
- Record date-sensitive details with a `last_checked` date.
- Treat plan limits, available models, and product surfaces as volatile. Re-check before making subscription decisions.

## Evidence Tiers

- `official`: provider docs, model cards, pricing/help pages.
- `primary-adjacent`: official blog announcements, release notes, GitHub model cards.
- `benchmark`: third-party evals, leaderboards, independent tests.
- `user-observed`: results from the user's own tasks.
- `hypothesis`: plausible but unproven routing preference.

## Phase 1: Inventory

Catalog models and execution surfaces available in the target environment:

- OpenAI: ChatGPT, Codex, API, and media models as available.
- Anthropic: Claude app, Claude Code, and API as available.
- Google: Gemini app, API, Flow/Veo, and long-context products as available.
- xAI/Grok: app, X, API, or partner surfaces as available.
- Perplexity: plan status and available advanced models to verify.

Catalog candidates:

- Perplexity Pro / Sonar API for sourced retrieval.
- OpenRouter for broad model trials.
- Together, Fireworks, Hugging Face, Replicate for open-weight and media model access.
- Mistral Le Chat/API.
- Local Ollama/LM Studio/vLLM models for extraction/tagging/private batch work.
- Media tools: Runway, Kling, Higgsfield, Midjourney, Ideogram, Flux/ComfyUI, Google Flow/Veo, Sora.

## Phase 2: Task Decomposition

Break each workflow into operations. Example:

- Customer research: source discovery, official-fact extraction, market framing, meeting questions, brief writing, claim verification.
- Video analysis: upload/native video pass, shot/timecode inventory, camera/edit/grade analysis, recreation prompt, storyboard, implementation.
- Design/image critique: factual visual inventory, composition critique, brand-system fit, production recreation, generation/editing.
- Coding: repo search, architecture judgment, implementation, test writing, failure triage, review.
- QA: deterministic test design, browser/device inspection, screenshot comparison, bug-risk synthesis.

## Phase 3: Bakeoff

Create repeatable prompts and score outputs across quality, source grounding, cost/limit impact, speed, and follow-up usefulness.

Minimum bakeoff set:

1. customer meeting prep from a company URL,
2. 30-90 second video critique and recreation plan,
3. design image critique,
4. product planning memo,
5. codebase bug fix plan,
6. QA test plan,
7. finance/accounting analysis,
8. marketing campaign/distribution plan,
9. creative writing sample,
10. agent-orchestration plan.

## Phase 4: Skillization

Package the routing rules as a local skill named `phase-relay` so Codex/Claude Code planning can:

- choose the primary model/tool per operation,
- assign cheap/fallback routes,
- warn when a task is being over-modeled,
- require verification for current facts, visual claims, financial/legal facts, and rendered outputs,
- preserve a memory of user-observed winners.
