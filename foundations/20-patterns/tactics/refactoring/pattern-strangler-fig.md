---
id: pattern-strangler-fig
title: Strangler Fig
type: pattern
category: refactoring
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, refactoring, migration, legacy]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-anti-corruption-layer]]"
  - "[[pattern-modular-monolith]]"
  - "[[pattern-microservices]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html"
  - "StranglerFigApplication (Fowler, 2004) — https://martinfowler.com/bliki/StranglerFigApplication.html"
---

## When to use

- Replacing a legacy system too large or risky to rewrite in one shot.
- Migrating toward a new architecture incrementally while keeping the lights on.
- When partial value can be delivered as each capability is carved out.
- When rollback per capability is required to contain migration risk.

## When NOT to use

- Small systems where a straight rewrite is cheaper and shorter.
- Legacy without a stable seam to intercept traffic (no gateway, tight coupling).
- Teams unable to sustain parallel-run effort over months or years.
- Pure data migrations with no request surface to redirect.

## Decision inputs

- Traffic interception point — gateway, reverse proxy, facade service.
- Slicing strategy — by capability, endpoint, customer cohort, or data domain.
- Data ownership — dual-write, event replication, or hard cutover per slice.
- Rollback unit — per slice, per endpoint, per tenant.
- Decommissioning criteria for each legacy slice.

## Solution sketch

Put a **facade** (gateway, proxy, or thin service) in front of the legacy. Route each request to legacy by default. As each capability is rebuilt, flip the route for that capability to the new implementation. Keep data consistent via dual-write or event replication during parallel run. Retire the legacy capability once traffic is fully shifted and confidence is established. Repeat until the legacy is empty, then remove it.

```
[client] --> [facade] --/endpoint-A--> [legacy]
                       \--/endpoint-B--> [new service]
```

See Fowler's original essay for the metaphor and the AWS prescriptive guide for cloud execution.

## Trade-offs

| Gain | Cost |
|------|------|
| Incremental risk — one slice at a time | Parallel-run overhead (infra, data sync, ops) |
| Continuous delivery of value during migration | Long tail — the last 10% is often the hardest |
| Per-slice rollback contains blast radius | Facade and dual-write logic add complexity |
| No big-bang cutover | Organisational stamina required over long horizon |

## Implementation checklist

- [ ] Install a facade or gateway in front of the legacy.
- [ ] Inventory capabilities and pick the first slice (low-risk, high-value).
- [ ] Decide data-sync approach for that slice (dual-write, CDC, events).
- [ ] Build the new implementation behind a feature flag or route.
- [ ] Shadow-run traffic to the new service and compare outputs.
- [ ] Flip the route; monitor error and latency deltas.
- [ ] Define and execute decommissioning for the legacy slice.
- [ ] Track progress — legacy LOC, endpoints, or capabilities remaining.
- [ ] Budget for the long tail; do not skip decommissioning.

## See also

- [[pattern-anti-corruption-layer]] — shield the new model from legacy semantics during parallel run.
- [[pattern-modular-monolith]] — a common target architecture for strangled monoliths.
- [[pattern-microservices]] — another target; pick per capability and team shape.
