---
id: principle-observe-before-optimising
title: Observe Before Optimising
type: principle
maturity: stable
pillar: "[[pillar-operational-excellence]]"
related_patterns:
  - "[[pattern-structured-logging]]"
  - "[[pattern-distributed-tracing]]"
  - "[[pattern-red-metrics]]"
  - "[[pattern-correlation-id]]"
tags: [principle, stable, operational-excellence, observability]
---

## Statement

Instrument first; measure; then optimise. Guesses about bottlenecks are wrong more often than right.

## Rationale

Performance intuition is unreliable even for senior engineers; modern systems have too many layers and too much caching for mental models to hold. Optimising without measurement wastes time on the wrong hot paths and hides real regressions behind subjective claims. Observability turns optimisation into a feedback loop instead of a guessing game.

## How to apply

- Ship observability in the first commit, not after the first incident.
- Measure user-perceived latency (P95, P99), not only server-side averages.
- Trace end-to-end before optimising any single hop.
- Validate after each change with the same metrics you used to diagnose.

## Related patterns

- [[pattern-structured-logging]] — queryable, high-cardinality telemetry.
- [[pattern-distributed-tracing]] — see across service hops.
- [[pattern-red-metrics]] — the three numbers that matter per service.
- [[pattern-correlation-id]] — connect logs, traces, and user reports.
