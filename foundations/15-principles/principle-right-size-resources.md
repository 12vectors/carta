---
id: principle-right-size-resources
title: Right-Size Resources
type: principle
maturity: stable
pillar: "[[pillar-cost]]"
related_patterns:
  - "[[pattern-load-balancing]]"
  - "[[pattern-queue-based-load-leveling]]"
  - "[[pattern-throttling]]"
tags: [principle, stable, cost-optimization]
---

## Statement

Provision for observed load, not worst-case guesses. Reshape the system to match demand.

## Rationale

Over-provisioning is the default response to uncertainty; it also silently consumes the bulk of infrastructure spend. Most systems run at 10–20% average utilisation because capacity is sized for tail events without elasticity. Observed load plus elastic scaling is cheaper and more honest than static overcommit.

## How to apply

- Measure P50, P95, P99 load, not average.
- Match compute shape to workload shape (CPU-bound, memory-bound, burst, batch).
- Scale out on demand signals; scale in on quiet signals.
- Flatten spikes with queues rather than buying for the peak.

## Related patterns

- [[pattern-load-balancing]] — distribute so instances can be sized smaller.
- [[pattern-queue-based-load-leveling]] — trade latency for peak capacity.
- [[pattern-throttling]] — shed load rather than over-provision for it.
