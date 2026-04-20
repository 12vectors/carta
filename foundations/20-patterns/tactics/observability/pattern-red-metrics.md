---
id: pattern-red-metrics
title: RED Metrics (Rate, Errors, Duration)
type: pattern
category: observability
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, observability, metrics, slo]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-distributed-tracing]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-health-check-endpoint]]"
conflicts_with: []
contradicted_by: []
sources:
  - "The RED Method (Wilkie, Grafana Labs blog, 2018) — https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/"
  - "The USE Method (Gregg) — https://www.brendangregg.com/usemethod.html"
---

## When to use

- Request-driven services where user-visible behaviour is the SLO target.
- Standardising a minimum bar for instrumentation across many services.
- Defining SLOs around availability and latency without bespoke metrics per team.
- Dashboards and alerting for service health at a glance.

## When NOT to use

- Resource-bound workloads (batch jobs, DBs, queues) — USE (Utilisation, Saturation, Errors) fits better.
- Pure data pipelines measured by throughput and lag — use pipeline-specific metrics.
- One-off scripts with no persistent operator.

## Decision inputs

- Metrics backend (Prometheus, Cloud Monitoring, Datadog) and cardinality budget.
- Label set — endpoint, method, status class — and cardinality limits.
- Histogram buckets for duration — aligned to SLO thresholds.
- Error definition — which status codes count; client errors usually excluded.
- Aggregation window and percentile targets (p50, p95, p99).

## Solution sketch

For every request-handling surface emit three metrics:

- **Rate** — requests per second (counter, rate-able).
- **Errors** — error requests per second (counter; 5xx typically, not 4xx).
- **Duration** — latency distribution (histogram with SLO-aligned buckets).

Label by `service`, `endpoint`, and `status_class`. Keep label cardinality bounded. Combine with USE for infrastructure and tracing for root-cause drill-down.

```
http_requests_total{service="orders",endpoint="POST /orders",status_class="5xx"}
http_request_duration_seconds_bucket{service="orders",endpoint="POST /orders",le="0.5"}
```

See the RED Method post for the framing and USE for complementary resource metrics.

## Trade-offs

| Gain | Cost |
|------|------|
| Uniform service-health signal across the fleet | Hides resource saturation — pair with USE |
| Histograms support percentile SLOs directly | Cardinality explodes with unbounded labels |
| Cheap to alert on; widely tooled | Does not explain *why* — tracing still required |
| Vendor-neutral via OpenTelemetry / Prometheus | Requires discipline to keep definitions consistent |

## Implementation checklist

- [ ] Instrument every inbound handler with rate, errors, duration.
- [ ] Agree error definition across services (typically 5xx, excluding 4xx).
- [ ] Bound label cardinality — never label by user or request ID.
- [ ] Choose histogram buckets aligned to SLO thresholds.
- [ ] Export to the metrics backend via standard exporter.
- [ ] Build a per-service RED dashboard.
- [ ] Define SLOs and burn-rate alerts off the same metrics.
- [ ] Pair with USE for resource-bound components.

## See also

- [[pattern-distributed-tracing]] — metrics tell you something is wrong; traces tell you where.
- [[pattern-structured-logging]] — drill from a spiking metric to the offending logs.
- [[pattern-health-check-endpoint]] — liveness/readiness complement traffic-driven metrics.
