---
name: release-readiness
description: Validates release readiness, semantic versioning, changelog updates, rollback procedures, approvals, and Gate G8 Release Readiness.
---

# Release Readiness & Gate G8 Workflow

## Objective
Verify all prerequisites, artifacts, version bumps, changelogs, rollback procedures, and approvals required to cut an authorized release and pass Gate G8.

## Responsible Agents
- Lead: `release-manager`
- Auditor: `independent-verifier`

## Inputs
- Task ID from ledger.
- Release version target (SemVer).

## Execution Sequence
1. **Audit Preceding Gates**: Verify that G0 through G7 have all PASSED in `governance/traceability_ledger.json`.
2. **Bump SemVer Version**: Update version in `package.json`, `pyproject.toml`, or `plugin.json`.
3. **Generate CHANGELOG**: Populate `CHANGELOG.md` with categorized release notes referencing task and requirement IDs.
4. **Verify Rollback Runbook**: Ensure an explicit rollback procedure is saved in `docs/releases/REL-<ID>-rollback.md`.
5. **Acquire Release Approval**: Confirm authorization from designated release approver or human authority.
6. **Execute Gate G8 Check**:
   `python scripts/gate_validator.py --gate G8 --task <TASK_ID>`

## Completion Criteria
- Gates G0-G7 verified PASSED.
- SemVer and CHANGELOG updated.
- Rollback plan verified.
- Gate G8 returns PASS.
