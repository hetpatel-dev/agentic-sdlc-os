---
name: feature-implementation
description: Coordinates feature implementation from approved requirements and architecture through code changes, testing, peer review, and verification.
---

# Feature Implementation Workflow

## Objective
Implement a software feature from approved requirements and architectural contracts through clean coding, automated testing, independent review, and gate verification.

## Responsible Agents
- Lead: `engineering-lead`
- Workers: `backend-engineer`, `frontend-engineer`, `database-architect`, `unit-test-engineer`
- Reviewer: `code-reviewer` / `independent-verifier`

## Inputs
- Approved requirement (`REQ-XXX`) and architecture plan (`ARCH-XXX`).
- Task ID from `governance/traceability_ledger.json`.

## Execution Sequence
1. **Implementation Plan & Gate G3 Check**:
   - Inspect existing codebase.
   - List files to Create, Modify, or Delete.
   - Run `python scripts/gate_validator.py --gate G3 --task <TASK_ID>`.
2. **Execute Implementation**:
   - For backend: Delegate to `backend-engineer`.
   - For frontend: Delegate to `frontend-engineer`.
   - For database: Delegate to `database-architect`.
   - Use isolated worktrees/branches when concurrent workers touch overlapping areas.
3. **Automated Testing**:
   - Author unit and integration tests covering the new functionality.
   - Run test suite: verify 100% pass rate.
4. **Lint & Static Analysis**:
   - Execute project linters and formatters.
5. **Code Review & Gate G4 Check**:
   - Request review from `code-reviewer`.
   - Address any reviewer feedback.
   - Run `python scripts/gate_validator.py --gate G4 --task <TASK_ID>`.
6. **Functional Quality & Gate G5 Check**:
   - Request verification from `qa-lead`.
   - Run `python scripts/gate_validator.py --gate G5 --task <TASK_ID>`.

## Completion Criteria
- Code implemented and adhering to standards.
- Tests passing with terminal evidence.
- Gates G3, G4, and G5 pass validation.
