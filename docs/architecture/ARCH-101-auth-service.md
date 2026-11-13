# Architecture Specification: Authentication Service

**Spec ID:** `ARCH-101`
**Title:** Stateless Token-Based Authentication Architecture
**Author:** `solution-architect`
**Reviewer:** `technical-critic`
**Status:** `APPROVED`
**Traces:** `REQ-101`, `REQ-102`

---

## 1. System Architecture Diagram

```mermaid
sequenceDiagram
    autonumber
    Client->>AuthService: POST /auth/login {username, password}
    AuthService->>UserStore: Lookup User & Password Hash
    UserStore-->>AuthService: User Record
    AuthService->>AuthService: Verify Cryptographic Hash
    AuthService->>AuthService: Sign Token (HMAC-SHA256)
    AuthService-->>Client: 200 OK {token, expires_at}
    Client->>ProtectedAPI: GET /resource with Bearer Token
    ProtectedAPI->>ProtectedAPI: Verify Signature & Expiry
    ProtectedAPI-->>Client: 200 OK Resource Data
```

---

## 2. Component Design & Contracts
- **Token Format:** Base64URL header + payload + HMAC-SHA256 signature.
- **Payload Claims:**
  - `sub`: User identifier
  - `exp`: Expiration timestamp (UTC epoch seconds)
  - `iat`: Issued at timestamp
  - `scope`: Granted permission roles
