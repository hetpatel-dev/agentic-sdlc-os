# Architecture Standards & ADR Rules

This rule governs architectural integrity, boundary separation, technology choices, and decision records.

## 1. Architecture Decision Records (ADRs)
- Any material architectural change (introducing a new library, altering persistence schemas, creating an external integration, modifying concurrency or security models) requires an ADR.
- ADRs must be committed under `docs/adr/` using the format `docs/adr/NNNN-<title>.md`.
- ADR status values: `PROPOSED`, `ACCEPTED`, `SUPERSEDED`, `REJECTED`.
- An ADR is only marked `ACCEPTED` once reviewed and approved by `solution-architect` and `technical-critic`.

## 2. Modularity and Boundary Enforcement
- **Domain-Driven Boundaries:** Components must maintain high cohesion and loose coupling. Modules must interact only through well-defined public interfaces or contracts.
- **Dependency Direction:** Domain core logic must not depend on external infrastructure adapters (databases, third-party network clients). Use dependency injection or interface abstraction.
- **Zero Circular Dependencies:** Circular imports between packages or modules are forbidden.

## 3. Resilience and Failure Modes
- All network and distributed calls must specify:
  1. Explicit timeout limits (connection and read).
  2. Circuit breaking or bounded exponential backoff retry strategies.
  3. Graceful degradation or fallback behavior when dependencies fail.
