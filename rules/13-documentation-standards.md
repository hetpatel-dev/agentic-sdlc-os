# Documentation Standards & Spec Synchronization Rules

This rule enforces accuracy, synchronicity, structure, and readability across all technical documentation.

## 1. Documentation as Code
- Documentation lives in the repository under `docs/` and is version-controlled alongside source code.
- Pull requests modifying functional logic, APIs, or database schemas must include corresponding documentation updates in the same PR.

## 2. Standard Document Hierarchy
- `docs/product/`: Product vision, market research, business cases.
- `docs/requirements/`: Approved PRDs, SRS documents, user story specifications.
- `docs/architecture/`: System context, component diagrams, domain models.
- `docs/adr/`: Architecture Decision Records.
- `docs/api/`: OpenAPI specs, contract definitions, and interaction flows.
- `docs/database/`: ER diagrams, schema definitions, and migration catalogs.
- `docs/security/`: Threat models, compliance matrices, security reviews.
- `docs/testing/`: Test plans, test reports, and verification evidence.
- `docs/operations/`: Runbooks, deployment procedures, incident postmortems.
- `docs/releases/`: Release checklists, changelogs, rollback procedures.
- `docs/governance/`: Engineering standards, audit reports, gate records.

## 3. Strict Accuracy & Reference Integrity
- Documents must not cite nonexistent endpoints, database tables, or functions.
- When describing current architecture, verify against source code.
- When detailing future state or proposed changes, clearly label sections as `PROPOSED`.
- Broken links or unmaintained specs will be flagged by `documentation-governor`.
