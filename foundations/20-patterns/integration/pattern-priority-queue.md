---
id: pattern-priority-queue
title: Priority Queue
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-performance]]"
tags: [pattern, stable, messaging, priority, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-competing-consumers]]"
  - "[[pattern-throttling]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/priority-queue"
---

## When to use

- Workloads mix latency-critical and background items on the same pipeline.
- Paying tiers or SLA-bound tenants must jump ahead of bulk work.
- Burst-driven flows where interactive requests must overtake batch jobs.
- Incident-response flows (alerts) must pre-empt routine telemetry.
- Low-priority backlog is acceptable as long as high-priority stays fast.

## When NOT to use

- All work has the same SLA — FIFO is simpler and fair.
- Priority logic hides a capacity problem that more workers would fix.
- Ordering matters globally — priority reorders messages by design.
- Low-priority traffic dwarfs high-priority and can starve the topology.

## Decision inputs

- Number of priority tiers — two is usually enough; more adds operational cost.
- Priority signal source — header, tenant, event type, SLA class.
- Starvation policy — age-based promotion or dedicated low-priority capacity?
- Consumer model — one queue per priority or a single priority-aware broker?
- SLA per tier — targets and alerts per priority class.
- Abuse mitigation — who can set high priority and how is it verified?

## Solution sketch

Two common shapes: **queue-per-priority** (simpler, more portable) or **single broker with priority semantics** (e.g. RabbitMQ x-max-priority). Consumers drain high before low, with starvation protection.

```
[Producer] --priority=hi--> [Queue-Hi] --+
                                         +-> [Consumer Pool]
           --priority=lo--> [Queue-Lo] --+
```

- Prefer **dedicated capacity** for high-priority: separate consumer group or reserved worker slots.
- Implement **anti-starvation**: age threshold promotes long-waiting low-priority items.
- Authenticate priority — do not let callers self-declare without policy checks.
- Measure **per-tier** latency and SLO; global p99 masks starvation.
- Keep the number of tiers small — two or three; more causes operational confusion.

## Trade-offs

| Gain | Cost |
|------|------|
| Latency-critical work bypasses bulk backlog | More queues or broker features to operate |
| Enables tiered SLAs on a shared pipeline | Low-priority starvation risk without age-promotion |
| Natural fit for tenant- or SLA-based differentiation | Priority can be abused — needs authorisation |
| Simple autoscaling per tier | Per-tier metrics and alerts multiply observability cost |

## Implementation checklist

- [ ] Define priority tiers and map them to SLAs — document each.
- [ ] Reserve capacity (worker slots or consumer group) for high-priority.
- [ ] Add age-based promotion or low-priority minimum service to prevent starvation.
- [ ] Authenticate and audit priority assignment.
- [ ] Emit per-tier queue depth, oldest-age, and end-to-end latency.
- [ ] Alert per-tier on SLO breach, not on aggregate.
- [ ] Load-test worst case: high-priority spike during low-priority flood.
- [ ] Document promotion/demotion rules for operators.

## See also

- [[pattern-competing-consumers]] — worker pool reads from each tier.
- [[pattern-throttling]] — often combined so low-priority cannot swamp resources.
- [[pattern-queue-based-load-leveling]] — priority is a refinement; load-level first.
