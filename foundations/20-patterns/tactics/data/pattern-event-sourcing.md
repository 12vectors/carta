---
id: pattern-event-sourcing
title: Event Sourcing
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, data, event-sourcing, audit]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-cqrs]]"
  - "[[pattern-saga]]"
  - "[[pattern-transactional-outbox]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://martinfowler.com/eaaDev/EventSourcing.html"
---

## When to use

- Audit trail and full history are first-class business requirements.
- You need to reconstruct past state or replay "what if" scenarios.
- Domain is naturally expressed as a sequence of facts (orders, ledgers, workflows).
- Multiple read models must derive from the same authoritative stream.
- Temporal queries ("state as of X") are a recurring need.

## When NOT to use

- Simple CRUD where current state is all anyone ever needs.
- Teams without experience in eventual consistency and replay mechanics.
- Domains where events lack stable semantics and will churn.
- Strict regulatory requirements for in-place deletion (GDPR erasure without crypto-shredding plan).

## Decision inputs

- Event granularity — one per user intent, not one per field change.
- Retention policy, snapshotting cadence, and storage growth rate.
- Schema-evolution strategy (upcasters, versioned events).
- Consistency boundary — the aggregate whose events form an atomic stream.
- PII handling: crypto-shredding, tombstones, or avoidance.

## Solution sketch

Persist every state change as an immutable event appended to a per-aggregate stream. Current state is derived by folding events; snapshots cache the fold at checkpoints. Commands load the aggregate (replay + snapshot), validate, and append new events atomically with optimistic concurrency on stream version. Readers subscribe to the stream to build projections.

```
[Command] --> [Load aggregate: snapshot + events] --> [Decide] --> [Append events@version] --> [Subscribers/projections]
```

Event schemas evolve via upcasters or versioned event types — never by rewriting history. Pair with CQRS for query-shaped read models; pair with outbox or a log-based store to reliably publish events downstream.

## Trade-offs

| Gain | Cost |
|------|------|
| Complete, immutable audit trail by construction | Every schema change requires upcasters or replays |
| Rebuild any projection from source of truth | Event storage grows monotonically; snapshotting required |
| Temporal queries and replay for debugging | Eventual consistency on read side |
| Natural fit with event-driven integration | PII erasure and GDPR require deliberate design |

## Implementation checklist

- [ ] Define aggregates and their event streams explicitly.
- [ ] Choose an event store (EventStoreDB, Kafka with compaction, append-only table).
- [ ] Enforce optimistic concurrency on stream version at append.
- [ ] Design events around business intent, not table diffs.
- [ ] Implement snapshotting with a documented cadence.
- [ ] Plan schema evolution (upcasters, versioning) before v2.
- [ ] Address PII: crypto-shredding keys or keep PII out of events.
- [ ] Monitor stream growth, projection lag, and replay time.

## See also

- [[pattern-cqrs]] — read models derived from the event stream.
- [[pattern-saga]] — long-running processes orchestrated by events.
- [[pattern-transactional-outbox]] — simpler alternative when you only need to publish events, not rebuild state.
- [[pattern-materialized-view]] — typical shape of event-sourced read models.
