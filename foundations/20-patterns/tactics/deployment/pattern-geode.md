---
id: pattern-geode
title: Geode (Geo-distributed Nodes)
type: pattern
category: deployment
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, deployment, multi-region, latency]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-deployment-stamps]]"
  - "[[pattern-load-balancing]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/geodes"
---

## When to use

- Global user base where edge latency dominates perceived performance.
- Active-active multi-region required for RTO/RPO near zero.
- Read-heavy workloads tolerating eventual consistency across regions.
- Regulatory requirements that still permit cross-region replication of some data.

## When NOT to use

- Strong-consistency workloads (financial ledgers) where global coordination is unavoidable.
- Small user bases concentrated in one region — single-region is simpler and cheaper.
- Workloads dominated by write conflicts across regions.
- When deployment-stamp isolation (per region, not active-active) is sufficient.

## Decision inputs

- Consistency model — eventual, causal, or bounded staleness.
- Routing — latency-based DNS, Anycast, or global load balancer.
- Data replication — multi-master DB, CRDTs, or async replication with conflict rules.
- Conflict-resolution policy — last-writer-wins, app-level merge, or partitioned ownership.
- Failover semantics — automatic, weighted, or manual.

## Solution sketch

Deploy the full service stack in multiple regions, each a **geode**, serving all users. A global routing layer (latency DNS, Anycast, Front Door, Cloudfront) steers each request to the nearest healthy geode. Data replicates asynchronously between geodes; conflicts are handled by the chosen consistency and resolution strategy. Any geode can fail without user-visible outage — traffic shifts to the next nearest.

```
[user-EU] --> [edge router] --> [geode-eu]
[user-US] --> [edge router] --> [geode-us] <--async replication--> [geode-eu]
[user-AP] --> [edge router] --> [geode-ap]
```

See the Microsoft docs for data-tier patterns and conflict-resolution guidance.

## Trade-offs

| Gain | Cost |
|------|------|
| Low latency worldwide — serve from nearest node | Eventual consistency and conflict handling |
| Region failure is transparent to users | Multi-region replication infra and egress cost |
| Capacity scales by adding geodes | Complex schema evolution across regions |
| Natural geo-redundancy | Debugging spans multiple regions and clocks |

## Implementation checklist

- [ ] Pick consistency model and document staleness bounds.
- [ ] Choose replication technology compatible with the consistency model.
- [ ] Define conflict-resolution rules per data type.
- [ ] Deploy global routing with health-aware failover.
- [ ] Automate identical geode provisioning (IaC).
- [ ] Test a geode outage — automatic reroute, no data loss beyond RPO.
- [ ] Monitor replication lag per pair of geodes; alert on thresholds.
- [ ] Validate data-residency constraints per region.
- [ ] Budget cross-region egress and storage replication cost.

## See also

- [[pattern-deployment-stamps]] — stamps are isolated; geodes are actively replicated.
- [[pattern-load-balancing]] — geode selection is global load balancing by latency and health.
