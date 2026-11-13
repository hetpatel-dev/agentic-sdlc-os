---
name: requirements-validation
description: Validates PRD/SRS requirements for completeness, testability, consistency, and validates Gate G1 Requirements Approval.
---

# Requirements Validation & Gate G1 Workflow

## Objective
Rigorously stress-test a generated PRD or SRS, ensuring requirements are complete, non-contradictory, testable, and compliant with Gate G1 standards.

## Responsible Agents
- Lead: `requirements-engineer`
- Auditor: `independent-verifier`
- Critic: `technical-critic`

## Inputs
- PRD document path in `docs/requirements/`.
- Task ID from `governance/traceability_ledger.json`.

## Execution Sequence
1. **Audit Testability**: Verify each `REQ-XXX` has at least one executable Given/When/Then acceptance criterion.
2. **Audit Edge Cases**: Check boundary limits (0, 1, max, negative, null, timeout).
3. **Audit Conflicts**: Ensure no requirement contradicts existing system invariants or another requirement.
4. **Independent Review**: `independent-verifier` inspects the document and confirms absence of ambiguity.
5. **Execute Gate G1 Check**:
   `python scripts/gate_validator.py --gate G1 --task <TASK_ID>`

## Completion Criteria
- Gate G1 returns PASS.
- Task marked as ready for architecture phase.
