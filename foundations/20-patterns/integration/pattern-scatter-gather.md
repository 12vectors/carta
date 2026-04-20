---
id: pattern-scatter-gather
title: Scatter-Gather
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-performance]]"
tags: [pattern, stable, messaging, aggregation, parallel, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-publish-subscribe]]"
  - "[[pattern-async-request-reply]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/scatter-gather.html"
  - "EIP (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/BroadcastAggregate.html"
---

## When to use

- A request must query multiple independent sources in parallel and combine their replies.
- Price quotes, search federation, insurance-bid aggregation, multi-region reads.
- Latency budget allows the slowest responder — or a partial-results strategy.
- Sources are autonomous and cannot be consolidated into one service.
- You want best-effort completeness with a bounded wait.

## When NOT to use

- One source is sufficient — avoid fan-out cost.
- Strict all-or-nothing semantics — use a saga or 2PC, not scatter-gather.
- Sources have wildly different SLAs and the slowest blocks everyone.
- Fan-out cost (per-source quota, compute) is prohibitive at scale.

## Decision inputs

- Number of recipients and their latency distributions.
- Completion policy — wait-for-all, first-N, or deadline-based.
- Aggregation function — merge, rank, dedupe, score.
- Correlation strategy — one key threads requests and replies.
- Timeout per recipient and overall deadline.
- Partial-result tolerance and how it is surfaced to the caller.

## Solution sketch

Dispatch the same request to N recipients in parallel; an **aggregator** collects replies, correlates them, and applies a completion rule before returning.

```
                 +-> [Service A] -+
[Caller] -> [Scatter] -> [Service B] -+-> [Gather/Aggregator] -> [Caller]
                 +-> [Service C] -+
```

- Use a **correlation ID** on every outbound request to match replies.
- Pick a **completion condition**: all-replied, first-N, or timeout-hit — and document it.
- Gather must handle **late replies** — discard or log; never mutate state.
- Expose partial-result mode explicitly; do not silently drop slow responders.
- Cap fan-out — unbounded scatter is a self-inflicted DoS.

## Trade-offs

| Gain | Cost |
|------|------|
| Parallel fan-out reduces wall time to slowest responder | End-to-end latency bounded by slowest (or timeout) |
| Keeps sources autonomous and independently scaled | Aggregator is a choke point and a stateful component |
| Partial results recover from individual failures | Correctness of aggregation is harder to test |
| Natural fit for federation and best-effort reads | Per-request fan-out cost multiplies downstream load |

## Implementation checklist

- [ ] Assign a correlation ID per request — see `[[pattern-correlation-id]]`.
- [ ] Pick a completion rule (all / first-N / deadline) and encode it explicitly.
- [ ] Set a per-recipient timeout; also an overall deadline.
- [ ] Aggregate idempotently — handle duplicate and late replies.
- [ ] Surface partial-result mode to callers; do not hide it.
- [ ] Emit per-recipient latency and failure rate; alert on straggler patterns.
- [ ] Cap concurrent fan-out and apply circuit breakers to recipients.
- [ ] Load-test degraded-recipient scenarios.

## See also

- [[pattern-publish-subscribe]] — fan-out mechanism for the scatter leg.
- [[pattern-async-request-reply]] — gather half resembles correlated reply collection.
- [[pattern-circuit-breaker]] — protect the aggregator from a persistently slow recipient.
