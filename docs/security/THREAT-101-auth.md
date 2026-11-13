# Security Threat Model: Authentication Service

**Model ID:** `THREAT-101`
**Component:** `src/auth/service.py`
**Lead:** `security-lead`
**Target Gate:** Gate G6 Security Quality
**Status:** `VERIFIED`
**Date:** `2026-11-13`

---

## 1. STRIDE Analysis & Verification

| Threat | Description | Mitigation in Code | Verification Status |
| :--- | :--- | :--- | :--- |
| **Spoofing** | Forged session token | HMAC-SHA256 signature verification with secret key | Verified in `test_verify_token_tampered_signature` |
| **Tampering** | Modified claims payload | Signature covers encoded header and payload | Verified in `test_verify_token_tampered_signature` |
| **Information Disclosure** | Timing attack on signature comparison | `hmac.compare_digest` used for constant-time comparison | Verified in source review |
| **Information Disclosure** | Plaintext credential exposure | Salted PBKDF2 with 100,000 iterations | Verified in `test_hash_and_verify_password` |
| **Denial of Service** | Infinite token replay | `exp` claim verified against current epoch seconds | Verified in `test_verify_token_expired` |
| **Elevation of Privilege** | Unauthenticated scope escalation | Signature validation prevents arbitrary claim injection | Verified in `test_verify_token_success` |

---

## 2. Automated Secret Scan
- Scanner: `scripts/security_check.py --stage audit`
- Detected Secrets: **0**
- CVEs: **0** (pure Python standard library implementation)
