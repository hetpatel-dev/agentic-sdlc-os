# Performance Baseline & Reliability Rules

This rule sets performance budgets, scalability requirements, resource utilization constraints, and load testing standards.

## 1. Latency & Throughput Budgets
- **Interactive Web / REST Endpoints:**
  - p95 latency must be under 200ms under standard operational load.
  - p99 latency must be under 500ms.
- **Background Jobs / Asynchronous Workers:**
  - Must report queue wait times, execution durations, and dead-letter queue metrics.
- Tasks exceeding these latency budgets must file an ADR detailing mitigation strategies before passing Gate G7.

## 2. Resource Utilization & Leaks
- Memory allocation must remain flat across sustained execution cycles. No unbounded caches or leaking event listeners.
- File descriptors, database connections, and network sockets must always be released in guaranteed cleanup blocks (`finally`, context managers `with`, `defer`).
- Database connection pools must be configured with explicit maximum sizes and acquisition timeouts.

## 3. Load & Resilience Testing
- Core revenue-impacting endpoints must undergo load testing at 2x expected peak volume prior to major releases.
- The system must demonstrate graceful degradation under load shedding rather than catastrophic cascading failure.
