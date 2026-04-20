---
id: principle-design-for-self-healing
title: Design for Self-Healing
type: principle
maturity: stable
pillar: "[[pillar-reliability]]"
related_patterns:
  - "[[pattern-health-check-endpoint]]"
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-leader-election]]"
tags: [principle, stable, reliability]
---

## Statement

Recover automatically without operator intervention. Operators react to alerts; systems heal themselves.

## Rationale

Human response time dominates mean-time-to-recovery. A system that can detect and correct its own faults — restart a stuck process, reroute around a failed replica, re-elect a leader — brings recovery from minutes to seconds and removes toil from on-call.

## How to apply

- Every long-running component exposes a liveness and readiness signal.
- The orchestrator (k8s, ECS, systemd, etc.) is authorised to restart unhealthy instances.
- Transient-fault handling (retries, backoff, circuit breakers) sits below the application code, not inside it.
- Operators are paged only for novel failures, not for known ones with automated recovery.

## Related patterns

- [[pattern-health-check-endpoint]] — let the platform see liveness.
- [[pattern-circuit-breaker]] + [[pattern-retry-with-backoff]] — absorb transient faults.
- [[pattern-leader-election]] — recover from coordinator loss without manual intervention.
