# Model Inventory v1

Last checked: 2026-08-15

This is a working inventory. It is intentionally detailed but provisional: plan limits, product surfaces, and available model menus change often.

## Major Provider Surfaces

### OpenAI and Codex

Use for: planning, coding with Codex, high-judgment synthesis, multimodal image analysis, image generation/editing, agent orchestration, final answer composition.

Likely strengths:

- Strong general reasoning and coding-agent workflows in Codex.
- Strong image understanding and generation/editing ecosystem.
- Good final synthesis when given clean source bundles.
- Good "manager" role for decomposing tasks and assigning tools.

Use sparingly for:

- raw source collection,
- long unfiltered transcript/document dumping,
- repeated extraction/classification that local or cheaper models can do.

Evidence:

- OpenAI model docs: https://platform.openai.com/docs/models
- OpenAI images/vision guide: https://platform.openai.com/docs/guides/images
- ChatGPT plans: https://chatgpt.com/pricing

### Anthropic Claude and Claude Code

Use for: deep writing, planning, product strategy, codebase reasoning, Claude Code agentic implementation, document synthesis, creative strategy, long-context reasoning.

Likely strengths:

- Strong at structured thinking, critique, product/spec work, long-form synthesis, and agentic coding.
- Good as a final editorial/strategy judge after evidence has been gathered elsewhere.

Use sparingly for:

- source discovery that Perplexity/search can do cheaper,
- brute-force batch extraction,
- first-pass OCR/transcription/tagging.

Evidence:

- Claude model overview: https://docs.anthropic.com/en/docs/about-claude/models/overview
- Claude pricing: https://www.anthropic.com/pricing
- Claude Code docs: https://docs.anthropic.com/en/docs/claude-code/overview

### Google Gemini

Use for: native video/audio-visual analysis, long-context multimodal analysis, Google ecosystem research and document handling, source-heavy comparison, large context dumps when needed.

Important nuance:

- Gemini should be a default first-pass video-analysis model because Google documents native video understanding across visual and audio streams.
- Do not claim "Gemini views every frame" as a blanket rule. Gemini API File API video is sampled/stored at 1 frame per second by default, while Vertex AI examples expose configurable FPS. For true frame-level analysis, extract frames with ffmpeg and feed keyframes or sampled frames deliberately.

Likely strengths:

- Long-context multimodal reasoning.
- Video/audio understanding and moment retrieval.
- Good source compression when given many documents.

Use sparingly for:

- final creative taste decisions without a second model review,
- codebase implementation where Codex/Claude Code has better tool integration.

Evidence:

- Gemini video understanding: https://ai.google.dev/gemini-api/docs/video-understanding
- Gemini long context: https://ai.google.dev/gemini-api/docs/long-context
- Gemini models: https://ai.google.dev/gemini-api/docs/models
- Vertex AI video understanding: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/video-understanding

### Perplexity

Use for: customer/company research, market scans, current events, cited source discovery, competitor research, "what should I read before a meeting?"

Likely strengths:

- Sourced retrieval with citations.
- Fast company/market briefing.
- Good first-pass fact collection before handing a compact evidence bundle to GPT/Claude/Gemini.

Use sparingly for:

- final product/creative judgment,
- code implementation,
- nuanced design critique from raw visuals unless paired with a visual model.

Evidence:

- Perplexity Pro: https://www.perplexity.ai/pro
- Perplexity help center: https://www.perplexity.ai/help-center
- Perplexity Sonar API docs: https://docs.perplexity.ai/

Recommendation:

- Start using it immediately for source collection and meeting prep.
- Consider API only if sourced research becomes a repeated automated step.

### Grok

Use for: quick current-culture pulse, X/Twitter-adjacent context, lightweight brainstorming, alternative takes.

Likely strengths:

- Real-time/social context if surfaced through X/Grok.
- Useful contrast model when you want a less corporate read.

Use sparingly for:

- high-stakes facts,
- source-grounded business briefs unless citations are verified,
- final financial/legal/accounting decisions,
- large codebase work on free limits.

Evidence:

- xAI models docs: https://docs.x.ai/docs/models
- Grok plans: https://grok.com/plans

## Open-Weight / Local Candidates

### Llama

Use for: local/private summarization, extraction, classification, batch tagging, inexpensive drafts, agent substeps when privacy/cost matters.

Evidence:

- Meta Llama: https://www.llama.com/
- Llama model cards: https://github.com/meta-llama/llama-models

Recommendation:

- Use through Ollama/LM Studio/OpenRouter/Together first; only invest in local GPU setup if repeated private batch work justifies it.

### Qwen

Use for: coding support, multilingual reasoning, structured extraction, open-weight trials, cost-effective batch work.

Evidence:

- Qwen docs: https://qwen.readthedocs.io/
- Qwen GitHub: https://github.com/QwenLM

Recommendation:

- Test Qwen Coder variants for cheap code review/extraction and repo Q&A before premium-model escalation.

### DeepSeek

Use for: code reasoning, math/logical reasoning, cheap second opinion, structured technical analysis.

Evidence:

- DeepSeek docs: https://api-docs.deepseek.com/
- DeepSeek GitHub: https://github.com/deepseek-ai

Recommendation:

- Use via API/router, not as default for sensitive private data unless privacy posture is acceptable.

### Mistral

Use for: fast open/commercial models, European provider option, code and structured tasks, Le Chat experiments.

Evidence:

- Mistral models: https://docs.mistral.ai/getting-started/models/models_overview/
- Mistral pricing: https://mistral.ai/pricing/

Recommendation:

- Worth trying through Le Chat/API or a router; may become a good cheaper "analyst/extractor" lane.

### Kimi / Moonshot

Use for: long-context reading and code/reasoning trials if available through OpenRouter or direct API.

Evidence:

- Moonshot AI: https://www.moonshot.ai/
- Kimi API docs: https://platform.moonshot.ai/docs

Recommendation:

- Candidate for bakeoff, especially long-context document/code tasks.

### GLM / Z.ai

Use for: open-weight reasoning/coding trials, low-cost comparison model.

Evidence:

- Z.ai: https://z.ai/
- GLM GitHub: https://github.com/THUDM

Recommendation:

- Candidate only after the main configured routes are tested.

## Model Routers / Access Layers

### OpenRouter

Use for: trying many models with one API, comparing open/proprietary models, building router prototypes.

Evidence:

- OpenRouter docs: https://openrouter.ai/docs
- OpenRouter models: https://openrouter.ai/models

Recommendation:

- Strong candidate sign-up/API key because this project is explicitly about routing.

### Together AI

Use for: hosted open-weight model inference and fine-tuning experiments.

Evidence:

- Together docs: https://docs.together.ai/
- Together models: https://docs.together.ai/docs/serverless-models

### Fireworks AI

Use for: fast open model serving, production-style open-weight APIs.

Evidence:

- Fireworks docs: https://docs.fireworks.ai/
- Fireworks models: https://fireworks.ai/models

### Hugging Face

Use for: discovering open models, hosted inference providers, model cards, datasets.

Evidence:

- Hugging Face Inference Providers: https://huggingface.co/docs/inference-providers

### Replicate

Use for: media/open model trials, especially image/video/audio utilities.

Evidence:

- Replicate docs: https://replicate.com/docs

## Creative Media Candidates

### Google Flow / Veo

Use for: high-end video generation from Google ecosystem, especially when paired with Gemini planning.

Evidence:

- Google Flow: https://labs.google/fx/tools/flow
- Veo: https://deepmind.google/models/veo/

### Sora

Use for: OpenAI video generation where available, story-driven or prompt-driven video experiments.

Evidence:

- Sora: https://openai.com/sora/

### Runway

Use for: video generation/editing, motion design, creative video iteration.

Evidence:

- Runway: https://runwayml.com/
- Runway Gen-4: https://runwayml.com/research/introducing-runway-gen-4

### Kling

Use for: video generation tests, especially motion and cinematic short clips.

Evidence:

- Kling AI: https://klingai.com/

### Higgsfield

Use for: stylized video generation and camera/motion-driven clips when credit use is controlled.

Evidence:

- Higgsfield: https://higgsfield.ai/

### Flux / Black Forest Labs

Use for: image generation, local/ComfyUI workflows, realism/design experiments.

Evidence:

- Black Forest Labs: https://blackforestlabs.ai/
- FLUX tools/API: https://docs.bfl.ai/

### Ideogram

Use for: image generation with better typography/logo/text rendering tests.

Evidence:

- Ideogram: https://ideogram.ai/

### Midjourney

Use for: high-taste creative image exploration and art direction references.

Evidence:

- Midjourney: https://www.midjourney.com/
