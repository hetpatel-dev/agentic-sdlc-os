---
name: continuous-improvement
description: Tracks DORA metrics, analyzes cycle times, evaluates agent performance, and coordinates continuous engineering process optimization.
---

# Continuous Improvement & Governance Workflow

## Objective
Measure engineering performance, analyze DORA metrics, identify delivery bottlenecks, evaluate agent collaboration efficiency, and continuously improve team processes.

## Responsible Agents
- Lead: `engineering-governance-lead`
- Support: `delivery-manager`, `sre-lead`

## Inputs
- Historical task ledgers from `governance/traceability_ledger.json`.
- Git commit and release history.

## Execution Sequence
1. **Calculate DORA Metrics**:
   - Deployment Frequency (deployments per week/month)
   - Lead Time for Changes (time from task creation to production deployment)
   - Change Failure Rate (percentage of deployments causing incidents/rollbacks)
   - Mean Time to Recovery (average time to resolve incidents)
2. **Analyze Quality Gate Bottlenecks**: Measure average dwell time in each gate (G0 through G11) to locate friction points.
3. **Conduct Retrospective**: Document findings and process improvements in `docs/governance/retrospectives/`.
4. **Update Standards & Rules**: If repetitive defects occur, formulate new modular rules or update existing skills to prevent recurrence.

## Completion Criteria
- DORA metrics report generated.
- Retrospective and actionable process improvements committed.
