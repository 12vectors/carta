---
id: pillar-cost
title: Cost Optimization
type: pillar
maturity: stable
tags: [pillar, stable, cost-optimization]
realised_by:
  - "[[principle-right-size-resources]]"
  - "[[principle-pay-for-what-you-use]]"
tradeoffs_with:
  - "[[pillar-reliability]]"
  - "[[pillar-performance]]"
sources:
  - "https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/"
  - "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/"
---

## Description

Cost optimization is the discipline of delivering business value at the lowest sustainable cost — not the cheapest possible infrastructure. It balances capacity against demand, elastically scales resources to match load, and eliminates unused or oversized components without compromising other pillars below acceptable levels.

## When this dominates

- Early-stage products where unit economics drive survival.
- Mature steady-state systems whose infrastructure spend is large enough that efficiency moves the P&L.
- Batch and asynchronous workloads where latency is flexible and scheduling is free variable.

## Trade-offs

| Gain | Cost |
|------|------|
| Lower infrastructure spend per unit of work | Tighter capacity reduces headroom for failure recovery ([[pillar-reliability]]) |
| Elastic scaling matches cost to demand | Cold-start and scale-out latency ([[pillar-performance]]) |
| Reserved / committed pricing reduces rates | Loss of flexibility to reshape architecture cheaply |

## Realised by

- [[principle-right-size-resources]] — provision for observed load, not worst-case guesses.
- [[principle-pay-for-what-you-use]] — prefer consumption-priced or autoscaled resources over always-on capacity.
- [[pattern-queue-based-load-leveling]], [[pattern-cache-aside]], [[pattern-throttling]] — patterns that improve cost efficiency.
