---
id: pattern-event-notification
title: Event Notification
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, messaging, events, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-event-carried-state-transfer]]"
  - "[[pattern-publish-subscribe]]"
conflicts_with: []
contradicted_by:
  - "[[pattern-event-carried-state-transfer]]"
sources:
  - "What do you mean by 'Event-Driven'? (Fowler, 2017) — https://martinfowler.com/articles/201701-event-driven.html"
---

## When to use

- Producer signals "something happened" with identity but minimal data.
- Consumers that care already have access to authoritative source data.
- Events are small, high-volume, and replay is cheap.
- Source-of-truth must remain the producer; no local replicas wanted.
- Subscribers vary in what fields they need — best to let them ask.

## When NOT to use

- Consumers cannot afford a synchronous callback to the producer.
- Producer may be unavailable when consumers process events (use state transfer).
- Callback storm would overload the producer under fan-out.
- Consumers need historical state snapshot — notifications alone do not carry it.

## Decision inputs

- Producer capacity to serve callback reads under peak subscriber load.
- Acceptable latency for callback-fetch after event delivery.
- Security: are callbacks allowed across trust boundaries?
- Consistency window — is stale-read after event tolerable?
- Subscriber count growth projection (callback load is linear with consumers).
- Ownership of the canonical record — must remain with the producer.

## Solution sketch

Publish a lightweight event carrying **only an identifier and event type** (plus trace metadata). Interested consumers fetch the full state from the producer when — and if — they need it.

```
[Producer] --event{id, type}--> [Topic] --> [Consumer] --GET /resource/id--> [Producer]
```

- Event payload: `id`, `type`, `occurredAt`, `correlationId` — nothing more.
- Consumer decides whether to call back; many events require no action.
- Producer must serve a stable read API keyed on the identifier.
- Idempotent consumers — duplicate events are cheap because the payload is tiny.
- **Not the same** as event-carried state transfer; do not mix silently on one topic.

## Trade-offs

| Gain | Cost |
|------|------|
| Minimal payload; cheap to publish and fan out | Consumers must call back — producer becomes a hotspot |
| Single source of truth stays with the producer | Adds latency for consumers that always need the data |
| Easy to evolve — payload is just identity | Producer availability blocks all consumer work |
| Works across trust boundaries with simple schema | Callback storm under high subscriber count |

## Implementation checklist

- [ ] Keep event payload to identity + type + timestamps + correlation id.
- [ ] Provide a stable, idempotent read API keyed on the event identifier.
- [ ] Cache responses on the consumer side where staleness is acceptable.
- [ ] Size producer for peak callback load, not just publish load.
- [ ] Document on each topic: notification vs state-transfer — pick one.
- [ ] Include trace IDs in every event for end-to-end correlation.
- [ ] Alert on callback error rate and producer latency under event bursts.
- [ ] Consider a circuit breaker for consumers calling back.

## See also

- [[pattern-event-carried-state-transfer]] — alternative event style; payload carries state.
- [[pattern-publish-subscribe]] — delivery mechanism for the notification.
- [[pattern-circuit-breaker]] — protect the producer from callback storms.
- [[pattern-correlation-id]] — trace the event and its callbacks as one flow.
