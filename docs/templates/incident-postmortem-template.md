# Incident Postmortem (Blameless)

**Incident ID:** `INC-<ID>`
**Severity:** `SEV-1` | `SEV-2` | `SEV-3`
**Commander:** `sre-lead`
**Date of Incident:** `YYYY-MM-DD`
**Duration:** `X hours Y minutes`
**Services Affected:** `[Service names]`

---

## 1. Executive Summary
Brief summary of what happened, customer impact (e.g., number of failed requests or minutes of degraded latency), and how the issue was mitigated.

---

## 2. Customer Impact
- **Peak Error Rate:**
- **Requests Dropped:**
- **Affected User Segments:**

---

## 3. Incident Timeline (UTC)
- **HH:MM** - Anomaly detected by alert `[Alert Name]`.
- **HH:MM** - Incident Commander paged; triage started.
- **HH:MM** - Fault isolated to commit `[hash]` or service `[name]`.
- **HH:MM** - Mitigation executed (e.g., traffic rolled back).
- **HH:MM** - Recovery verified; error rates returned to baseline.

---

## 4. Root Cause Analysis (5 Whys)
1. *Why did the service fail?* e.g., Unhandled database connection timeout.
2. *Why was there a timeout?* e.g., Table lock caused by migration.
3. *Why was table lock acquired?* e.g., `CREATE INDEX` executed without `CONCURRENTLY`.
4. *Why was `CONCURRENTLY` missing?* e.g., Migration script bypassed database linter.
5. *Why was it bypassed?* e.g., Gate check lacked automated concurrency flag rule.

---

## 5. What Went Well / What Went Wrong
- **Went Well:** Alert fired within 60 seconds; rollback was executed cleanly in 3 minutes.
- **Went Wrong:** Staging environment had low data volume so the lock was not observed in pre-prod.

---

## 6. Action Items & Remediation Tasks
| Action Item | Owner | Task ID | Target Date |
| :--- | :--- | :--- | :--- |
| Add rule blocking non-concurrent index migrations | `data-engineering-lead` | `TASK-501` | YYYY-MM-DD |
| Synthetic load test on staging with production-sized dataset | `performance-lead` | `TASK-502` | YYYY-MM-DD |
