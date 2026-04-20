---
id: pattern-throttling
title: Throttling
type: pattern
category: resilience
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-cost]]"
tags: [pattern, stable, resilience, load-shedding, capacity]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-rate-limiting]]"
  - "[[pattern-queue-based-load-leveling]]"
  - "[[pattern-bulkhead]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling"
---

## When to use

- Protect a service from total collapse when offered load exceeds capacity.
- Traffic spikes (viral events, retry storms) threaten availability for everyone.
- Cost ceiling on autoscaling — shed rather than scale unbounded.
- Shared infrastructure where one noisy workload can starve others.
- Back-pressure signal needed upstream when queues grow unboundedly.

## When NOT to use

- Per-client quota or fairness — use `[[pattern-rate-limiting]]` instead.
- Capacity is elastic and cheap; autoscale rather than shed.
- Dropping requests violates the business contract (use queues + SLAs).

## Decision inputs

- Shed signal — CPU, queue depth, p99 latency, concurrency, downstream errors.
- Shed policy — reject (503/429), degrade (reduced functionality), defer (queue).
- Priority classes — which traffic sheds first (background before interactive).
- Recovery behaviour — hysteresis to avoid flapping between shed/serve.
- Observability — clients must know they were shed, not failed mysteriously.

## Solution sketch

Server-side load shedding: when a saturation signal crosses threshold, reject or degrade excess work so the service stays healthy for retained traffic. Differs from rate limiting — rate limiting enforces per-client quotas regardless of server state; throttling reacts to server state and can shed any client. Common policies: drop lowest-priority traffic first, return 503 with `Retry-After`, serve degraded responses (cached, partial). Combine with bulkheads so shedding happens per partition.

```
load < threshold   → serve all
threshold < load   → shed priority-3 traffic
critical < load    → shed priority-2; degrade priority-1 responses
```

See Azure Architecture Center (linked in sources) for policy patterns.

## Trade-offs

| Gain | Cost |
|------|------|
| Keeps service healthy under overload | Sheds real user traffic — visible failure |
| Bounds cost vs unbounded autoscale | Threshold tuning requires load-test data |
| Enables graceful degradation by priority | Retry storms can follow if clients ignore `Retry-After` |
| Provides back-pressure signal upstream | Needs priority classification baked into requests |

## Implementation checklist

- [ ] Pick the saturation signal (CPU, queue depth, concurrency, p99).
- [ ] Define thresholds from load-test results, not guesses.
- [ ] Classify traffic by priority; decide shed order.
- [ ] Return 503/429 with `Retry-After` and a clear shed reason.
- [ ] Add hysteresis (different thresholds for enter/exit shed).
- [ ] Emit shed counts, rates, and active-class metrics.
- [ ] Coordinate with client retry/backoff to avoid amplification.
- [ ] Load-test the shed path — confirm service stays healthy.

## See also

- [[pattern-rate-limiting]] — per-client quota; throttling is server-side shedding — use both.
- [[pattern-queue-based-load-leveling]] — defer instead of shed when queueing is acceptable.
- [[pattern-bulkhead]] — throttle per partition for isolation.
