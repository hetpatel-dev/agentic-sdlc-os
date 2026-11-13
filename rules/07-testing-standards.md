# Testing Standards & Verification Rules

This rule defines testing rigor, test pyramid distribution, code coverage criteria, and execution verification.

## 1. Test Pyramid Distribution
Testing must be structured hierarchically:
1. **Unit Tests (Base):** Fast, isolated tests targeting pure business logic and individual functions without network or database dependencies.
2. **Integration Tests (Middle):** Verify interactions between services, database queries, and third-party adapter boundaries using lightweight test containers or mocks.
3. **Contract Tests (Boundary):** Verify that API producers and consumers satisfy OpenAPI / Pact contracts.
4. **End-to-End / Regression Tests (Apex):** Critical user path smoke tests validating end-to-end workflows in staging environments.

## 2. Coverage & Quality Gates
- All newly added functional code must achieve at least 85% branch coverage.
- Code coverage is a prerequisite for passing Gate G5 (`Functional Quality`).
- Tests must assert specific outcomes, error messages, and edge cases (boundary values, nulls, invalid inputs, timeouts).

## 3. Strict Execution Verification
- Agents must never report that tests passed unless the test runner was executed via terminal command during the current session.
- Test runner output logs must be captured and referenced in the gate validation artifact.
- Flaky tests must be quarantined, tagged, and resolved immediately; silent ignores are prohibited.
