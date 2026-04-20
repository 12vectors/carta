---
id: principle-design-for-failure
title: Design for Failure
type: principle
maturity: stable
pillar: "[[pillar-reliability]]"
related_patterns:
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-bulkhead]]"
  - "[[pattern-timeout]]"
tags: [principle, stable, reliability]
---

## Statement

Assume every dependency will fail. Encode the failure behaviour as a first-class code path.

## Rationale

Systems at any scale experience partial failure — network blips, slow downstreams, resource exhaustion, bad deploys. Designs that assume success degrade catastrophically when reality intervenes. Reliability is not about preventing failure; it is about absorbing it predictably.

## How to apply

- Enumerate each external dependency's failure modes at design time.
- Specify the fallback or graceful-degradation behaviour per failure class.
- Encode the fallback as a first-class code path, not a caught exception.
- Exercise the failure paths in CI — integration-level fault injection catches the bugs mocks hide.

## Related patterns

- [[pattern-circuit-breaker]] — fail fast when dependencies are down.
- [[pattern-retry-with-backoff]] — absorb transient blips.
- [[pattern-bulkhead]] — contain failure to isolated pools.
- [[pattern-timeout]] — bound waiting.
