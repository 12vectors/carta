---
id: pattern-read-replica
title: Read Replica
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, data, replication, read-scaling]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-cqrs]]"
  - "[[pattern-materialized-view]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Designing Data-Intensive Applications (Kleppmann, O'Reilly, 2017) ch. 5 — https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/"
---

## When to use

- Read throughput saturates the primary while writes are fine.
- Queries tolerate replication lag of milliseconds to seconds.
- Reporting, search, or analytics queries must not impact OLTP.
- You need a warm standby for failover and also want to use it for reads.
- Geographic read latency matters and replicas can live near users.

## When NOT to use

- Write-heavy workloads — replicas don't help writes.
- Every query needs read-your-writes — overhead of routing outweighs gains.
- Small datasets where a bigger primary is cheaper and simpler.
- Consistency model of the primary already chokes on write volume (shard instead).

## Decision inputs

- Read/write ratio and peak read QPS.
- Acceptable replication lag per query class.
- Failover expectations (RPO/RTO) and promotion procedure.
- Routing strategy — application-level, proxy, or driver-level.
- Geographic distribution of readers.

## Solution sketch

Primary accepts all writes and streams its change log (WAL, binlog, oplog) to one or more replicas that apply changes asynchronously. Reads are routed to replicas; writes always to the primary. Route queries that require read-your-writes back to the primary, or pin the session to the primary for a short window after a write.

```
         writes
[Client] -------> [Primary] -- WAL/binlog --> [Replica 1]
                                         \--> [Replica 2]
         reads
[Client] --> [Proxy / router] --> [Replica N]
```

Monitor replication lag and fence reads off lagging replicas. For failover, promote a replica; accept the RPO implied by async replication, or use synchronous/quorum replication where the write latency budget allows.

## Trade-offs

| Gain | Cost |
|------|------|
| Linear read scaling by adding replicas | Writes don't scale; primary remains the bottleneck |
| Isolates reporting load from OLTP | Replication lag breaks read-your-writes expectations |
| Warm standby doubles as capacity and DR | Async replication means non-zero RPO on failover |
| Cross-region replicas cut user-perceived latency | Operational complexity — routing, lag monitoring, promotion |

## Implementation checklist

- [ ] Measure read/write ratio and current primary saturation.
- [ ] Provision replicas with identical hardware and config.
- [ ] Set up a routing layer (proxy, driver, or app-level).
- [ ] Classify queries by lag tolerance; route accordingly.
- [ ] Implement read-your-writes escape hatch (primary pin, session consistency).
- [ ] Monitor replication lag per replica and alert above threshold.
- [ ] Document and rehearse failover promotion.
- [ ] Load-test at N-1 replicas to confirm capacity under replica loss.

## See also

- [[pattern-cqrs]] — when divergent read/write models justify more than replicas.
- [[pattern-materialized-view]] — when query-shaped reads beat 1:1 replication.
- [[pattern-sharding]] — when writes, not reads, are the bottleneck.
- [[pattern-cache-aside]] — complementary for hot read paths.
