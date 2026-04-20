---
id: context-event-driven-system
title: Event-Driven System
type: context
maturity: stable
tags: [context, stable, event-driven]
signals:
  - "Communication between components is primarily via events or messages, not request-response"
  - "Components publish or consume from queues, topics, or streams"
  - "Eventual consistency is accepted or required across components"
  - "Order, delivery guarantees, and replay are first-class architectural concerns"
recommended_patterns:
  - "[[pattern-event-driven-architecture]]"
  - "[[pattern-publish-subscribe]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-dead-letter-channel]]"
  - "[[pattern-event-sourcing]]"
  - "[[pattern-transactional-outbox]]"
  - "[[pattern-correlation-id]]"
recommended_standards: []
common_antipatterns: []
related:
  - "[[context-web-application]]"
sources:
  - "Enterprise Integration Patterns (Hohpe & Woolf, Addison-Wesley, 2003) — https://www.enterpriseintegrationpatterns.com/"
  - "Designing Event-Driven Systems (Stopford, O'Reilly, 2018)"
---

## Description

A system whose components communicate primarily via asynchronous events or messages rather than synchronous request-response. The defining shape is a flow of events through channels — queues, topics, or streams — with producers and consumers decoupled in time, space, and availability.

## Key concerns

- **Delivery guarantees.** At-least-once is the norm; consumers must handle duplicates. Exactly-once is expensive and often infeasible.
- **Ordering.** Global ordering is usually impossible at scale; design for partition ordering or tolerate unordered.
- **Eventual consistency.** State across components converges over time; API contracts must state the staleness window honestly.
- **Poison messages.** Any consumer can encounter an event it cannot process. Dead-letter channels are non-optional.
- **Observability.** Tracing across async hops requires correlation IDs and structured logs; without them, incident diagnosis is guesswork.

## Typical architecture

- **Broker-centric** — services publish to and consume from a central broker (Kafka, RabbitMQ, SQS, Pub/Sub).
- **Log-based** — an append-only event log is the source of truth; consumers derive views. Often combined with event sourcing.
- **Choreography** — services react to each other's events with no central coordinator.
- **Orchestration** — a coordinator process drives the sequence across services (often via sagas).

## See also

- [[context-web-application]] — many modern web applications have async internals and straddle both contexts.
- [[dtree-choose-messaging-style]] — pick between sync RPC, async queue, pub-sub, and event streaming.
- [[dtree-choose-event-style]] — pick between event notification, event-carried state transfer, and event sourcing.
