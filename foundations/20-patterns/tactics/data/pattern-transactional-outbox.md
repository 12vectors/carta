---
id: pattern-transactional-outbox
title: Transactional Outbox
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, data, messaging, exactly-once]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-saga]]"
  - "[[pattern-event-sourcing]]"
  - "[[pattern-publish-subscribe]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://microservices.io/patterns/data/transactional-outbox.html"
  - "Microservices Patterns (Richardson, 2018) ch. 3"
---

## When to use

- A service must update its database AND publish a message atomically.
- You cannot tolerate silently dropped events when the broker is unavailable.
- Dual writes to DB and broker are already causing lost or duplicate events.
- Downstream consumers drive sagas, projections, or integrations.
- You need at-least-once delivery with a clear idempotency contract.

## When NOT to use

- No messaging involved — single-service CRUD.
- Fire-and-forget notifications where loss is acceptable.
- When the datastore natively supports change data capture and CDC is already in place and sufficient.
- Systems that require strict exactly-once without consumer-side idempotency.

## Decision inputs

- Volume of outbox rows per second and retention window.
- Relay mechanism — polling publisher or log-tailing (CDC).
- Ordering requirements per aggregate or partition key.
- Idempotency contract with consumers (message ID, dedup window).
- Cleanup policy for published rows (delete, archive, TTL).

## Solution sketch

In the same local transaction as the state change, insert a row into an `outbox` table describing the event to publish. A separate relay process reads unpublished rows and publishes them to the broker, marking each as sent (or deleting it) after acknowledgement. Crash between state change and relay is safe — the row is still there.

```
BEGIN TX
  UPDATE orders SET status='paid' WHERE id=...;
  INSERT INTO outbox (id, topic, payload, created_at) VALUES (...);
COMMIT

[Relay] -- poll / CDC --> [Broker] -- consumers
```

Two relay styles: **polling** (simple, adds DB load) and **transaction-log tailing** via CDC (Debezium-style, lower latency, more moving parts). Either way, consumers must deduplicate by message ID — delivery is at-least-once.

## Trade-offs

| Gain | Cost |
|------|------|
| Atomic state-change + event publish without XA | Extra table, relay process, and dedup on consumer side |
| Survives broker outages — events catch up on recovery | Outbox table can grow; needs cleanup and monitoring |
| Works with any SQL store; well-understood operationally | At-least-once delivery shifts idempotency burden downstream |
| Clear audit of what was published, in what order | Polling adds DB load; CDC adds infra and permissions |

## Implementation checklist

- [ ] Add an `outbox` table with message ID, topic, payload, status/timestamps.
- [ ] Write to `outbox` inside the same transaction as the business state change.
- [ ] Choose polling vs. CDC relay; document the trade-off.
- [ ] Include a stable message ID for consumer-side deduplication.
- [ ] Preserve per-partition order (aggregate ID as key) through the relay.
- [ ] Mark or delete rows only after broker ack; retry on failure.
- [ ] Monitor outbox lag, relay health, and table size.
- [ ] Document retention and cleanup (TTL, archive, or delete on publish).

## See also

- [[pattern-saga]] — publishes saga step events reliably.
- [[pattern-event-sourcing]] — alternative when the event log is the source of truth.
- [[pattern-publish-subscribe]] — the delivery mechanism downstream.
- [[pattern-idempotency-key]] — consumer-side dedup contract.
