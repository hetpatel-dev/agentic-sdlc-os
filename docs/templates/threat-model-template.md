# Threat Model Specification

**Model ID:** `THREAT-<ID>`
**Target Component:** [Service or Feature Name]
**Author:** `security-lead` / `threat-modeler`
**Status:** `DRAFT` | `VERIFIED`
**Traces:** `ARCH-<ID>`

---

## 1. System Overview & Data Flow Diagram
Description of components, ingress points, egress points, and trust boundaries.

---

## 2. STRIDE Threat Analysis

| Threat ID | STRIDE Category | Threat Description | Likelihood | Impact | Severity | Mitigation Strategy | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T-01` | **S**poofing | Attacker forges auth token | LOW | CRITICAL | HIGH | Cryptographic signing & short expiry | MITIGATED |
| `T-02` | **T**ampering | Man-in-the-middle payload edit | LOW | HIGH | HIGH | Strict TLS 1.3 encryption | MITIGATED |
| `T-03` | **R**epudiation | User denies initiating transaction| LOW | MEDIUM | MEDIUM | Immutable audit log with user ID | MITIGATED |
| `T-04` | **I**nfo Disclosure| Sensitive data exposed in logs | MEDIUM | HIGH | HIGH | Masking & automated secret scan | MITIGATED |
| `T-05` | **D**enial of Service| Resource exhaustion via payload | MEDIUM | HIGH | HIGH | Rate limiting & body size caps | MITIGATED |
| `T-06` | **E**levation | Privilege escalation via IDOR | LOW | CRITICAL | HIGH | Object-level authorization checks | MITIGATED |

---

## 3. Residual Risks & Action Items
- Item 1: Linked to `TASK-XXX`
