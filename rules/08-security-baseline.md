# Security Baseline & Vulnerability Governance

This rule defines mandatory application security standards, secret protection, vulnerability remediation, and access control.

## 1. Secret Management & Credential Zero
- Zero plaintext secrets in code, configuration files, pull requests, or git history.
- Use environment variables, secret managers (e.g., Vault, AWS Secrets Manager, Google Secret Manager), or encrypted vaults.
- The repository must include automated pre-commit / pre-tool secret scanning (`scripts/security_check.py`).
- If a secret is accidentally committed, it is considered compromised immediately and must be revoked and rotated.

## 2. Threat Modeling & OWASP Top 10
- All user input must be sanitized and validated at system boundaries.
- Database access must use parameterized queries or trusted ORM mappings to prevent SQL Injection.
- Output destined for browsers or web clients must be contextually encoded to prevent Cross-Site Scripting (XSS).
- Authentication tokens (JWTs, session cookies) must enforce cryptographic signing, expiry times, and secure flags (`HttpOnly`, `SameSite=Strict`, `Secure`).

## 3. Dependency Scanning & Software Bill of Materials (SBOM)
- All third-party dependencies must be scanned for known CVEs.
- Zero open HIGH or CRITICAL CVEs are permitted in production releases (enforced at Gate G6).
- Dependencies must be locked with exact checksums (`package-lock.json`, `poetry.lock`, `go.sum`).
