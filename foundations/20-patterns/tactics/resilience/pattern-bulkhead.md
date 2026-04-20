---
id: pattern-bulkhead
title: Bulkhead
type: pattern
category: resilience
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, resilience, fault-tolerance, isolation]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-timeout]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Release It!, 2nd ed (Nygard, Pragmatic Bookshelf, 2018) — https://pragprog.com/titles/mnee2/release-it-second-edition/"
---

## When to use

- Single process calls multiple downstreams sharing one thread/connection pool.
- One slow dependency can exhaust resources and starve unrelated work.
- Multi-tenant systems where one tenant must not consume all capacity.
- Critical and non-critical traffic share infrastructure.
- Async consumers process mixed message types with differing SLAs.

## When NOT to use

- Single-dependency services with no contention to isolate.
- Low-traffic systems where pool exhaustion is not a realistic failure mode.
- Hard per-request latency budgets too tight for queueing overhead.

## Decision inputs

- Partition axis (per dependency, per tenant, per criticality, per endpoint).
- Pool size per partition based on observed concurrency and latency.
- Queue depth and rejection policy when a partition is saturated.
- Blast radius — how many partitions does one bad actor reach.
- Metrics on pool utilisation, rejections, and saturation per partition.

## Solution sketch

Partition resources — thread pools, connection pools, semaphores, queues — so failure in one compartment cannot drown the others. Each downstream dependency (or tenant, or workload class) gets its own bounded pool. When a partition saturates, requests into it fail fast while other partitions keep serving. Size pools from Little's Law: `pool = arrival_rate * p99_latency` with headroom.

```
[client] --> [pool-A: payments]   --> payments-svc (slow)
         \-> [pool-B: catalog]    --> catalog-svc  (healthy)
         \-> [pool-C: analytics]  --> analytics    (healthy)
```

See Nygard ch. 5 for sizing guidance and failure-mode analysis.

## Trade-offs

| Gain | Cost |
|------|------|
| Contains failure to one partition; unrelated work stays healthy | More pools to size, tune, and monitor |
| Enforces per-tenant/per-dependency capacity limits | Under-used partitions waste capacity vs shared pool |
| Makes saturation observable per dependency | Mis-sized partitions cause premature rejection |
| Composes with circuit breakers and timeouts | Adds queueing latency on the hot path |

## Implementation checklist

- [ ] Choose partition axis matching the dominant failure mode.
- [ ] Size each pool from `arrival_rate * p99_latency` with headroom.
- [ ] Set explicit queue depth and rejection policy per partition.
- [ ] Emit saturation, rejection, and queue-depth metrics per partition.
- [ ] Alert on sustained saturation or rejection rate.
- [ ] Load-test one partition to failure; confirm others stay healthy.
- [ ] Pair with `[[pattern-timeout]]` so stuck calls release pool slots.
- [ ] Pair with `[[pattern-circuit-breaker]]` to shed load on a failing partition.

## See also

- [[pattern-circuit-breaker]] — trip per partition to shed load fast.
- [[pattern-timeout]] — prevents pool slots from being held indefinitely.
- [[pattern-throttling]] — server-side load shedding complements bulkheads.
