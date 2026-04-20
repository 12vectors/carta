---
id: principle-pay-for-what-you-use
title: Pay for What You Use
type: principle
maturity: stable
pillar: "[[pillar-cost]]"
related_patterns:
  - "[[pattern-queue-based-load-leveling]]"
  - "[[pattern-cache-aside]]"
  - "[[pattern-throttling]]"
tags: [principle, stable, cost-optimization, elasticity]
---

## Statement

Prefer consumption-priced or autoscaled resources over always-on capacity, unless steady-state pricing is demonstrably cheaper.

## Rationale

Idle capacity is pure waste. Consumption pricing and autoscaling align spend with value — no traffic, no bill. The asymmetric case (steady, predictable load) benefits from reserved capacity; most other workloads do not. The mistake is defaulting to provisioned capacity for workloads that don't need it.

## How to apply

- Profile utilisation before committing to reserved or dedicated capacity.
- Default to autoscaling groups or serverless for spiky workloads.
- Use reserved or committed pricing only where utilisation is demonstrably steady.
- Decommission or hibernate non-production resources outside work hours.
- Track cost per request, not just total spend.

## Related patterns

- [[pattern-queue-based-load-leveling]] — smooth demand so autoscaling has time to react.
- [[pattern-cache-aside]] — avoid the work entirely where possible.
- [[pattern-throttling]] — cap cost under pathological load.
