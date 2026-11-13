# Observability & SRE Standards

This rule governs structured telemetry (logs, metrics, traces), health checking, alerting policies, and incident telemetry.

## 1. Structured Logging
- All application logs must be emitted in structured JSON format to `stdout`/`stderr`.
- Every log entry must include standard contextual fields:
  - `timestamp` (ISO-8601 UTC)
  - `level` (`DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`)
  - `service` (microservice or module name)
  - `trace_id` & `span_id` (OpenTelemetry distributed tracing context)
  - `message` (concise human-readable description)
  - `context` (key-value metadata; never log raw PII or secret credentials)

## 2. Standard Metrics (RED / USE)
- Request-driven services must export RED metrics:
  - **Rate:** Requests per second.
  - **Errors:** Failed requests per second (by HTTP status or error code).
  - **Duration:** Latency histograms (p50, p95, p99).
- Resource-driven components must export USE metrics:
  - **Utilization:** % time resource is busy (CPU, memory, disk).
  - **Saturation:** Queue depths or pending requests.
  - **Errors:** Hardware or driver error events.

## 3. Distributed Tracing & Health Probes
- All inbound and outbound RPC/HTTP calls must propagate W3C TraceContext headers.
- Services must provide:
  - `/healthz` or `/live`: Liveness probe indicating process is alive.
  - `/ready`: Readiness probe indicating all downstream dependencies (database, cache) are healthy.
