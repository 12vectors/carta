---
id: principle-cache-close-to-consumer
title: Cache Close to the Consumer
type: principle
maturity: stable
pillar: "[[pillar-performance]]"
related_patterns:
  - "[[pattern-cache-aside]]"
  - "[[pattern-materialized-view]]"
  - "[[pattern-read-replica]]"
  - "[[pattern-geode]]"
tags: [principle, stable, performance-efficiency, caching]
---

## Statement

Serve reads from the layer closest to the consumer that can serve them correctly. Each hop further from the consumer is latency and cost the consumer pays.

## Rationale

Network and disk hops dominate response time for most read-heavy workloads. The cache-friendly rule: the right answer is the one that avoids the most hops without violating staleness requirements. Materialised views, read replicas, and edge caches all realise this — they move answers toward the consumer.

## How to apply

- State the maximum tolerable staleness per read path; choose caching layer accordingly.
- Prefer read-through or cache-aside over hand-rolled invalidation.
- Put static and semi-static content on a CDN.
- Shorten feedback loops between write and cache-invalidation events.

## Related patterns

- [[pattern-cache-aside]] — populate on miss; serve from cache on hit.
- [[pattern-materialized-view]] — precompute the answer.
- [[pattern-read-replica]] — scale reads horizontally.
- [[pattern-geode]] — geographically-distributed read paths.
