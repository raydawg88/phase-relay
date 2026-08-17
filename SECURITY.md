# Security

Do not report a secret or private prompt in a public issue. Send vulnerability reports to the repository owner through GitHub's private security advisory flow.

PhaseRelay stores local telemetry in `~/.config/phaserelay` unless another home is selected. Treat that directory as private: it may contain project names, model usage, costs, feedback, and execution metadata.

The CLI does not send prompts or telemetry over the network. Provider CLIs, APIs, MCP servers, and routers used by an agent have their own data-handling policies and must be reviewed separately.

