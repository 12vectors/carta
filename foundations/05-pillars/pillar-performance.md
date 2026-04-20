---
id: pillar-performance
title: Performance Efficiency
type: pillar
maturity: stable
tags: [pillar, stable, performance-efficiency]
realised_by:
  - "[[principle-scale-out-not-up]]"
  - "[[principle-cache-close-to-consumer]]"
  - "[[principle-do-less-work]]"
tradeoffs_with:
  - "[[pillar-cost]]"
  - "[[pillar-reliability]]"
sources:
  - "https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/"
  - "https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/"
---

## Description

Performance efficiency is the system's ability to meet its latency, throughput, and scalability targets using the resources it has. It covers architectural choices (caching, sharding, async vs sync), data access patterns, and the ability to scale horizontally in response to load.

## When this dominates

- Latency-sensitive user-facing paths (search, checkout, live interaction).
- Systems with spiky load where elasticity matters more than steady-state capacity.
- Data-heavy pipelines where throughput per dollar is the operative metric.

## Trade-offs

| Gain | Cost |
|------|------|
| Lower tail latency and higher throughput | Aggressive caching and precomputation raise infrastructure cost ([[pillar-cost]]) |
| Horizontal scale and elasticity under load | Distributed-systems failure modes multiply ([[pillar-reliability]]) |
| Close-to-consumer data access | Consistency is weaker; staleness becomes a first-class concern |

## Realised by

- [[principle-scale-out-not-up]] — add instances before you add bigger boxes.
- [[principle-cache-close-to-consumer]] — bring the data to the request.
- [[principle-do-less-work]] — the fastest operation is the one not performed.
- [[pattern-cache-aside]], [[pattern-sharding]], [[pattern-read-replica]], [[pattern-load-balancing]] — patterns that realise these principles.
