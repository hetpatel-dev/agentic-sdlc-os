---
name: system-design
description: Produces high-level and low-level system designs, component models, data contracts, and Mermaid architecture diagrams.
---

# System Design & Architecture Workflow

## Objective
Formulate the architectural design, component boundaries, domain models, interface definitions, and technology selections that satisfy approved requirements (`REQ-XXX`).

## Responsible Agents
- Lead: `solution-architect`
- Contributors: `database-architect`, `platform-engineer`, `security-lead`

## Inputs
- Approved PRD from `docs/requirements/`.
- Architecture template: `docs/templates/rfcs-template.md`.

## Execution Sequence
1. **Identify System Boundaries**: Define bounded contexts, service boundaries, and responsibility separation.
2. **Model Data & Interfaces**: Define data models and API schemas in `docs/api/`.
3. **Diagram Component Architecture**: Author architecture flowcharts and sequence diagrams in Mermaid syntax.
4. **Draft Architectural Decisions**: For any major technology choice or structural pattern, author an ADR in `docs/adr/`.
5. **Save Architecture Document**: Commit design specification to `docs/architecture/ARCH-<ID>-<name>.md`.
6. **Register Architecture**: Run `python scripts/traceability_cli.py link --task <TASK_ID> --artifact <PATH>`.

## Completion Criteria
- System context diagram, component diagram, and sequence diagrams created.
- API and data contracts defined.
- Applicable ADRs authored.
