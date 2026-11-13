---
name: api-development
description: Governs API design, schema validation, backwards compatibility checks, mocking, and API documentation generation.
---

# API Development Workflow

## Objective
Design, implement, and document robust, versioned, backward-compatible APIs (REST/gRPC/GraphQL) with machine-readable specifications and contract tests.

## Responsible Agents
- Lead: `solution-architect` / `engineering-lead`
- Workers: `backend-engineer`, `unit-test-engineer`

## Inputs
- Requirement specifications from PRD.
- Existing API schemas in `docs/api/`.

## Execution Sequence
1. **Contract-First Design**: Draft the OpenAPI 3.1 specification or Protobuf `.proto` in `docs/api/`.
2. **Backward Compatibility Check**: If updating an existing endpoint, run a compatibility check to ensure no fields were removed or changed in a breaking manner.
3. **Endpoint Implementation**: Delegate implementation to `backend-engineer`. Ensure input validation is strictly enforced against the schema.
4. **Contract Testing**: Write tests verifying schema compliance, status codes, and error response formats.
5. **Update API Documentation**: Verify docs accurately reflect request parameters and sample payloads.

## Completion Criteria
- Machine-readable specification saved in `docs/api/`.
- Zero backward compatibility violations.
- Contract tests passing with real terminal execution output.
