---
name: prd-generation
description: Generates formal Product Requirement Documents (PRDs), numbered functional requirements (REQ-XXX), and Given/When/Then acceptance criteria.
---

# PRD Generation Workflow

## Objective
Author a comprehensive, unambiguous Product Requirements Document (PRD) from an approved business brief (Gate G0).

## Responsible Agents
- Lead: `requirements-engineer`
- Contributors: `product-strategist`, `ux-design-lead`

## Inputs
- Approved Gate G0 business brief from `docs/product/`.
- PRD Template: `docs/templates/prd-template.md`.

## Execution Sequence
1. **Load Template**: Copy structure from `docs/templates/prd-template.md`.
2. **Decompose Functional Requirements**: Write individual requirements (`REQ-101`, `REQ-102`), detailing trigger, inputs, validation rules, state mutations, and outputs.
3. **Formulate Acceptance Criteria**: Format every requirement with concrete `Given [initial state] When [action occurs] Then [expected outcome]` criteria.
4. **Define Non-Functional Requirements**: Quantify latency budgets, uptime SLOs, security, and concurrency expectations.
5. **Save PRD**: Write output to `docs/requirements/PRD-<ID>-<name>.md`.
6. **Link Artifact**: Register PRD in `governance/traceability_ledger.json` via `python scripts/traceability_cli.py link --task <TASK_ID> --artifact <PATH>`.

## Completion Criteria
- PRD created with numbered `REQ-XXX` requirements and testable acceptance criteria.
- No unstated assumptions or vague adjectives ("fast", "intuitive") without metrics.
