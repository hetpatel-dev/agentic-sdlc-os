---
name: product-discovery
description: Conducts product discovery, market analysis, stakeholder alignment, and prepares business case for Gate G0 Business Approval.
---

# Product Discovery & Business Strategy Workflow

## Objective
Transform an ambiguous business concept or market opportunity into a validated problem statement, persona profile, value hypothesis, and Gate G0 Business Approval brief.

## Responsible Agents
- Lead: `product-strategist`
- Support: `delivery-manager`, `solution-architect`

## Inputs
- Initial user request or business opportunity statement.
- Market research and competitor references (if available).
- Organizational constraints and targets.

## Execution Sequence
1. **Analyze Problem Space**: Identify target users, pain points, and current workarounds.
2. **Conduct Market / Technical Scan**: Search for established patterns or solutions using `search_web`.
3. **Define Scope Boundary**: Explicitly document what is IN-SCOPE and what is strictly OUT-OF-SCOPE.
4. **Define Success Metrics**: Formulate quantitative KPIs (e.g., conversion, latency reduction, user adoption).
5. **Draft Brief**: Save document into `docs/product/PROD-<ID>-discovery.md`.
6. **Register Task**: Run `python scripts/traceability_cli.py create-task --domain strategy --title "Product Discovery: <Title>" --obj OBJ-<ID>`.
7. **Submit for Gate G0**: Run `python scripts/gate_validator.py --gate G0 --task <TASK_ID>`.

## Completion Criteria
- Business brief saved in `docs/product/`.
- Gate G0 passes validation.
