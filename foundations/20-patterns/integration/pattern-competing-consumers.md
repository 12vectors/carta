---
id: pattern-competing-consumers
title: Competing Consumers
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, messaging, scaling, concurrency, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-queue-based-load-leveling]]"
  - "[[pattern-publish-subscribe]]"
  - "[[pattern-priority-queue]]"
conflicts_with: []
contradicted_by: []
sources:
  - "EIP (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/CompetingConsumers.html"
---

## When to use

- Work items are independent and can run in parallel on any worker.
- Throughput must scale horizontally by adding worker instances.
- Single-consumer throughput is the bottleneck, not producer rate.
- Failure of one worker should not block or lose pending work.
- Each message must be processed exactly once across the pool.

## When NOT to use

- Every subscriber must see every message (use publish-subscribe).
- Strict global ordering is required — use a single consumer or per-key partitioning.
- Work is very short and per-message overhead dominates — batch first.
- Handlers cannot be made idempotent and redelivery would corrupt state.

## Decision inputs

- Per-message processing time distribution (mean, p95, p99).
- Ordering scope required — none, per-key, or per-partition.
- Visibility timeout vs handler p99 — must cover slow-path runs.
- Idempotency guarantees — at-least-once requires dedupe.
- Autoscaling signal — queue depth, oldest-message age, or CPU.
- Poison-message strategy and DLQ thresholds.

## Solution sketch

A pool of identical consumers pulls from one shared queue. The broker delivers each message to exactly one consumer at a time; scale is a matter of adding workers.

```
              +-> [Worker 1] -+
[Queue] ------+-> [Worker 2] -+-> [Downstream]
              +-> [Worker N] -+
```

- **At-least-once** is the default — design handlers to be idempotent.
- **Visibility timeout** must exceed worker p99 processing time to avoid duplicate delivery.
- For per-key ordering, partition the queue (Kafka) or use message-group IDs (SQS FIFO).
- Autoscale on **depth** or **oldest-age**, not CPU — RPS lies about backlog.
- Always pair with a DLQ — poison messages must not loop forever.

## Trade-offs

| Gain | Cost |
|------|------|
| Horizontal throughput by adding workers | Loses global ordering unless partitioned |
| Failure of one worker does not block others | Requires idempotent handlers — redelivery is normal |
| Natural load balancing via pull model | Visibility-timeout tuning is fragile; mis-tuning causes duplicates |
| Autoscaling on backlog is simple and effective | Tail latency can spike if backlog grows faster than scale-out |

## Implementation checklist

- [ ] Make every handler idempotent — see `[[pattern-idempotency-key]]`.
- [ ] Set visibility timeout ≥ handler p99 plus safety margin.
- [ ] Configure max-receive count and a per-queue DLQ.
- [ ] Autoscale on queue depth or oldest-message age.
- [ ] Partition (Kafka) or use message groups (SQS FIFO) if per-key ordering matters.
- [ ] Alert on DLQ arrival, backlog growth, and oldest-message age.
- [ ] Load-test concurrency; verify no duplicate side effects.
- [ ] Graceful-shutdown: finish in-flight messages before exit.

## See also

- [[pattern-queue-based-load-leveling]] — queue upstream protects the consumer pool.
- [[pattern-publish-subscribe]] — opposite shape; one message, many consumers.
- [[pattern-dead-letter-channel]] — essential companion for poison-message handling.
- [[pattern-priority-queue]] — when some messages deserve faster consumption.
