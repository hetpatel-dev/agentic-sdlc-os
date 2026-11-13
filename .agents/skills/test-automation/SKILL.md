---
name: test-automation
description: Automates unit, integration, and E2E test generation, test execution, coverage auditing, and Gate G5 Functional Quality.
---

# Test Automation & Verification Workflow

## Objective
Author, execute, and verify automated test suites across unit, integration, and end-to-end layers, ensuring strict coverage and functional correctness.

## Responsible Agents
- Lead: `qa-lead`
- Workers: `unit-test-engineer`

## Inputs
- Implemented code under `src/`.
- Requirement acceptance criteria from `docs/requirements/`.
- Task ID from ledger.

## Execution Sequence
1. **Map Test Cases to Acceptance Criteria**: Create test cases tagged with requirement IDs (`@traces REQ-XXX`).
2. **Implement Unit & Integration Tests**: Author test cases exercising happy path, boundary values, invalid inputs, and error states.
3. **Execute Test Runner**: Run tests using project test runner (e.g., `pytest`, `npm test`, `go test`). Capture full output.
4. **Measure Coverage**: Verify newly introduced code meets the 85% branch coverage target.
5. **Execute Gate G5 Check**:
   `python scripts/gate_validator.py --gate G5 --task <TASK_ID>`

## Completion Criteria
- 100% of test cases pass.
- Coverage threshold satisfied.
- Terminal execution logs recorded.
- Gate G5 returns PASS.
