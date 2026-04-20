---
id: pattern-cqrs
title: Command Query Responsibility Segregation
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, data, cqrs, read-write-separation]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-event-sourcing]]"
  - "[[pattern-materialized-view]]"
  - "[[pattern-read-replica]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://martinfowler.com/bliki/CQRS.html"
  - "CQRS Documents (Young, 2010) — https://cqrs.wordpress.com/wp-content/uploads/2010/11/cqrs_documents.pdf"
---

## When to use

- Read and write workloads have very different shapes, scale, or consistency needs.
- Complex domain writes coexist with many simple, high-volume queries.
- Read-side denormalisation materially simplifies query code.
- Eventual consistency on the read side is acceptable to the business.
- You already tolerate (or plan) asynchronous replication between stores.

## When NOT to use

- CRUD apps where reads and writes share the same shape.
- Small teams or simple domains — the split doubles the moving parts.
- Strong read-your-writes requirements across all queries.
- Low-traffic systems where a single model performs fine.

## Decision inputs

- Read/write ratio and divergence in access patterns.
- Acceptable staleness window on the read side (ms, seconds, minutes).
- Whether the domain already emits events or can be made to.
- Operational capacity to run and monitor two stores.
- Query complexity — joins, aggregations, search.

## Solution sketch

Split the model into a **command side** (validates, mutates, writes authoritative state) and a **query side** (read-optimised projections serving UI and APIs). Commands run against the write store; a projector consumes changes (CDC, events, or outbox) and updates one or more read stores shaped per query. Queries never touch the write store.

```
[Client] --command--> [Write model] --events/CDC--> [Projector] --> [Read model(s)] <--query-- [Client]
```

Projections can be rebuilt from the source of truth, so schema changes are replays, not migrations. Combine with event sourcing when the write model is itself an event log; otherwise emit change events via outbox.

## Trade-offs

| Gain | Cost |
|------|------|
| Reads and writes scale and evolve independently | Two models, two stores, two deployment paths |
| Query-shaped projections eliminate expensive joins | Eventual consistency surfaces in UX and APIs |
| Rebuilding a projection is a replay, not a migration | Projector lag must be monitored and alerted |
| Clear boundary between domain logic and read serving | Developer cognitive load roughly doubles |

## Implementation checklist

- [ ] Identify a bounded context where the split pays for itself.
- [ ] Choose the change-propagation mechanism (outbox, CDC, event log).
- [ ] Design read models per query, not per entity.
- [ ] Make projectors idempotent and restartable from a checkpoint.
- [ ] Expose staleness metrics (projector lag) and alert on them.
- [ ] Decide UX for read-your-writes (client echo, sync read after write).
- [ ] Document rebuild procedure for each projection.
- [ ] Integration-test write, project, and query paths end-to-end.

## See also

- [[pattern-event-sourcing]] — natural source of truth for the command side.
- [[pattern-materialized-view]] — the shape most read projections take.
- [[pattern-read-replica]] — simpler alternative when the split is only about read scale.
- [[pattern-transactional-outbox]] — reliable change propagation to projectors.
