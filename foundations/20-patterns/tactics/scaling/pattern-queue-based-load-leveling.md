---
id: pattern-queue-based-load-leveling
title: Queue-Based Load Leveling
type: pattern
category: scaling
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-cost]]"
tags: [pattern, stable, scaling, queue, load-leveling, async]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-throttling]]"
  - "[[pattern-rate-limiting]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-publish-subscribe]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling"
---

## When to use

- Producer traffic is spiky; downstream service has fixed or slow-scaling capacity.
- Work is async-tolerable — caller does not need an immediate synchronous result.
- Protecting an expensive tier (DB, ML inference, third-party API) from overload.
- Batch, ETL, email, webhook dispatch, or notification pipelines.
- Smoothing cost: size consumers for steady-state, not peak.

## When NOT to use

- Request-response flows where callers need a synchronous answer inside one RTT.
- Sub-second end-to-end latency SLOs that cannot tolerate queueing.
- Workloads already uniform — queue adds complexity with no levelling benefit.
- When backpressure to the producer is the desired behaviour (use rate limiting instead).

## Decision inputs

- Peak-to-average ratio — higher ratios justify a queue.
- Acceptable end-to-end latency budget including queue dwell time.
- Message durability requirement (at-least-once, exactly-once, ordered).
- Consumer concurrency model and idempotency guarantees.
- Dead-letter strategy and max retry count.
- Queue depth alerting thresholds.

## Solution sketch

Insert a durable queue between producer and consumer. Producers enqueue and return fast; consumers pull at their own pace.

```
[Producer] --enqueue--> [Queue] --pull--> [Consumer pool]
                          |
                          +--> [Dead-letter queue]
```

- Consumers scale on **queue depth** or **age of oldest message**, not producer RPS.
- Make handlers **idempotent** — retries and redelivery are the norm.
- Bound retries; route poison messages to a DLQ with alerting.
- Cap queue depth or TTL messages to prevent unbounded backlog.

See Azure pattern for capacity-planning formulas. Pair with competing-consumers for horizontal worker scale.

## Trade-offs

| Gain | Cost |
|------|------|
| Smooths spikes; consumer sized for mean, not peak | Adds latency — sync UX becomes async |
| Protects downstream tiers from overload | Extra infrastructure to operate (queue, DLQ, monitoring) |
| Decouples producer/consumer deploy cycles | Requires idempotent consumers and duplicate handling |
| Natural retry boundary on consumer failure | Queue backlog hides problems until SLO breach |
| Consumers autoscale on depth → cost efficiency | Ordering and exactly-once are hard; most queues are at-least-once |

## Implementation checklist

- [ ] Pick queue technology matched to durability and ordering needs (SQS, Kafka, RabbitMQ, PubSub).
- [ ] Make every consumer handler idempotent — see `[[pattern-idempotency-key]]`.
- [ ] Configure visibility timeout ≥ p99 handler time.
- [ ] Set max-receive count and route to DLQ.
- [ ] Alert on queue depth, oldest-message age, and DLQ arrival.
- [ ] Autoscale consumers on depth/age, not CPU.
- [ ] Define TTL or max depth to cap unbounded growth.
- [ ] Load-test spike-then-drain; verify consumer catch-up time.

## See also

- [[pattern-competing-consumers]] — how to scale consumer throughput horizontally.
- [[pattern-publish-subscribe]] — fan-out counterpart when multiple consumers need each message.
- [[pattern-throttling]] — caps work at the boundary; queue absorbs what it allows through.
- [[pattern-rate-limiting]] — rejects excess producer traffic; queue buffers accepted traffic.
