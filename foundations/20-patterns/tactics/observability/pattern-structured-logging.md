---
id: pattern-structured-logging
title: Structured Logging
type: pattern
category: observability
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
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

- Any production system — debugging, tracing, and alerting depend on it.
- Multi-service architectures where request correlation matters.
- Systems subject to audit or compliance trails.
- Anywhere log aggregation (ELK, Loki, Datadog) is available downstream.

## When NOT to use

- Throwaway scripts and prototypes — plain prints are fine.
- Extremely hot inner loops where serialisation cost is measurable — sample instead.
- Environments with no aggregator where humans grep the raw terminal output.

## Decision inputs

- Format — JSON Lines is the de facto standard.
- Mandatory fields: `timestamp`, `level`, `service`, `trace_id`, `message`.
- Optional fields: `span_id`, `user_id`, `endpoint`, `duration_ms`, `error_code`.
- Transport — stdout + orchestrator collection, or dedicated shipper.
- Retention tiers (hot / warm / cold) and cost.

## Solution sketch

Emit one JSON object per event to stdout. Message is a short event name; all context lives in fields. Propagate a `trace_id` generated at the boundary through every downstream call. Enforce a severity convention (DEBUG/INFO/WARN/ERROR/FATAL) across the org.

```json
{"timestamp":"2024-03-15T14:32:07.123Z","level":"ERROR","service":"order-service",
 "trace_id":"abc-123","endpoint":"POST /orders","error_code":"PAYMENT_TIMEOUT"}
```

See Observability Engineering ch. 6 for the events-vs-logs framing.

## Trade-offs

| Gain | Cost |
|------|------|
| Machine-parseable — queries, alerts, dashboards at scale | More verbose — higher storage and bandwidth |
| Correlation IDs enable cross-service tracing | Requires aggregator infrastructure to realise value |
| Consistent severity enables error-rate alerting | Less human-readable in a raw terminal |
| Foundation for compliance and forensics | Needs org-wide field-naming discipline |

## Implementation checklist

- [ ] Adopt a structured logging library for each language/runtime.
- [ ] Define and share the mandatory-field schema.
- [ ] Configure JSON Lines to stdout.
- [ ] Generate `trace_id` at the boundary; propagate through all downstream calls.
- [ ] Document and enforce severity-level meanings.
- [ ] Stand up an aggregator and verify queryable within minutes.
- [ ] Create at least one dashboard and one alert off log fields.
- [ ] Sample or rate-limit high-volume DEBUG logs in production.
- [ ] Define retention tiers and automate archival/deletion.

## See also

- [[pattern-circuit-breaker]] — log state transitions as structured events.
