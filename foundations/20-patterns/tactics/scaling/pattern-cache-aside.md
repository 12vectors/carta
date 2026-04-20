---
id: pattern-cache-aside
title: Cache-Aside
type: pattern
category: scaling
maturity: stable
pillars:
  - "[[pillar-performance]]"
tags: [pattern, stable, scaling, caching, read-optimization]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-materialized-view]]"
  - "[[pattern-read-replica]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside"
---

## When to use

- Read-heavy workloads where the same records are fetched repeatedly.
- Expensive reads: joins, aggregations, remote API calls, slow ORMs.
- Tolerant of bounded staleness (seconds to minutes).
- When source-of-truth writes are infrequent relative to reads.
- When a miss-then-fetch latency spike is acceptable for cold keys.

## When NOT to use

- Strong-consistency requirements (financial ledgers, inventory decrements).
- Write-heavy keys where invalidation churn erases the hit-rate gain.
- Tiny or already in-memory datasets — the cache is pure overhead.
- When per-request data is unique (high cardinality, no reuse).

## Decision inputs

- Read/write ratio and hit-rate target (≥80% usually required to pay off).
- Acceptable staleness window — drives TTL.
- Invalidation strategy on write (delete, write-through, write-behind).
- Key design and cardinality; avoid unbounded keyspaces.
- Cache sizing, eviction policy (LRU, LFU), and stampede protection.

## Solution sketch

Application owns the cache logic; cache is a side-store.

```
read(k):
  v = cache.get(k)
  if v is None:
    v = db.get(k)
    cache.set(k, v, ttl)
  return v

write(k, v):
  db.put(k, v)
  cache.delete(k)   # or cache.set(k, v, ttl)
```

- **TTL** bounds staleness even if invalidation is missed.
- **Delete on write** beats update-on-write (avoids two-writer races).
- Guard against **stampede**: single-flight, jittered TTL, or probabilistic early expiry.
- Negative caching for not-found keys prevents repeated DB lookups.

See Microsoft Azure pattern for detail on consistency trade-offs.

## Trade-offs

| Gain | Cost |
|------|------|
| Large latency and DB-load reduction for hot reads | Staleness: reads can lag writes by up to TTL |
| Simple to bolt on — app-owned, no ORM changes | Cache-stampede risk on popular cold keys |
| Survives cache outage (fall back to DB) | DB must be sized to handle cache-cold traffic |
| Fine-grained per-key TTLs | Invalidation bugs surface as user-visible staleness |
| Works with any cache (Redis, Memcached, in-proc) | Cache and DB drift silently without observability |

## Implementation checklist

- [ ] Define TTL per key class based on staleness budget.
- [ ] Invalidate (delete) on every write path — in the same transaction where possible.
- [ ] Use single-flight or request coalescing for hot keys.
- [ ] Add jitter to TTL to avoid synchronised expiry stampedes.
- [ ] Cache negatives with short TTL to blunt 404 scans.
- [ ] Emit hit rate, miss rate, and eviction metrics per key class.
- [ ] Alert when hit rate drops below target — indicates key design or TTL regression.
- [ ] Load-test cold-cache scenarios; verify DB can absorb the traffic.

## See also

- [[pattern-materialized-view]] — precomputed alternative for complex reads.
- [[pattern-read-replica]] — scale reads at the DB layer instead of, or with, caching.
- [[pattern-circuit-breaker]] — wrap cache calls to fail over to the source of truth.
