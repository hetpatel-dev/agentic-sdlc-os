---
name: incident-response
description: Coordinates incident triage, impact assessment, rapid containment, service recovery, root cause analysis, and blameless postmortems.
---

# Production Incident Response Workflow

## Objective
Provide fast, structured, blameless response to production incidents, minimizing MTTR and preventing recurrence.

## Responsible Agents
- Incident Commander: `sre-lead`
- Execution Worker: `incident-responder`

## Inputs
- Alert trigger or incident notification.
- Affected service telemetry and logs.

## Execution Sequence
1. **Declare Incident & Assess Severity**:
   - `SEV-1`: Critical outage affecting revenue/core functionality.
   - `SEV-2`: Degraded functionality with available workaround.
   - `SEV-3`: Minor defect or non-critical alert.
2. **Contain Impact**: Prioritize service restoration over deep debugging (e.g., restart, traffic rollback, fallback switch).
3. **Log Timeline**: Maintain a real-time event log in `docs/operations/incidents/INC-<ID>-timeline.md`.
4. **Isolate Root Cause**: Inspect logs, traces, and recent changes using `scripts/gate_validator.py` and commit history.
5. **Draft Blameless Postmortem**: Use `docs/templates/incident-postmortem-template.md` to document timeline, root cause, what went well, what went wrong, and corrective action tasks (`TASK-XXX`).

## Completion Criteria
- Service restored and validated.
- Blameless postmortem published in `docs/operations/postmortems/`.
- Remediation tasks created in `governance/traceability_ledger.json`.
