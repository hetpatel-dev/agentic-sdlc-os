# Release Governance & Change Management Rules

This rule enforces change control, semantic versioning, release artifacts, deployment approvals, and rollback readiness.

## 1. Semantic Versioning & Changelogs
- Releases follow Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`):
  - `MAJOR`: Incompatible API or structural changes.
  - `MINOR`: Backwards-compatible new functionality.
  - `PATCH`: Backwards-compatible bug fixes.
- Every release must generate an updated `CHANGELOG.md` categorizing:
  - Features Added (`Added`)
  - Fixes (`Fixed`)
  - Deprecations (`Deprecated`)
  - Removals (`Removed`)
  - Security Fixes (`Security`)

## 2. Release Readiness Gate (G8)
Before a release tag is cut or deployed to production:
1. All prior gates G0 through G7 must have `PASSED` status in `governance/traceability_ledger.json`.
2. A tested, documented rollback plan must exist in `docs/releases/`.
3. An authorized human release approver or designated release manager must sign off.

## 3. Deployment & Rollback Strategy
- Production deployments must utilize progressive rollout strategies: Canary releases or Blue/Green environments.
- Automated rollback must trigger if:
  1. Error rates increase by more than 1% post-deployment.
  2. Latency p99 exceeds the SLO threshold.
  3. Health check endpoints fail for 3 consecutive probes.
