# Agentic SDLC Operating System — Universal Engineering Charter

This repository is powered by **Agentic SDLC OS**, an AI-native Software Development Lifecycle (SDLC) operating system orchestrated through Antigravity. It organizes software engineering into 16 disciplines, specialized autonomous agents, modular rules, reusable skills, explicit tool permissions, and enforceable quality gates.

---

## 1. Core Operating Principles (Non-Negotiable)

1. **Independent Verification (No Self-Approval)**: An agent who writes code, specifications, or configurations must NEVER approve its own work. Changes require independent review by designated review agents (`independent-verifier`, `code-reviewer`, `technical-critic`, `security-lead`, or authorized human).
2. **Execution Evidence Over Assumptions**: Never claim tests, linters, or builds pass without executing them and recording real terminal output. Imagined or synthetic pass states are strictly forbidden.
3. **Traceability by Default**: Every code change, test case, schema change, or configuration must trace backward to an approved requirement ID (`REQ-XXX`) or approved engineering task (`TASK-XXX`).
4. **Zero Silent Contract Breaks**: Never alter established public APIs, data schemas, or messaging payloads without an approved Architecture Decision Record (ADR), deprecation plan, and migration path.
5. **Least-Privilege and Secret Zero**: Never hardcode secrets, tokens, keys, or credentials in source code or documentation. Never perform destructive or production-impacting commands without explicit confirmation.
6. **Reversibility and Modularity**: All changes must be scoped, modular, and accompanied by automated rollback procedures or undo migrations.

---

## 2. SDLC Domain Architecture (16 Disciplines)

| Domain | Scope | Lead Agent | Primary Skills |
| :--- | :--- | :--- | :--- |
| **1. Strategy** | Market research, business case, vision | `product-strategist` | `product-discovery` |
| **2. Requirements** | PRD, SRS, user stories, acceptance criteria | `requirements-engineer` | `prd-generation`, `requirements-validation` |
| **3. Architecture** | System design, domain modeling, ADRs | `solution-architect` | `system-design`, `architecture-review` |
| **4. UX/UI** | User journeys, design systems, a11y | `ux-design-lead` | `system-design` |
| **5. Delivery** | Sprint planning, estimation, risk tracking | `delivery-manager` | `continuous-improvement` |
| **6. Development** | Frontend, backend, mobile, integrations | `engineering-lead` | `feature-implementation`, `api-development` |
| **7. Data** | Data schemas, pipelines, ETL, governance | `data-engineering-lead` | `database-change` |
| **8. Quality** | Unit, integration, E2E, contract tests | `qa-lead` | `test-automation` |
| **9. Security** | Threat modeling, SAST, SCA, IAM audits | `security-lead` | `security-assessment` |
| **10. Performance**| Benchmarks, profiling, resilience, budgets | `performance-lead` | `performance-assessment` |
| **11. DevOps** | CI/CD pipelines, IaC, containers, cloud | `platform-engineer` | `ci-cd-setup` |
| **12. Release** | SemVer, changelogs, rollback plans | `release-manager` | `release-readiness` |
| **13. Operations** | Provisioning, deployments, health checks | `operations-lead` | `production-deployment` |
| **14. Observability**| Telemetry (logs/metrics/traces), incidents | `sre-lead` | `incident-response` |
| **15. Maintenance** | Debt remediation, refactoring, upgrades | `maintenance-lead` | `technical-modernization` |
| **16. Governance** | Compliance, standards audit, DORA metrics | `engineering-governance-lead` | `continuous-improvement` |

---

## 3. Hierarchical Agent Organization

- **L0 Executive Orchestrator (`sdlc-orchestrator`)**: Coordinates lifecycle workflows, decomposes business requests, manages dependency handoffs, enforces gates, and synthesizes deliverables.
- **L1 Domain Leads (16 agents)**: Own the technical outcomes of their respective domains.
- **Cross-Domain Critics & Governors**:
  - `code-reviewer`: Dedicated peer reviewer auditing coding standards, exception safety, and Gate G4 Code Quality.
  - `technical-critic`: Red-teams designs, challenges assumptions, uncovers hidden coupling and failure modes.
  - `independent-verifier`: Validates deliverables against acceptance criteria before gate transitions.
  - `change-impact-analyzer`: Computes blast radius across services, schemas, and dependencies.
  - `traceability-manager`: Enforces the requirements-to-production artifact chain.
  - `risk-manager`: Maintains the technical and operational risk register.
  - `documentation-governor`: Detects documentation drift and synchronizes specs with code.
  - `engineering-coordinator`: Resolves blocking cross-team dependencies.
- **L2 / L3 Focused Specialists**: Focused execution workers (`backend-engineer`, `frontend-engineer`, `database-architect`, `unit-test-engineer`, `threat-modeler`, `incident-responder`).

---

## 4. Quality Gate Lifecycle (G0 to G11)

All changes traverse enforceable quality gates:

```
[G0: Business Approval]
       │
[G1: Requirements Approval] ────> [G2: Architecture Approval] ────> [G3: Implementation Readiness]
                                                                                │
[G6: Security Quality] <──── [G5: Functional Quality] <──── [G4: Code Quality Review]
       │
[G7: Performance Budget] ────> [G8: Release Readiness] ────> [G9: Production Deployment]
                                                                                │
[G11: Closure & Lessons] <──── [G10: Operational Acceptance & Telemetry] <──────┘
```

Automated gate validation is executed via `python scripts/gate_validator.py --gate <Gx> --task <TASK_ID>`.

---

## 5. Directory Conventions

- `.agents/agents/`: Agent personas and execution boundary definitions.
- `.agents/rules/`: Modular engineering rules and constraints.
- `.agents/skills/`: Multi-step operational skills and workflow runbooks.
- `docs/`: Central repository documentation and deliverables (`adr/`, `requirements/`, etc.).
- `docs/templates/`: Standardized templates for PRDs, ADRs, Threat Models, and Test Plans.
- `governance/`: Gate definitions, schemas, and traceability ledgers.
- `scripts/`: Production automation tools (gate validator, traceability CLI, security scanning, bootstrap).
- `src/`: Application source code.
- `tests/`: Automated unit, integration, contract, and E2E test suites.

---

## 6. Upgrades & Extension Conventions

To enable consumer repositories to upgrade the framework without losing project assets:
- **Project Space Protection**: Source code (`src/`), tests (`tests/`), project documents (`docs/`), and task ledger history (`governance/traceability_ledger.json`) are permanently preserved.
- **Custom Extension Points**:
  - Custom Agents: `.agents/agents/custom/*.md`
  - Custom Rules: `.agents/rules/custom/*.md`
  - Custom Skills: `.agents/skills/custom/*/SKILL.md`
- **Safe Upgrade Tooling**: Run `powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -Update`, `bash scripts/install.sh --update`, or `python scripts/update.py`. Automatic snapshots are saved to `.agents/.backup/` with instant rollback available.
