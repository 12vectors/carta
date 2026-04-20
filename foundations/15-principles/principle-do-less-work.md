---
id: principle-do-less-work
title: Do Less Work
type: principle
maturity: stable
pillar: "[[pillar-performance]]"
related_patterns:
  - "[[pattern-cache-aside]]"
  - "[[pattern-materialized-view]]"
  - "[[pattern-queue-based-load-leveling]]"
  - "[[pattern-throttling]]"
tags: [principle, stable, performance-efficiency]
---

## Statement

The fastest operation is the one not performed. Batch, cache, defer, or eliminate before you optimise the hot path.

## Rationale

Micro-optimisation inside a hot path has a ceiling; removing the path entirely does not. Before tuning, ask whether the work must happen now, happen at all, or happen per-request. Batching, precomputation, lazy evaluation, and dropping unnecessary calls routinely yield order-of-magnitude wins that micro-optimisation cannot touch.

## How to apply

- Profile the call path; ask of each step "does this need to run, and does it need to run now?"
- Batch similar operations; amortise fixed costs.
- Precompute results that are read more often than they change.
- Defer non-critical work to background queues.
- Shed load when doing less is the only way to meet the SLO.

## Related patterns

- [[pattern-cache-aside]] — don't redo work for the same input.
- [[pattern-materialized-view]] — precompute the read.
- [[pattern-queue-based-load-leveling]] — defer the work.
- [[pattern-throttling]] — cap the work when necessary.
