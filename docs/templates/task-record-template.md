# Task Record Template

```yaml
task:
  id: TASK-101
  title: Implement User Authentication Service
  domain: development
  status: IN_PROGRESS
  current_gate: G3
  created_at: "2026-11-13T07:46:00Z"
  assigned_agent: backend-engineer

  traceability:
    objective_id: OBJ-001
    requirement_ids:
      - REQ-101
      - REQ-102
    adr_ids:
      - ADR-001
    commits:
      - "a1b2c3d"
    test_case_ids:
      - TEST-101
      - TEST-102
    release_version: "v1.0.0"

  artifacts:
    - "docs/requirements/PRD-001-auth.md"
    - "docs/architecture/ARCH-001-auth.md"
    - "src/auth/service.py"
    - "tests/test_auth.py"

  validation:
    lint: PASSED
    unit_tests: PASSED
    security_scan: PASSED
    coverage_percent: 92.5

  gate_history:
    - gate: G0
      status: PASSED
      timestamp: "2026-11-13T08:00:00Z"
      verified_by: product-strategist
    - gate: G1
      status: PASSED
      timestamp: "2026-11-13T08:30:00Z"
      verified_by: requirements-engineer
    - gate: G2
      status: PASSED
      timestamp: "2026-11-13T09:00:00Z"
      verified_by: solution-architect

  risks:
    - id: RISK-001
      description: Third-party OAuth latency spike
      severity: MEDIUM
      mitigation: Implement local token cache and circuit breaker
```
