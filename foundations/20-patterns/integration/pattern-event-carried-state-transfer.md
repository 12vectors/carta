---
id: pattern-event-carried-state-transfer
title: Event-Carried State Transfer
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, messaging, events, state, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-event-notification]]"
  - "[[pattern-event-sourcing]]"
conflicts_with: []
contradicted_by:
  - "[[pattern-event-notification]]"
sources:
  - "What do you mean by 'Event-Driven'? (Fowler, 2017) — https://martinfowler.com/articles/201701-event-driven.html"
---

## When to use

- Consumers need to act without calling back to the producer.
- Producer availability should not gate consumer throughput.
- Cross-service read models or local projections reduce cross-team coupling.
- Reducing chatty request-response traffic between services.
- High-latency or cross-region consumers need locality for reads.

## When NOT to use

- Payloads are very large — fan-out cost is prohibitive (consider claim check).
- Strong consistency is required — local copies will be stale.
- Fields are sensitive and shipping them widens the data-exposure surface.
- Producer's schema changes frequently — propagation cost is high.

## Decision inputs

- Payload size and fan-out ratio (subscribers × events/sec × bytes).
- Staleness tolerance at the consumer.
- Schema-evolution strategy — backward/forward compatibility rules.
- Data classification (PII, regulated) vs subscriber access scope.
- Replay requirements — rebuilding read models from the log.
- Storage cost at consumers maintaining local projections.

## Solution sketch

Publish events that carry **enough state** for consumers to act locally without calling back. Consumers project the stream into their own read models.

```
[Producer] --event{id, full state}--> [Topic] --> [Consumer projects into local store]
```

- Payload is the **subset of state** the consumer domain needs — not necessarily the whole aggregate.
- Use a **schema registry** (Avro, Protobuf, JSON Schema) with compatibility rules.
- Consumers maintain **idempotent projections** — apply the same event twice is safe.
- Log-based broker (Kafka) enables late joiners to backfill via replay.
- Treat events as a contract — document semantics, not just fields.

## Trade-offs

| Gain | Cost |
|------|------|
| Consumers decoupled from producer availability | Larger events; more broker and network cost |
| Local reads are fast and scale independently | Multiple copies of data — eventual consistency by design |
| Enables cross-service read models and projections | Schema changes must preserve compatibility or break consumers |
| Replay rebuilds consumers from scratch | Regulated data now lives in more places — broader exposure |

## Implementation checklist

- [ ] Define the event schema as a versioned contract in a registry.
- [ ] Enforce backward-compatible evolution; deprecate fields, do not remove.
- [ ] Make consumer projections idempotent — see `[[pattern-idempotency-key]]`.
- [ ] Use a log-based broker if replay or late-joiner backfill is needed.
- [ ] Classify data; restrict topics carrying regulated or sensitive state.
- [ ] Document on each topic: state-transfer vs notification — pick one.
- [ ] Monitor consumer lag and projection freshness, not just broker depth.
- [ ] Test schema upgrades with both old and new consumers running.

## See also

- [[pattern-event-notification]] — lightweight alternative; consumer calls back for data.
- [[pattern-event-sourcing]] — state-transfer events are often produced from a sourced log.
- [[pattern-publish-subscribe]] — delivery mechanism; log-based preferred for replay.
- [[pattern-claim-check]] — when the state is too large to carry inline.
