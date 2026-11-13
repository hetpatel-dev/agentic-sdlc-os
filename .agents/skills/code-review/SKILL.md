---
name: code-review
description: Performs rigorous independent code review, verifying coding standards, error handling, security, test coverage, and Gate G4 Code Quality.
---

# Code Review & Gate G4 Workflow

## Objective
Provide independent, authoritative code review of proposed changes to ensure compliance with coding standards, error handling best practices, and Gate G4 criteria.

## Responsible Agents
- Lead: `code-reviewer` / `engineering-lead`
- Auditor: `independent-verifier`

## Inputs
- Git diff or list of modified files.
- Task ID and linked requirement ID.

## Execution Sequence
1. **Scope Inspection**: Check git diff to ensure changes are strictly bounded to the assigned task. Flag unrelated file modifications.
2. **Quality & Style Checks**:
   - Verify proper naming and single responsibility principles.
   - Verify absence of unhandled exceptions or empty catch blocks.
   - Verify type annotations on public interfaces.
3. **Traceability Verification**:
   - Check that commits and docstrings link to `TASK-XXX` and `REQ-XXX`.
4. **Run Static Analysis**:
   - Execute linters and formatters.
5. **Issue Review Findings**:
   - Output structured review comments (BLOCKER, MAJOR, MINOR).
6. **Execute Gate G4 Check**:
   `python scripts/gate_validator.py --gate G4 --task <TASK_ID>`

## Completion Criteria
- Zero open BLOCKER or MAJOR review comments.
- Linters pass cleanly.
- Gate G4 returns PASS.
