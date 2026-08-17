# Scoring and Token Tracking

## Accuracy Model

Each workflow/subtask/model combination receives a score from 0 to 100.

Initial defaults:

- `official` capability claim: 60-70 until user testing confirms usefulness.
- `actionable` deterministic workflow rule: 70-80.
- `hypothesis`: 50-65.
- `user-observed` repeated success: 75-95.
- repeated failure: demote in steps of 5-20 depending on severity.

## Score Events

Add score when:

- the user says the output worked,
- verification passes,
- the model saved time or tokens,
- it produced a reusable artifact,
- it succeeded with fewer retries than alternatives.

Subtract score when:

- the user says it was wrong, generic, lazy, useless, or missed the point,
- a source/visual/code/accounting claim fails verification,
- the model burns premium limits on low-value work,
- it requires repeated correction,
- an alternative clearly beats it.

Suggested deltas:

- `+3`: useful but ordinary success.
- `+8`: strong success.
- `+15`: standout success; consider default promotion.
- `-5`: mild correction.
- `-10`: wrong or wasteful.
- `-20`: serious failure on an important task.

## Replacement Rule

Replace the default when an alternative has:

- at least 3 comparable successful uses,
- score at least 10 points higher,
- no unresolved privacy/security/cost issue,
- better or equal token/limit impact.

## Token Tracking

Track usage at three levels:

1. **Exact API usage** when available from provider/API logs.
2. **Codex/Claude Code usage reports** when surfaced by the tool/app.
3. **Manual estimate** for web app use, using plan-limit events and session notes.

Every substantial routed task should log:

- provider,
- model/tool,
- workflow/subtask,
- input tokens,
- output tokens,
- reasoning tokens if available,
- estimated cost or plan impact,
- whether a limit was hit or avoided,
- whether a cheaper lane could have done the work.

## Token-Savings Metric

For each workflow, compare:

- old route: one premium model handles everything,
- routed route: retrieval/extraction/tooling first, premium synthesis only when needed.

Report:

- total tokens,
- premium-model tokens,
- retries,
- time to accepted result,
- quality outcome,
- limit hits.

The router is working only if quality stays equal/better while premium-model burn and retries decline.
