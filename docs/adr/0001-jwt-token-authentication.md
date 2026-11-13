# ADR 0001: Stateless JWT Token Authentication

**ADR ID:** `ADR-0001`
**Status:** `ACCEPTED`
**Deciders:** `solution-architect`, `technical-critic`, `security-lead`
**Date:** `2026-11-13`
**Traces:** `REQ-101`, `REQ-102`

---

## 1. Context and Problem Statement
Microservices need to verify incoming client requests without performing a database lookup on every single API invocation, which would introduce latency bottlenecks and database lock contention.

---

## 2. Decision Drivers
- High throughput requirement (> 10,000 RPS).
- Verification latency under 2ms.
- Decentralized, stateless service verification.

---

## 3. Considered Options
1. **Server-side Session DB (Redis):** Requires network round-trip for every request.
2. **Stateless Signed Tokens (JWT):** Zero database lookups for verification; self-contained claims.
3. **mTLS Client Certificates:** Complex key management for public mobile/web clients.

---

## 4. Decision Outcome
**Chosen Option:** Option 2 (Stateless Signed Tokens with HMAC-SHA256).

### Positive Consequences
- Zero database load during token verification.
- Verification is pure in-memory cryptographic computation.

### Negative Consequences
- Tokens cannot be revoked immediately before expiry without an in-memory blocklist. Mitigation: Keep token lifetime short (15 minutes).
