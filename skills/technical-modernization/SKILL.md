---
name: technical-modernization
description: Coordinates technical debt assessment, legacy code refactoring, dependency modernizations, and architecture evolution.
---

# Technical Modernization & Refactoring Workflow

## Objective
Safely modernize legacy components, upgrade major runtime versions, reduce technical debt, and refactor code without introducing behavioral regressions.

## Responsible Agents
- Lead: `maintenance-lead`
- Workers: `backend-engineer`, `unit-test-engineer`

## Inputs
- Debt item from `docs/governance/technical-debt.md`.
- Existing test suites and benchmarks.

## Execution Sequence
1. **Establish Baseline Tests**: Verify comprehensive automated test coverage exists before modifying any legacy logic. If coverage is inadequate, author characterization tests first.
2. **Execute Incremental Refactoring**: Apply the Strangler Fig or Branch by Abstraction pattern. Never attempt monolithic rewrites.
3. **Execute Continuous Verification**: Run test suites after each incremental change to confirm zero regression.
4. **Benchmark Performance**: Verify that refactoring did not introduce latency or throughput regressions.
5. **Update Technical Debt Register**: Mark the debt item as resolved in `docs/governance/technical-debt.md`.

## Completion Criteria
- Code refactored to modern standards.
- 100% of existing tests pass without regressions.
- Technical debt ledger updated.
