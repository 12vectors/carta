---
id: pattern-materialized-view
title: Materialized View
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-performance]]"
tags: [pattern, stable, data, projection, query-optimisation]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-cqrs]]"
  - "[[pattern-read-replica]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view"
---

## When to use

- Recurring queries are expensive (joins, aggregations, cross-source).
- Results are read far more often than the underlying data changes.
- Staleness on the order of seconds to minutes is acceptable.
- Query shape is stable enough to justify a dedicated projection.
- You need to combine data from multiple services or stores into one read.

## When NOT to use

- Ad-hoc, unpredictable queries — you can't pre-materialise everything.
- Strong read-your-writes requirements on the materialised data.
- Low-volume queries where on-demand computation is cheap.
- Source data changes so fast that refresh cost exceeds query savings.

## Decision inputs

- Refresh strategy — event-driven, CDC, scheduled, or on-demand.
- Acceptable staleness per view (SLA).
- Storage footprint and growth rate of the projection.
- Rebuild cost and time — can you regenerate from source on demand.
- Ownership — who updates the view when the source schema changes.

## Solution sketch

Precompute and persist the result of a query as a separate read-only store shaped exactly for the consumer. Keep it up to date by reacting to changes in the sources (events, CDC, triggers) or refreshing on a schedule. Queries hit the view; writes never do.

```
[Source A] --\
              >-- [Projector] --> [Materialized view] <-- reads -- [Client]
[Source B] --/
```

The view is disposable — if it's wrong, rebuild it from sources. That changes schema migrations from in-place alters to "stand up v2, switch readers, drop v1". Pair with event-driven updates when possible; fall back to scheduled refresh when source systems don't emit change events.

## Trade-offs

| Gain | Cost |
|------|------|
| Query latency drops from joins/aggregates to point reads | Stale data within the refresh window |
| One view can combine multiple sources for clients | Extra storage and a projector to operate |
| Views are disposable — schema changes are rebuilds | Projector must be idempotent and restartable |
| Shields source systems from expensive query load | Cache invalidation becomes projection correctness |

## Implementation checklist

- [ ] Identify a query that is both expensive and frequent.
- [ ] Design the view schema around the query, not the source tables.
- [ ] Choose refresh mechanism (events, CDC, schedule) and justify it.
- [ ] Make the projector idempotent with a checkpoint/offset.
- [ ] Monitor projector lag and view staleness.
- [ ] Document and test the rebuild-from-sources procedure.
- [ ] Decide on deletion/eviction for rows no longer relevant.
- [ ] Version the view schema; treat breaking changes as new views.

## See also

- [[pattern-cqrs]] — materialised views are the canonical read side of CQRS.
- [[pattern-read-replica]] — simpler when the read shape equals the source.
- [[pattern-cache-aside]] — per-query caching as a lighter alternative.
- [[pattern-event-sourcing]] — natural source for event-driven views.
