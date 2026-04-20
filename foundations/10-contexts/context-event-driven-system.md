---
id: context-event-driven-system
title: Event-Driven System
type: context
maturity: stable
tags: [context, stable, event-driven, messaging]
signals:
  - "Components communicate primarily via events or messages, not synchronous request-response"
  - "Services publish to or consume from queues, topics, or append-only streams"
  - "Eventual consistency is accepted or required across service boundaries"
  - "Order, delivery guarantees, and replay are first-class architectural concerns"
  - "Producers and consumers are decoupled in time, space, and availability"
recommended_patterns:
  - "[[pattern-event-driven-architecture]]"
  - "[[pattern-publish-subscribe]]"
  - "[[pattern-message-router]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-dead-letter-channel]]"
  - "[[pattern-event-sourcing]]"
  - "[[pattern-transactional-outbox]]"
  - "[[pattern-saga]]"
  - "[[pattern-async-request-reply]]"
  - "[[pattern-idempotency-key]]"
  - "[[pattern-correlation-id]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-circuit-breaker]]"
recommended_standards: []
common_antipatterns: []
related:
  - "[[context-web-application]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
sources:
  - "Enterprise Integration Patterns (Hohpe & Woolf, Addison-Wesley, 2003) — https://www.enterpriseintegrationpatterns.com/"
  - "Designing Event-Driven Systems (Stopford, O'Reilly, 2018)"
  - "What do you mean by Event-Driven? (Fowler, 2017) — https://martinfowler.com/articles/201701-event-driven.html"
  - "Designing Data-Intensive Applications (Kleppmann, O'Reilly, 2017) ch. 11 — https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/"
---

## Description

A system whose components communicate primarily via asynchronous events or messages rather than synchronous request-response. The defining shape is a flow of events through channels — queues, topics, or streams — with producers and consumers decoupled in time, space, and availability. Decisions are dominated by delivery guarantees, ordering, idempotency, and schema evolution. Event-driven is both an integration style between services and, in some systems, the source-of-truth mechanism via an append-only log.

## Key concerns

- **Delivery guarantees.** At-least-once is the norm; consumers must handle duplicates. Exactly-once is expensive and often infeasible.
- **Ordering.** Global ordering is usually impossible at scale; design for partition ordering or tolerate unordered.
- **Eventual consistency.** State across components converges over time; API contracts must state the staleness window honestly.
- **Poison messages.** Any consumer can encounter an event it cannot process. Dead-letter channels are non-optional.
- **Observability.** Tracing across async hops requires correlation IDs and structured logs; without them, incident diagnosis is guesswork.

## Typical architecture

- **Broker-centric** — services publish to and consume from a central broker (Kafka, RabbitMQ, SQS, Pub/Sub).
- **Log-based** — an append-only event log is the source of truth; consumers derive views. Often combined with event sourcing.
- **Choreography** — services react to each other's events with no central coordinator; end-to-end flow is implicit.
- **Orchestration** — a coordinator process drives a multi-step flow across services, typically via sagas.

## See also

- [[context-web-application]] — many modern web applications have async internals and straddle both contexts.
- [[context-data-pipeline]] — streaming pipelines specialise event-driven for bulk data movement.
- [[context-batch-processing]] — queue-backed events often trigger batch runs.
- [[dtree-choose-messaging-style]] — pick between sync RPC, async queue, pub-sub, and event streaming.
- [[dtree-choose-event-style]] — pick between event notification, event-carried state transfer, and event sourcing.
