# API Contract & Compatibility Rules

This rule enforces strict backward compatibility, contract specifications, and versioning protocols for all internal and external APIs.

## 1. Contract Specifications
- Every public API (REST, GraphQL, gRPC, WebSocket) must have a formal machine-readable specification stored in `docs/api/` (OpenAPI 3.1 YAML/JSON, Protobuf `.proto`, or GraphQL schema).
- New endpoints or mutations must include example request/response payloads and documented HTTP status codes / error shapes.

## 2. Backward Compatibility
- Established public API contracts are immutable for existing consumers.
- Breaking changes (removing a field, renaming an endpoint, changing a type, altering error codes) are strictly forbidden within the same major version.
- Breaking changes require:
  1. A formal ADR approved by `solution-architect`.
  2. A new versioned endpoint prefix (e.g., `/api/v2/`).
  3. A deprecation notice and transition window for existing clients.

## 3. Idempotency & Validation
- Mutating endpoints (POST, PUT, PATCH, DELETE) handling financial transactions, state machine transitions, or order processing must support idempotency keys.
- All request parameters, headers, and payloads must be validated against schema schemas before hitting business logic.
