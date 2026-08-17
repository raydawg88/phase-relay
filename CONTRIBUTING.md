# Contributing to PhaseRelay

PhaseRelay improves through reproducible evidence, not provider hype.

## Development

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
phase-relay validate
```

## Routing Changes

A pull request that changes a default should include:

- the workflow and subtask;
- exact provider, model ID, and execution surface;
- at least three comparable runs, or one standout result clearly labeled for review;
- verification evidence;
- quality, retry, latency, and token/cost impact;
- privacy or access constraints.

New releases enter as candidates first. Deprecations may be updated immediately from official documentation.

Never commit prompts, task IDs, customer information, private media, API keys, account-limit screenshots, or personal telemetry.

