# Product Requirements Document (PRD)

**Document ID:** `PRD-<ID>`
**Status:** `DRAFT` | `IN_REVIEW` | `APPROVED`
**Owner:** `requirements-engineer`
**Traces Objective:** `OBJ-<ID>`
**Last Updated:** `YYYY-MM-DD`

---

## 1. Executive Summary & Problem Framing
- **Background:** Brief context explaining the business driver.
- **Problem Statement:** What pain point or capability gap are we resolving?
- **Target Audience / Personas:** Who will use or benefit from this feature?

---

## 2. Goals & Success Metrics (KPIs)
- **Primary Goal:**
- **Success Metrics:**
  - Metric 1: e.g., Response latency reduction by 30%
  - Metric 2: e.g., 99.9% uptime for transaction processing

---

## 3. Scope Boundaries
- **In-Scope:**
  - Explicit capability 1
  - Explicit capability 2
- **Out-of-Scope (Non-Goals):**
  - Explicit non-goal 1

---

## 4. Functional Requirements

### `REQ-101`: [Requirement Title]
- **Description:** Clear statement of functional behavior.
- **Traces:** `US-201`
- **Inputs & Triggers:**
- **Validation Rules:**
- **State Changes / Side Effects:**
- **Output / Responses:**
- **Acceptance Criteria:**
  - `GIVEN` [initial system state]
  - `WHEN` [user or system action occurs]
  - `THEN` [expected observable outcome]

---

## 5. Non-Functional Requirements (NFRs)
- **Performance:** p95 latency < 200ms, throughput > 500 RPS.
- **Security:** Least privilege IAM, TLS 1.3, input sanitization.
- **Availability:** 99.95% availability during business hours.
- **Observability:** RED metrics, structured JSON logs, trace propagation.

---

## 6. Assumptions & Dependencies
- **Assumptions:**
- **Upstream / Downstream Dependencies:**
