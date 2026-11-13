---
name: architecture-review
description: Conducts red-team architecture reviews, ADR validation, security/performance assessments, and Gate G2 Architecture Approval.
---

# Architecture Review & Gate G2 Workflow

## Objective
Stress-test system design, challenge architectural assumptions, assess security and scalability implications, and achieve Gate G2 Architecture Approval.

## Responsible Agents
- Lead: `solution-architect`
- Hostile Critic: `technical-critic`
- Security Auditor: `security-lead`
- Performance Auditor: `performance-lead`

## Inputs
- Architecture document in `docs/architecture/`.
- Proposed ADRs in `docs/adr/`.
- Task ID from ledger.

## Execution Sequence
1. **Red-Team Challenge**: `technical-critic` audits design for SPOFs, concurrency bottlenecks, cascading failures, and unnecessary complexity.
2. **Threat Assessment**: `security-lead` conducts preliminary threat modeling and checks trust boundary exposure.
3. **Capacity & Latency Check**: `performance-lead` evaluates if the proposed architecture can satisfy latency and throughput budgets.
4. **Resolve Findings**: `solution-architect` updates architecture document to address BLOCKER and MAJOR findings.
5. **Execute Gate G2 Check**:
   `python scripts/gate_validator.py --gate G2 --task <TASK_ID>`

## Completion Criteria
- Zero open BLOCKER findings from `technical-critic`.
- ADRs marked as ACCEPTED.
- Gate G2 passes validation.
