# Agentic SDLC OS — Gemini Directive

This project uses the **Agentic SDLC Operating System**.
All agents, subagents, and sessions must adhere strictly to the engineering charter defined in [AGENTS.md](./AGENTS.md) and modular rules defined in [.agents/rules/](../.agents/rules/).

### Core Guidelines
1. Read [.agents/rules/00-core-engineering.md](../.agents/rules/00-core-engineering.md) before writing code.
2. Ensure every task has an entry in `governance/traceability_ledger.json` using `python scripts/traceability_cli.py`.
3. Validate transitions with `python scripts/gate_validator.py`.
4. Never bypass quality gates G0-G11.
