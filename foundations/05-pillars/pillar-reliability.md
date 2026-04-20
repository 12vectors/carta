---
id: pillar-reliability
title: Reliability
type: pillar
maturity: stable
tags: [pillar, stable]
realised_by:
  - "[[principle-design-for-failure]]"
  - "[[principle-design-for-self-healing]]"
  - "[[principle-minimize-coordination]]"
tradeoffs_with:
  - "[[pillar-cost]]"
  - "[[pillar-performance]]"
sources:
  - "https://learn.microsoft.com/en-us/azure/well-architected/reliability/"
  - "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/"
---

## Description

Reliability is the system's ability to meet its uptime, recovery, and correctness targets in the face of faults — partial failures, dependency outages, infrastructure loss, load spikes. It is measured against explicit SLOs; it is not a qualitative aspiration.

## When this dominates

- User-visible systems where downtime maps directly to revenue or trust loss.
- Systems with hard recovery-time or recovery-point objectives (financial, medical, compliance-driven).
- Multi-region or multi-tenant platforms where a single failure would cascade.

## Trade-offs

| Gain | Cost |
|------|------|
| Higher availability under fault and load | Redundancy and replication raise infrastructure cost ([[pillar-cost]]) |
| Graceful degradation preserves partial function | Fallback and state-replication paths add latency ([[pillar-performance]]) |
| Lower mean time to recovery | Retry, timeout, and circuit logic add code-path complexity |

## Realised by

- [[principle-design-for-failure]] — assume dependencies fail and plan for it.
- [[principle-design-for-self-healing]] — recover automatically without operator intervention.
- [[pattern-circuit-breaker]], [[pattern-retry-with-backoff]], [[pattern-bulkhead]], [[pattern-timeout]] — tactical patterns that encode these principles.
