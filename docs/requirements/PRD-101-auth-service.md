# Product Requirements Document (PRD): Authentication Service

**Document ID:** `PRD-101`
**Status:** `APPROVED`
**Owner:** `requirements-engineer`
**Traces Objective:** `OBJ-001`
**Target Gate:** Gate G1 Requirements Approval
**Date:** `2026-11-13`

---

## 1. Functional Requirements

### `REQ-101`: User Credential Authentication & Token Minting
- **Description:** Given valid user credentials, the service must verify the password hash and issue a signed session token.
- **Inputs:** `username` (string, 3-50 chars), `password` (string, >= 8 chars).
- **Validation Rules:** Reject missing or malformed inputs with HTTP 400.
- **Acceptance Criteria:**
  - `GIVEN` a registered user with valid password hash
  - `WHEN` a login request is made with correct credentials
  - `THEN` return HTTP 200 with a cryptographically signed token and expiration timestamp.
  - `GIVEN` an invalid password or non-existent username
  - `WHEN` a login request is made
  - `THEN` return HTTP 401 Unauthorized without leaking whether the username exists.

### `REQ-102`: Session Token Verification
- **Description:** Given an active token, the service must verify cryptographic integrity and expiration status.
- **Acceptance Criteria:**
  - `GIVEN` an unexpired token with valid signature
  - `WHEN` verified by downstream services
  - `THEN` return user identity claims.
  - `GIVEN` an expired or tampered token
  - `WHEN` verification is attempted
  - `THEN` reject token with HTTP 401.

---

## 2. Non-Functional Requirements (NFRs)
- **NFR-01 (Latency):** Token verification p99 < 5ms.
- **NFR-02 (Security):** Signatures using HMAC-SHA256 with minimum 256-bit secret key.
- **NFR-03 (Availability):** Stateless token verification requiring zero external network hops.
