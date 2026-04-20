---
id: pattern-distributed-tracing
title: Distributed Tracing
type: pattern
category: observability
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, observability, tracing]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-correlation-id]]"
related:
  - "[[pattern-correlation-id]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-red-metrics]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Dapper, a Large-Scale Distributed Systems Tracing Infrastructure (Sigelman et al., Google, 2010) — https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/"
  - "OpenTelemetry docs — https://opentelemetry.io/docs/"
---

## When to use

- Requests cross three or more services and latency or errors are hard to localise.
- Investigating tail latency where logs alone cannot attribute time spent.
- Debugging fan-out or async workflows with non-obvious causal chains.
- Measuring critical-path contribution per dependency for capacity planning.

## When NOT to use

- Single-process monoliths with local call stacks already exposed by the profiler.
- Prototypes where no aggregator or trace backend exists yet.
- Ultra-low-latency hot paths where instrumentation overhead is unacceptable — sample aggressively.

## Decision inputs

- Trace backend (Jaeger, Tempo, Honeycomb, Datadog, Cloud Trace) and retention cost.
- Sampling strategy — head-based, tail-based, or probabilistic — and target rate.
- Context-propagation standard (W3C `traceparent` is the default).
- Instrumentation surface — auto-instrumentation vs. manual spans for business logic.
- Async boundaries (queues, schedulers) that must carry context explicitly.

## Solution sketch

Every inbound request starts or continues a **trace** identified by `trace_id`. Each unit of work is a **span** with a `span_id` and `parent_span_id`. Propagate context via W3C `traceparent` headers across HTTP, gRPC, and message metadata. Use OpenTelemetry SDKs to auto-instrument frameworks; add manual spans for domain operations. Export via OTLP to a backend. Sample head-based at the edge; prefer tail-based sampling when error traces must always be kept.

```
[edge]--trace_id=abc--> [svc-A span1]--parent=span1--> [svc-B span2]
                                 \--parent=span1--> [queue msg (traceparent)]--> [svc-C span3]
```

See the Dapper paper for the original model and OpenTelemetry docs for current APIs.

## Trade-offs

| Gain | Cost |
|------|------|
| End-to-end latency attribution across services | SDK, collector, and backend infrastructure to run |
| Causal graph of fan-out and async workflows | Per-request overhead; sampling required at scale |
| Joins with logs and metrics via `trace_id` | Context propagation bugs silently break traces |
| Vendor-neutral via OpenTelemetry | Instrumenting legacy code and async boundaries is tedious |

## Implementation checklist

- [ ] Adopt OpenTelemetry SDKs for each runtime in the stack.
- [ ] Standardise on W3C `traceparent` propagation.
- [ ] Auto-instrument HTTP, gRPC, DB, and queue clients.
- [ ] Add manual spans around domain-critical operations.
- [ ] Propagate context through async boundaries (queues, schedulers, background jobs).
- [ ] Emit `trace_id` and `span_id` in structured logs.
- [ ] Choose and configure a sampling strategy; document the rate.
- [ ] Deploy an OTLP collector and a trace backend with retention policy.
- [ ] Build at least one latency-breakdown dashboard per critical path.

## See also

- [[pattern-correlation-id]] — prerequisite; trace IDs are the correlation mechanism for spans.
- [[pattern-structured-logging]] — join logs to traces via `trace_id`.
- [[pattern-red-metrics]] — metrics and traces answer complementary questions.
