# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-13

### Added
- **Framework:** Initial production release of **Agentic SDLC OS** for Google Antigravity.
- **Domains & Agents:** 16 domain leads, 7 cross-domain critics/auditors, and 6 specialized workers in `.agents/agents/`.
- **Engineering Rules:** 15 modular engineering rule files in `.agents/rules/`.
- **Skills & Workflows:** 18 orchestration and domain execution skills in `.agents/skills/`.
- **Quality Gates:** 12 automated quality gates (G0 to G11) with validation CLI (`scripts/gate_validator.py`).
- **Traceability Ledger:** Bidirectional traceability system linking objectives, requirements, ADRs, code, and tests (`scripts/traceability_cli.py`).
- **Security Scanner:** Automated secret and dangerous command scanner hook (`scripts/security_check.py`).
- **MCP Servers:** Stdio servers for traceability and gate validation (`.agents/mcp_config.json`).
- **Authentication Service:** Reference production feature in `src/auth/service.py` with 100% test coverage (`tests/test_auth_service.py`), tracing `REQ-101` and `REQ-102`.
- **Documentation & Templates:** Full set of standard templates in `docs/templates/`.
