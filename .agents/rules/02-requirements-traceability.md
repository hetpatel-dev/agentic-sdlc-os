# Requirements Traceability Rules

Traceability connects business intent to code, tests, and operational telemetry. Unlinked work is considered unauthorized work.

## 1. Identifier Conventions
All artifacts in the system must use standardized identifiers:
- **Business Objective:** `OBJ-<NNN>` (e.g., `OBJ-001`)
- **Requirement:** `REQ-<NNN>` (e.g., `REQ-101`)
- **User Story:** `US-<NNN>` (e.g., `US-205`)
- **Architecture Decision Record:** `ADR-<NNN>` (e.g., `ADR-012`)
- **Engineering Task:** `TASK-<NNN>` (e.g., `TASK-304`)
- **Test Case:** `TEST-<NNN>` (e.g., `TEST-401`)
- **Risk Record:** `RISK-<NNN>` (e.g., `RISK-015`)
- **Incident Record:** `INC-<NNN>` (e.g., `INC-003`)

## 2. Bidirectional Traceability Chain
Every code change must satisfy:
`OBJ-XXX` -> `REQ-XXX` -> `ADR-XXX` -> `TASK-XXX` -> `[Source Commits]` -> `TEST-XXX` -> `Release`

1. **Commit Messages:** Must reference the active task ID (e.g., `feat(auth): [TASK-304] implement token validation for REQ-101`).
2. **Test Cases:** Test descriptions or docstrings must reference the verified requirement ID (`@traces REQ-101`).
3. **No Orphan Code:** Pull requests or commits containing functional logic that does not map to an approved `TASK-XXX` in `governance/traceability_ledger.json` will be rejected at Gate G4.
4. **Validation Tooling:** Use `python scripts/traceability_cli.py check` to verify bidirectional integrity before submitting for review.
