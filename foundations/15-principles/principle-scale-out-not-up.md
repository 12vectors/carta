---
id: principle-scale-out-not-up
title: Scale Out, Not Up
type: principle
maturity: stable
pillar: "[[pillar-performance]]"
related_patterns:
  - "[[pattern-load-balancing]]"
  - "[[pattern-sharding]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-space-based-architecture]]"
tags: [principle, stable, performance-efficiency, scalability]
---

## Statement

Add instances before you add bigger boxes. Horizontal scale is elastic, incremental, and fault-tolerant; vertical scale is none of these.

## Rationale

Scaling up hits hard ceilings (the biggest box available) and has a coarse economic step (doubling the instance doubles the cost regardless of utilisation). Scaling out is elastic, bounded only by parallelism in the workload, and naturally fault-tolerant because losing one instance is a degradation, not an outage.

## How to apply

- Make services stateless wherever possible; push state to managed stores.
- Partition data so instances can operate independently.
- Prefer shared-nothing designs; avoid cross-instance locks.
- Design the work unit so N workers is N× the throughput.

## Related patterns

- [[pattern-load-balancing]] — distribute across identical instances.
- [[pattern-sharding]] — partition state for independent parallelism.
- [[pattern-competing-consumers]] — parallelise queue processing.
- [[pattern-space-based-architecture]] — in-memory grid for extreme scale-out.
