---
name: security-assessment
description: Conducts comprehensive security audits, STRIDE threat modeling, secret scanning, dependency CVE scanning, and Gate G6 Security Quality.
---

# Security Assessment & Gate G6 Workflow

## Objective
Identify security vulnerabilities, threat vectors, plaintext secrets, and dependency CVEs before release, achieving Gate G6 Security Quality.

## Responsible Agents
- Lead: `security-lead`
- Worker: `threat-modeler`

## Inputs
- Architecture specs, source code, and dependency manifests.
- Task ID from ledger.

## Execution Sequence
1. **Threat Model Review**: Validate STRIDE analysis for trust boundaries and external inputs.
2. **Execute Secret Scanner**:
   `python scripts/security_check.py --stage audit`
   Verify zero hardcoded API keys, passwords, or tokens.
3. **Execute SAST / Static Analysis**: Scan source code for SQL injection, XSS, insecure deserialization, or weak cryptography.
4. **Execute SCA / Dependency Audit**: Check third-party dependencies for known CVEs.
5. **Remediate Open Vulnerabilities**: Block if any HIGH or CRITICAL findings exist.
6. **Execute Gate G6 Check**:
   `python scripts/gate_validator.py --gate G6 --task <TASK_ID>`

## Completion Criteria
- Zero detected secrets.
- Zero open HIGH/CRITICAL vulnerabilities.
- Gate G6 returns PASS.
