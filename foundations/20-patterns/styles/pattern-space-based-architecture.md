---
id: pattern-space-based-architecture
title: Space-Based Architecture
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, style, in-memory, elastic-scale, tuple-space]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-event-driven-architecture]]"
  - "[[pattern-cqrs]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Software Architecture Patterns (Richards, 2015) ch. 5"
  - "https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/"
---

## When to use

- Extreme, spiky concurrent load where the database is the bottleneck.
- Low-latency read/write workloads tolerating eventual durability.
- Applications that must scale out elastically (gaming, trading, ticketing, auctions).
- Workloads whose working set fits in replicated memory across nodes.

## When NOT to use

- Strongly durable, transactional systems — in-memory replication trades durability.
- Small or predictable load — complexity isn't justified.
- Reporting and complex query workloads — grid is optimised for operational access.
- Teams without operational capability for data grids and async replication.

## Decision inputs

- Working-set size vs per-node memory budget.
- Replication topology and consistency model across processing units.
- Data-writer SLA (how long the DB may lag the grid).
- Failure and recovery behaviour when a unit or the grid dies.
- Partitioning key for horizontal scale-out.

## Solution sketch

Requests hit **processing units** that hold application code plus an **in-memory replicated data grid**. No synchronous database reads on the hot path. A **data-writer** asynchronously persists grid changes to the database; a **data-reader** repopulates the grid on cold start. Units replicate grid state peer-to-peer.

```
     [ load balancer ]
            |
  [ processing unit ]  <== replicated grid ==> [ processing unit ]
            \                                      /
             \---> [ data writer ] --async--> [ DB ]
                   [ data reader ] <---cold---/
```

See Richards ch. 5 (linked) for grid, messaging grid, and deployment manager details.

## Trade-offs

| Gain | Cost |
|------|------|
| Near-linear horizontal scalability on hot paths | Complex grid, replication, and partitioning infrastructure |
| Sub-ms reads and writes on in-memory state | Eventual durability — crash windows may lose recent writes |
| Eliminates database as the scaling bottleneck | Cold start and replay logic is non-trivial |
| Elastic — add/remove units under load | Working set must fit memory; large sets force partitioning |

## Implementation checklist

- [ ] Pick a data grid (Hazelcast, Ignite, Coherence) per consistency needs.
- [ ] Define partitioning keys and replication factor.
- [ ] Design data-writer async pipeline with replay-safe semantics.
- [ ] Design data-reader cold-start repopulation from DB.
- [ ] Budget memory per unit against working-set growth.
- [ ] Load-test failover — unit loss, grid rebalance, DB lag.
- [ ] Alert on grid health, replication lag, and memory pressure.

## See also

- [[pattern-event-driven-architecture]] — events frequently drive grid updates.
- [[pattern-cqrs]] — separate read/write models align well with grid-plus-DB.
- [[pattern-cache-aside]] — simpler alternative if DB reads are the only bottleneck.
