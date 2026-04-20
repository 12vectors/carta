---
id: pattern-sharding
title: Sharding
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-performance]]"
tags: [pattern, stable, data, partitioning, horizontal-scaling]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-read-replica]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Designing Data-Intensive Applications (Kleppmann, 2017) ch. 6 — https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/"
---

## When to use

- Dataset or write throughput exceeds what a single node can hold or serve.
- A natural partition key exists (tenant, user, region) with even distribution.
- Most queries can be answered within a single shard.
- Read replicas alone have stopped solving the bottleneck.
- You accept the operational cost of running a distributed store.

## When NOT to use

- Data fits comfortably on one node with headroom to grow.
- No partition key gives even load — hot shards will form.
- Workload is dominated by cross-shard joins or global aggregates.
- Team lacks experience with rebalancing, resharding, and distributed ops.

## Decision inputs

- Shard key — what partitions the data and most queries.
- Strategy — range, hash, directory, or consistent hashing.
- Rebalancing approach when shards grow uneven or nodes change.
- Cross-shard query policy (scatter-gather, denormalise, forbid).
- Transaction scope — single-shard only, or distributed with a coordinator.

## Solution sketch

Split the dataset across N nodes by a shard key. A router (in the client, a proxy, or the database itself) maps each request to the shard(s) holding the relevant data. Writes and most reads touch exactly one shard. Cross-shard queries require scatter-gather or a separate read model.

```
            shard_key=hash(user_id) % N
[Client] -> [Router] -> [Shard 0] [Shard 1] [Shard 2] ... [Shard N-1]
```

Strategies: **range** (good for range scans, prone to hotspots), **hash** (even distribution, bad for range scans), **consistent hashing** (minimises movement on resize), **directory** (flexible, adds a lookup hop). Plan rebalancing from day one — online resharding is the hard part.

## Trade-offs

| Gain | Cost |
|------|------|
| Horizontal scale for writes and dataset size | Shard key choice is hard to change later |
| Failure blast radius limited to one shard | Cross-shard queries and transactions are expensive or forbidden |
| Per-shard operations remain fast as data grows | Hot shards appear if the key distributes unevenly |
| Regional sharding enables data residency | Rebalancing and resharding are operationally painful |

## Implementation checklist

- [ ] Choose a shard key based on query patterns and load distribution.
- [ ] Pick a strategy (hash, range, consistent hashing, directory) with justification.
- [ ] Design the router layer (client, proxy, or DB-native).
- [ ] Decide cross-shard query policy; build scatter-gather only if needed.
- [ ] Constrain transactions to a single shard where possible.
- [ ] Plan and test a rebalancing / resharding procedure before you need it.
- [ ] Monitor per-shard load, size, and latency; alert on skew.
- [ ] Document the shard map as code, not tribal knowledge.

## See also

- [[pattern-read-replica]] — try first if reads are the bottleneck, not writes.
- [[pattern-database-per-service]] — a coarse form of sharding by service.
- [[pattern-cache-aside]] — reduces per-shard read load.
- [[pattern-materialized-view]] — answers cross-shard queries without scatter-gather.
