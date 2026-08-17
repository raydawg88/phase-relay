# Daily Model Router Update Protocol

Use this protocol for the daily watcher.

## Goal

Keep `phase-relay` current as models, plan limits, pricing, and media capabilities change.

## Daily Light Check

Search official and primary-adjacent sources for:

- new model releases,
- model retirements/deprecations,
- plan and usage-limit changes,
- context-window changes,
- multimodal changes, especially video/image/audio,
- coding-agent changes,
- API pricing changes,
- new model-router availability,
- new open-weight releases.

## Source List

Check these first:

- OpenAI models/pricing/release notes: `https://platform.openai.com/docs/models`, `https://openai.com/news/`, `https://chatgpt.com/pricing`
- Anthropic models/pricing/release notes: `https://docs.anthropic.com/en/docs/about-claude/models/overview`, `https://www.anthropic.com/news`, `https://www.anthropic.com/pricing`
- Google Gemini/DeepMind: `https://ai.google.dev/gemini-api/docs/models`, `https://ai.google.dev/gemini-api/docs/video-understanding`, `https://deepmind.google/discover/blog/`
- Perplexity: `https://www.perplexity.ai/help-center`, `https://docs.perplexity.ai/`
- xAI/Grok: `https://docs.x.ai/docs/models`, `https://x.ai/news`
- OpenRouter: `https://openrouter.ai/models`, `https://openrouter.ai/docs`
- Mistral: `https://docs.mistral.ai/getting-started/models/models_overview/`, `https://mistral.ai/news/`
- Qwen: `https://qwen.readthedocs.io/`, `https://github.com/QwenLM`
- DeepSeek: `https://api-docs.deepseek.com/`, `https://github.com/deepseek-ai`
- Hugging Face trending/open models: `https://huggingface.co/models`
- Together/Fireworks/Replicate model catalogs.
- Media tools: Sora, Google Flow/Veo, Runway, Kling, Higgsfield, Flux/Black Forest Labs, Ideogram, Midjourney.

## Output Each Day

Append the audit to the active private telemetry home, normally `~/.config/phaserelay/telemetry/daily-update-log.md`:

```text
## YYYY-MM-DD

Checked:
- source

Changes found:
- provider/model/change/source/confidence

Router impact:
- add/update/demote/no change

Human approval needed:
- yes/no and why
```

## Update Policy

Do not silently promote a new model to "best" based only on launch hype.

- Add new models as candidates.
- Mark source-backed capability changes as `official`.
- Require a bakeoff or user-observed usage before replacing a stable default.
- If a provider removes a model or changes limits/pricing materially, update the inventory immediately and flag the router impact.
- Never commit private prompts, account details, task IDs, usage records, or user feedback with a public registry update.

## Weekly Deep Check

Once a week, review:

- telemetry scorecard,
- repeated user complaints or corrections,
- token usage by workflow,
- bakeoff results,
- whether expensive frontier models are being used for source collection or formatting,
- candidates that should be signed up for, cancelled, or ignored.
