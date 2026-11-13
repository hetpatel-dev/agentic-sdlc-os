# Release Readiness Checklist

**Release ID:** `REL-<ID>`
**Target Version:** `vX.Y.Z`
**Release Lead:** `release-manager`
**Target Gate:** Gate G8 Release Readiness
**Date:** `YYYY-MM-DD`

---

## 1. Quality Gate Verification
- [ ] Gate G0 (Business Approval): PASSED
- [ ] Gate G1 (Requirements Approval): PASSED
- [ ] Gate G2 (Architecture Approval): PASSED
- [ ] Gate G3 (Implementation Readiness): PASSED
- [ ] Gate G4 (Code Quality Review): PASSED
- [ ] Gate G5 (Functional Quality): PASSED
- [ ] Gate G6 (Security Quality): PASSED
- [ ] Gate G7 (Performance Quality): PASSED

---

## 2. Release Artifacts
- [ ] Version tag bumped in manifest files.
- [ ] `CHANGELOG.md` updated with categorized release notes.
- [ ] Rollback runbook verified.
- [ ] Release package built and digest recorded.

---

## 3. Rollback Runbook Summary
- **Trigger Conditions:** Error rate > 1%, smoke test failure, latency spike.
- **Rollback Command / Step:** e.g., `git checkout vX.Y.(Z-1)` or traffic switch command.
- **Data Reversion:** e.g., Run database rollback script `migrations/down`.
