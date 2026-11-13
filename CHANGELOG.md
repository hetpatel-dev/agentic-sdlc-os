# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-11-13

### Fixed
- **Agent Catalog:** Created dedicated `code-reviewer.md` persona for Gate G4 independent review (31 agents total).
- **Agent Tools:** Granted `call_mcp_tool`, `list_resources`, and `read_resource` permissions to coordinating and auditing agents.
- **Gate Validator:** Fixed monotonic gate advancement bug preventing gate regressions; added AST-based exception swallow detection for Python; normalized Windows path matching; added concrete evidence validation for Gates G7, G8, G9, G10, and G11.
- **Traceability CLI:** Added CLI subcommands for `create-objective`, `create-requirement`, and `create-adr`; populated top-level ledger dictionaries for OBJ-001, OBJ-002, REQ-101, REQ-102, REQ-201, and ADR-0001; reconciled governance history for TASK-102; regenerated traceability matrix.
- **Security Scanner & Hooks:** Integrated Antigravity JSON stdin/stdout protocol into `scripts/security_check.py`; added Windows dangerous command patterns; excluded binary files from directory scan; re-enabled automated pre-command and post-write hooks.
- **Authentication Service:** Hardened `AuthService` with cryptographically secure `secrets.token_bytes(16)` salt generation, JWT header algorithm validation (`alg == "HS256"`), and reserved claims protection; added REST API controller `AuthAPI` implementing `/auth/login` and `/auth/verify`.
- **Distribution & Links:** Fixed broken relative links in `rules/GEMINI.md`; synchronized 15 modular rule files to `rules/`; added offline local source copy fallback to `scripts/install.ps1` and `scripts/install.sh`; dynamically resolved Git bash path and enforced pre-commit exit codes in `scripts/bootstrap.ps1`.
- **Consumer Scaffolding Isolation:** Updated `scripts/install.ps1` and `scripts/install.sh` to strictly exclude testing/reference artifacts from new projects; scaffold only empty `docs/` subdirectories and `docs/templates/`; initialize consumer projects with a pristine empty traceability ledger (`tasks: {}`, `requirements: {}`, `objectives: {}`, `adrs: {}`) written as UTF-8 without BOM.
- **Traceability Numbering from 1:** Updated `scripts/traceability_cli.py` to auto-assign initial IDs starting from 1 (`TASK-001`, `OBJ-001`, `REQ-001`, `ADR-0001`); aligned standard documentation templates, agent directives, and rules to index starting at 1.

## [1.0.0] - 2026-11-13

### Added
- **Framework:** Initial production release of **Agentic SDLC OS** for Google Antigravity.
- **Domains & Agents:** 16 domain leads, 8 cross-domain critics/auditors (including `code-reviewer`), and 6 specialized workers in `.agents/agents/` (31 agents total).
- **Engineering Rules:** 15 modular engineering rule files in `.agents/rules/`.
- **Skills & Workflows:** 18 orchestration and domain execution skills in `.agents/skills/`.
- **Quality Gates:** 12 automated quality gates (G0 to G11) with validation CLI (`scripts/gate_validator.py`).
- **Traceability Ledger:** Bidirectional traceability system linking objectives, requirements, ADRs, code, and tests (`scripts/traceability_cli.py`).
- **Security Scanner:** Automated secret and dangerous command scanner hook (`scripts/security_check.py`).
- **MCP Servers:** Stdio servers for traceability and gate validation (`.agents/mcp_config.json`).
- **Authentication Service:** Reference production feature in `src/auth/service.py` with 100% test coverage (`tests/test_auth_service.py`), tracing `REQ-101` and `REQ-102`.
- **Documentation & Templates:** Full set of standard templates in `docs/templates/`.
