---
id: dtree-choose-data-access
title: Choose a Read-Path Data Access Strategy
type: decision-tree
maturity: stable
tags: [decision-tree, stable, data, caching, performance]
decides_between:
  - "[[pattern-cache-aside]]"
  - "[[pattern-read-replica]]"
  - "[[pattern-materialized-view]]"
  - "[[pattern-cqrs]]"
criteria:
  - "Query shape (point reads vs. range scans vs. aggregations)"
  - "Read/write ratio"
  - "Staleness tolerance"
  - "Write path under control (or read-path-only change)"
  - "Consistency mode (strong vs. read-your-writes vs. eventual)"
related_patterns:
  - "[[pattern-sharding]]"
  - "[[pattern-event-sourcing]]"
---

## Problem

Reads dominate the workload, and the primary store is struggling or would be cheaper relieved. Pick a read-scaling strategy appropriate to the shape of the query and the tolerable staleness.

## Criteria

- **Query shape** — same rows by key / range scans / aggregations across many rows?
- **Read/write ratio** — 10× reads / 100× reads / 1000× reads per write?
- **Staleness tolerance** — must be live / seconds is fine / minutes is fine?
- **Write path touch** — can the write path be changed, or is only the read path under control?
- **Consistency mode** — strongly consistent / read-your-writes / eventually consistent?

## Recommendation

| Situation | Choose |
|---|---|
| Hot keys, point reads, seconds-to-minutes staleness OK, write path untouched | [[pattern-cache-aside]] |
| Mixed query shapes against a relational store, minutes-of-replica-lag OK | [[pattern-read-replica]] |
| Aggregation or join-heavy reads, can afford to precompute | [[pattern-materialized-view]] |
| Read shape diverges structurally from write shape, both high volume | [[pattern-cqrs]] |
| Primary store itself is the bottleneck, not just read load | [[pattern-sharding]] on the primary |
| Need full event history and ability to rebuild views | [[pattern-event-sourcing]] as the backbone |

These compose: cache-aside sits in front of a read replica; a materialized view can feed a cache; CQRS often pairs with event-sourcing.

## Fallback

Default to cache-aside. Lowest-commitment, easiest to measure and roll back, non-invasive. Add read replicas next if write-master CPU is the limit. Move to materialized views or CQRS only when the read shape genuinely differs from the write shape — not because reads are slow.
