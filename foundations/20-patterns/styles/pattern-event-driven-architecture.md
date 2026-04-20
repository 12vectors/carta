---
id: pattern-event-driven-architecture
title: Event-Driven Architecture
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-performance]]"
tags: [pattern, stable, style, async, messaging, decoupled]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-microservices]]"
  - "[[pattern-space-based-architecture]]"
  - "[[pattern-pipeline]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Software Architecture Patterns (Richards, 2015) ch. 2"
  - "https://martinfowler.com/articles/201701-event-driven.html"
---

## When to use

- High-throughput, asynchronous workflows — orders, telemetry, notifications, ingest.
- Systems where producers and consumers evolve independently.
- Domains with many reactions per event (fan-out) or many sources per reaction (fan-in).
- Workflows tolerating eventual consistency and out-of-order delivery.

## When NOT to use

- Strong-consistency, synchronous request/response domains.
- Teams without tracing, replay, and DLQ tooling for async debugging.
- Simple CRUD where events add infrastructure without behaviour.
- Workflows requiring guaranteed linear ordering across many partitions.

## Decision inputs

- Event taxonomy — notification, event-carried state, or event-sourced.
- Broker semantics (ordering, delivery, retention, partitioning).
- Schema governance and evolution strategy.
- Consumer idempotency — duplicates and replays are expected.
- Topology — mediator (orchestrated) vs broker (choreographed).

## Solution sketch

Components communicate by producing and consuming **events** through a broker. Two common topologies per Richards: **broker topology** (choreography — consumers react independently) and **mediator topology** (orchestration — a workflow engine sequences steps).

```
[producer] --event--> [ broker / topic ] --event--> [consumer A]
                                        \---------> [consumer B]
```

Distinguish Fowler's four EDA flavours (notification, state transfer, sourcing, CQRS) — each has different coupling and storage implications. See Fowler (linked) for the taxonomy.

## Trade-offs

| Gain | Cost |
|------|------|
| Producers and consumers decouple in time and team | Debugging and reasoning about flows is harder |
| Natural fan-out, buffering, and back-pressure | Eventual consistency complicates UX and invariants |
| Resilience — broker absorbs consumer outages | Broker becomes a critical shared dependency |
| Scales by partitioning topics and consumers | Schema evolution and idempotency are permanent concerns |

## Implementation checklist

- [ ] Pick topology (broker vs mediator) per workflow.
- [ ] Define event schemas and a compatibility policy.
- [ ] Make every consumer idempotent (see [[pattern-idempotency-key]]).
- [ ] Configure DLQs and replay tooling.
- [ ] Propagate correlation IDs across events.
- [ ] Monitor consumer lag, broker health, and DLQ depth.
- [ ] Document ordering and delivery guarantees per topic.

## See also

- [[pattern-microservices]] — events are the default inter-service backbone.
- [[pattern-space-based-architecture]] — events often drive replicated in-memory state.
- [[pattern-pipeline]] — pipelines frequently run on event infrastructure.
- [[pattern-event-sourcing]] — stronger variant where events are the source of truth.
