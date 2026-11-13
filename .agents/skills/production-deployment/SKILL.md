---
name: production-deployment
description: Executes zero-downtime production deployment, canary/blue-green rollouts, post-deployment smoke tests, and Gate G9 Production Acceptance.
---

# Production Deployment & Gate G9 Workflow

## Objective
Execute safe, automated, progressive deployments to production environments, verify deployment health via smoke tests, and achieve Gate G9 Production Acceptance.

## Responsible Agents
- Lead: `operations-lead`
- Contributor: `platform-engineer`

## Inputs
- Approved release package from Gate G8.
- Deployment environment targets and credentials.

## Execution Sequence
1. **Pre-Deployment Sanity Check**: Verify target environment connectivity, secret availability, and database migration readiness.
2. **Execute Deployment**: Trigger progressive rollout (Canary or Blue/Green).
3. **Execute Post-Deployment Smoke Tests**: Run synthetic health checks against `/healthz`, `/ready`, and critical user paths.
4. **Monitor Health Metrics**: Observe error rates, latency, and system resources for the initial soak period.
5. **Execute Gate G9 Check**:
   `python scripts/gate_validator.py --gate G9 --task <TASK_ID>`
6. **Rollback Contingency**: If smoke tests fail or error rates exceed 1%, immediately initiate rollback.

## Completion Criteria
- Production deployment successful with zero unplanned downtime.
- Smoke tests pass 100%.
- Gate G9 returns PASS.
