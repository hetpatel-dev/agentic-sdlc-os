# SDLC Lifecycle Gates & Governance Rules

This rule enforces gate validation requirements for all changes moving through the lifecycle.

## 1. Quality Gate Hierarchy
Every deliverable advances through formal Quality Gates (G0 through G11). Gates must be validated in sequence or explicitly waived by an authorized human administrator with an audit rationale.

| Gate | Name | Required Evidence | Responsible Sign-Off |
| :--- | :--- | :--- | :--- |
| **G0** | Business Approval | Problem statement, ROI/value proposition, scope boundary | `product-strategist` |
| **G1** | Requirements Approval | Signed PRD/SRS with testable acceptance criteria (`REQ-XXX`) | `requirements-engineer` |
| **G2** | Architecture Approval | ADR, system context diagram, threat model review | `solution-architect` |
| **G3** | Implementation Readiness| Technical task breakdown, API specs, schema definitions | `engineering-lead` |
| **G4** | Code Quality Review | Independent review passed, linter clean, zero unhandled errors | `code-reviewer` |
| **G5** | Functional Quality | Unit & integration tests executed with 100% pass rate | `qa-lead` |
| **G6** | Security Quality | Zero HIGH/CRITICAL vulnerabilities, SAST clean, secret scan clean | `security-lead` |
| **G7** | Performance Quality | Latency/throughput budget verified, no regressions vs baseline | `performance-lead` |
| **G8** | Release Readiness | SemVer bumped, CHANGELOG updated, tested rollback procedure | `release-manager` |
| **G9** | Production Acceptance| Deployment executed cleanly, post-deploy smoke tests passed | `operations-lead` |
| **G10**| Operational Acceptance| Monitoring active, alerts configured, dashboards live, runbook verified| `sre-lead` |
| **G11**| Closure & Governance | Traceability chain complete, retrospective recorded | `engineering-governance-lead` |

## 2. Gate Advancement Rules
- **No Advancement on Failure:** If any required check fails, the task returns to the assigned lead agent for remediation.
- **Automated Validation:** All automated gate checks must be verified via `python scripts/gate_validator.py --gate <Gx> --task <TASK_ID>`.
- **Audit Logging:** Every gate transition is recorded in `governance/traceability_ledger.json` with timestamp, agent name, and artifact checksums.

## 3. Framework Upgrade Governance
- **Ledger Invariants:** Upgrades must never delete or overwrite existing tasks, requirements, objectives, or gate approval records in `governance/traceability_ledger.json`.
- **Pre-Update Backups:** Upgrades must execute a snapshot backup before making modifications.
- **Rollback Readiness:** If post-update gate validation or framework tests fail, the updater must provide an instant rollback mechanism.
