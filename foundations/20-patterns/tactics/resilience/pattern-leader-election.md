---
id: pattern-leader-election
title: Leader Election
type: pattern
category: resilience
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, resilience, coordination, distributed-systems]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-bulkhead]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/leader-election"
---

## When to use

- Multiple instances must coordinate on a singleton task (cron, reconcile, compaction).
- Exactly-one writer to a shared resource required for correctness.
- Scheduled jobs running in an HA fleet where duplicate execution is harmful.
- Stateful stream processors needing a single partition owner.
- Distributed cache invalidation or configuration refresh driver.

## When NOT to use

- Work that can be partitioned and run in parallel without coordination.
- Stateless idempotent tasks where duplicate execution is cheap.
- Single-node deployments — election adds nothing.
- Sub-second-critical paths where lease acquisition latency is unacceptable.

## Decision inputs

- Coordination backend (etcd, ZooKeeper, Consul, Redis, DB advisory lock, cloud lease).
- Lease duration vs renewal interval — renewal must comfortably beat expiry.
- Fencing token strategy to reject stale leaders' writes after partition.
- Failover target time — how long without a leader is acceptable.
- Split-brain cost — what breaks if two instances briefly think they lead.

## Solution sketch

Candidates race for a time-bounded lease in a consensus store. Holder renews before expiry; on failure to renew (crash, partition, GC pause), lease expires and another candidate acquires. Every write the leader performs carries a monotonic fencing token — downstream stores reject writes with a stale token, surviving split-brain windows. Prefer battle-tested stores (etcd, ZooKeeper) over DIY Redis locks for correctness-critical cases.

```
[inst-A] --acquire(lease, ttl=15s)--> [etcd] --granted, token=42--> leader
[inst-A] --renew every 5s-->
 (crash)
[inst-B] --acquire after 15s--> granted, token=43 (A's token=42 now stale)
```

See Azure Architecture Center (linked in sources) for backend trade-offs.

## Trade-offs

| Gain | Cost |
|------|------|
| Enables safe singleton work in an HA fleet | Coordination store becomes a critical dependency |
| Bounded failover time on leader crash | Split-brain windows exist without fencing tokens |
| Backends (etcd, ZooKeeper) are well-understood | Lease tuning is subtle — GC pauses break naive renewal |
| Works across language/runtime boundaries | Adds operational load (quorum health, backups) |

## Implementation checklist

- [ ] Pick a backend matching your correctness needs (etcd/ZK for strong, Redis for best-effort).
- [ ] Set lease TTL >> renewal interval >> worst-case GC pause.
- [ ] Issue and propagate a fencing token on every leader write.
- [ ] Have downstream stores reject stale tokens.
- [ ] Emit leader-change events and current-leader metric.
- [ ] Alert on frequent leader churn and on no-leader states.
- [ ] Test partition, crash, and slow-GC scenarios explicitly.
- [ ] Document graceful leader step-down on shutdown.

## See also

- [[pattern-bulkhead]] — isolate leader-only workload from follower traffic.
- [[pattern-health-check-endpoint]] — readiness can reflect leader status.
- [[pattern-structured-logging]] — log every lease transition.
