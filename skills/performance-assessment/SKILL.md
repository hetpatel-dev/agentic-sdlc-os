---
name: performance-assessment
description: Measures latency budgets (p95/p99), resource utilization, concurrency profiles, resilience under load, and validates Gate G7 Performance Quality.
---

# Performance Assessment & Gate G7 Workflow

## Objective
Benchmark system performance against latency budgets and resource thresholds under anticipated traffic loads to ensure reliability and validate Gate G7.

## Responsible Agents
- Lead: `performance-lead`
- Contributor: `solution-architect`

## Inputs
- Service endpoints and performance budgets from PRD/NFRs.
- Task ID from ledger.

## Execution Sequence
1. **Define Load Scenarios**: Establish baseline, peak, and stress scenarios.
2. **Execute Benchmark / Load Test**: Run performance test harness measuring latency percentiles (p50, p90, p95, p99) and requests per second.
3. **Verify Resource Footprint**: Inspect memory, CPU, and connection pool utilization during sustained execution.
4. **Compare Against SLA**: Ensure p95 < 200ms and p99 < 500ms (or documented service budget).
5. **Execute Gate G7 Check**:
   `python scripts/gate_validator.py --gate G7 --task <TASK_ID>`

## Completion Criteria
- Latency percentiles satisfy performance budgets.
- No memory leaks detected.
- Gate G7 returns PASS.
