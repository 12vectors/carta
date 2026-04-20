---
id: pattern-publish-subscribe
title: Publish-Subscribe Channel
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, messaging, pubsub, fan-out, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-message-router]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-event-notification]]"
  - "[[pattern-event-carried-state-transfer]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Enterprise Integration Patterns (Hohpe & Woolf, Addison-Wesley, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/PublishSubscribeChannel.html"
---

## When to use

- Multiple independent consumers must each receive a copy of every message.
- Producer must not know consumer identities or count — loose coupling is the goal.
- New consumers should be able to subscribe without changing the publisher.
- Fan-out for notifications, cache invalidations, audit trails, projections.
- Event-driven architectures where one state change triggers many reactions.

## When NOT to use

- Exactly one worker should handle each message (use competing consumers).
- Producer needs a synchronous reply per message (use request-reply).
- Strict ordering across all consumers matters more than delivery independence.
- Payload too large to replicate cheaply — use claim check first.

## Decision inputs

- Subscriber count and churn rate — topic-per-event vs dynamic filters.
- Delivery semantics: at-least-once vs at-most-once; per-subscriber retry.
- Retention and replay requirements (Kafka-style log vs broker fan-out).
- Message ordering scope — per key, per partition, or none.
- Subscriber isolation — one slow consumer must not block others.
- Schema evolution strategy for long-lived topics.

## Solution sketch

Publisher sends to a **topic**; broker delivers a copy to each subscribed **consumer**. Publisher has no reference to subscribers. Each subscriber has its own offset/cursor and its own dead-letter path.

```
                    +--> [Subscriber A]
[Publisher] -> [Topic] --> [Subscriber B]
                    +--> [Subscriber C]
```

- Two families: **broker fan-out** (SNS, RabbitMQ exchange) — push, no replay; **log-based** (Kafka, Pulsar) — pull, replay via offset.
- Each subscriber handles its own failures; one slow subscriber does not stall others.
- Versioned schemas — never break existing subscribers.
- Decide event style up front: notification (pointer) or carried-state.

## Trade-offs

| Gain | Cost |
|------|------|
| Loose coupling — producer ignorant of consumers | Harder to reason about global flow; fan-out is implicit |
| New subscribers without publisher changes | Per-subscriber backlog, DLQ, and monitoring to operate |
| Independent consumer scaling and failure domains | Duplicate delivery is the norm — handlers must be idempotent |
| Replay (log-based) enables reprocessing and new consumers | Schema changes ripple across all subscribers |

## Implementation checklist

- [ ] Pick broker style: fan-out (SNS, RabbitMQ) or log (Kafka, Pulsar) based on replay needs.
- [ ] Define topic naming convention and ownership.
- [ ] Publish versioned event schemas; gate with a schema registry.
- [ ] Make every subscriber idempotent — see `[[pattern-idempotency-key]]`.
- [ ] Per-subscriber DLQ and alerting on lag/age.
- [ ] Document event as notification or state-transfer; do not mix silently.
- [ ] Load-test fan-out at peak subscriber count.
- [ ] Plan schema evolution and deprecation process.

## See also

- [[pattern-competing-consumers]] — opposite shape; one message, one worker.
- [[pattern-message-router]] — subscribe one logical consumer, then route internally.
- [[pattern-event-notification]] — lightweight event style; subscribers call back for data.
- [[pattern-event-carried-state-transfer]] — heavy event style; subscribers need no callback.
- [[pattern-claim-check]] — when payloads are too large to fan out directly.
