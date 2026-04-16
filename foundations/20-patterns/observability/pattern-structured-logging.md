---
id: pattern-structured-logging
title: Structured Logging
type: pattern
category: observability
maturity: stable
tags: [pattern, stable, observability, logging]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
prerequisites: []
related:
  - "[[pattern-circuit-breaker]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Observability Engineering (Majors et al., 2022) ch. 6"
  - "https://www.honeycomb.io/blog/how-are-structured-logs-different-from-events"
---

## When to use

Apply structured logging in any production system where you need to debug issues, trace requests across service boundaries, or understand runtime behaviour. Specific triggers:

- **Multi-service architectures.** When a request touches more than one service, plain-text logs become nearly impossible to correlate. Structured fields (trace_id, span_id, service) make cross-service debugging tractable.
- **Production incident response.** When something breaks at 2 AM, you need to filter logs by user, endpoint, error code, and time window. Structured fields make this a query, not a grep.
- **Alerting and dashboards.** Log aggregation systems (Elasticsearch, Loki, Datadog) can parse structured logs into metrics, powering alerts and dashboards without separate instrumentation.
- **Compliance and audit trails.** Structured logs provide consistent, machine-verifiable records of what happened, when, and who triggered it.

## When NOT to use

- **Throwaway scripts and prototypes.** If the code will run once and be discarded, printf debugging is faster and perfectly adequate. Don't over-engineer logging for code that won't see production.
- **Extremely latency-sensitive hot paths.** In tight inner loops processing millions of events per second, even the overhead of serializing a JSON log line can matter. Profile before adding logging to hot paths, and consider sampling instead of logging every event.
- **Environments with no log aggregation.** Structured JSON logs are harder to read with the naked eye than plain text. If there is no log aggregation infrastructure and logs are only read by humans scrolling a terminal, the verbosity may hurt more than it helps.

## Decision inputs

Before implementing, resolve these questions:

- **What format?** JSON Lines (one JSON object per line) is the de facto standard. It is universally supported by log aggregators, trivially parseable, and avoids multi-line log complications.
- **What fields are mandatory?** At minimum, every log event should include:
  - `timestamp` -- ISO 8601 with timezone (e.g. `2024-03-15T14:32:07.123Z`)
  - `level` -- severity: DEBUG, INFO, WARN, ERROR, FATAL
  - `service` -- the name of the emitting service
  - `trace_id` -- a correlation ID linking all logs for a single request or workflow
  - `message` -- a human-readable description of the event
- **What optional fields are useful?** `span_id`, `user_id`, `endpoint`, `duration_ms`, `error_code`, `stack_trace` (for errors only).
- **Where do logs ship?** For containerized workloads, emit to stdout and let the orchestrator (Kubernetes, ECS) collect them. For VMs, use a log shipper (Fluentd, Filebeat) to forward to a central aggregator.
- **What is the log retention policy?** Structured logs are more verbose than plain text. Define retention tiers: hot storage (7-30 days, queryable), warm storage (90 days, slower), cold archive (1+ year, compliance).

## Solution sketch

1. **Emit logs as structured JSON objects.** Replace `log.info("User 42 logged in")` with `log.info("user_login", user_id=42, method="oauth", ip="10.0.1.5")`. The message becomes a short event name; all context lives in fields.

2. **Include correlation IDs for request tracing.** Generate a `trace_id` at the system boundary (API gateway, message consumer) and propagate it through every downstream call and log statement. This single field turns isolated log lines into a coherent story.

3. **Use severity levels consistently.** Define what each level means for your team and enforce it:
   - `DEBUG` -- verbose detail useful only during development or targeted diagnostics
   - `INFO` -- normal operations worth recording (request served, job completed)
   - `WARN` -- unexpected but handled conditions (retry triggered, cache miss, deprecated endpoint called)
   - `ERROR` -- failures that need attention (unhandled exception, downstream timeout after retries exhausted)
   - `FATAL` -- the process cannot continue and is shutting down

4. **Ship to a log aggregator.** Configure the runtime to write JSON to stdout. Use infrastructure-level collection (Fluentd sidecar, CloudWatch Logs agent, Datadog agent) to forward logs to a central system where they can be searched, filtered, and visualized.

```json
{
  "timestamp": "2024-03-15T14:32:07.123Z",
  "level": "ERROR",
  "service": "order-service",
  "trace_id": "abc-123-def-456",
  "span_id": "span-789",
  "user_id": 42,
  "endpoint": "POST /orders",
  "duration_ms": 1523,
  "error_code": "PAYMENT_TIMEOUT",
  "message": "Payment gateway timed out after 3 retries"
}
```

## Trade-offs

| Gain | Cost |
|------|------|
| Machine-parseable logs enable querying, filtering, alerting, and dashboards at scale | More verbose than plain text -- higher storage and bandwidth consumption |
| Correlation IDs support distributed tracing across service boundaries | Requires log aggregation infrastructure (ELK, Loki, Datadog) to realise full value |
| Consistent severity levels make it possible to alert on error rates and spot trends | Structured format is less human-readable in a raw terminal compared to plain text |
| Provides a foundation for compliance, audit trails, and forensic analysis | Teams need to agree on field naming conventions and enforce them across services |

## Implementation checklist

- [ ] Choose a structured logging library appropriate for your language and framework
- [ ] Define mandatory fields (timestamp, level, service, trace_id, message) in a shared schema
- [ ] Configure the logger to emit JSON Lines to stdout
- [ ] Propagate trace_id from the request boundary through all downstream calls and log statements
- [ ] Document severity level definitions and get team agreement on usage
- [ ] Set up a log aggregator and verify that logs are searchable within minutes of emission
- [ ] Create at least one dashboard and one alert based on structured log fields
- [ ] Add log sampling or rate limiting for high-volume DEBUG-level logs in production
- [ ] Define retention tiers and configure automatic archival or deletion

## See also

- [[pattern-circuit-breaker]] -- circuit breaker state changes (open, half-open, closed) should be logged as structured events for operational visibility
