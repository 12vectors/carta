---
id: dtree-choose-messaging-style
title: Choose a Messaging Style
type: decision-tree
maturity: stable
tags: [decision-tree, stable, messaging, integration]
decides_between:
  - "[[pattern-rest-api]]"
  - "[[pattern-grpc-api]]"
  - "[[pattern-publish-subscribe]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-async-request-reply]]"
criteria:
  - "Reply timing (now / seconds-to-minutes / no reply needed)"
  - "Receiver fan-out (one / any-of-N workers / all subscribers)"
  - "Ordering requirements (strict / partition / none)"
  - "Back-pressure (can the producer block?)"
  - "Availability coupling (must both sides be up simultaneously?)"
related_patterns:
  - "[[pattern-event-driven-architecture]]"
  - "[[pattern-queue-based-load-leveling]]"
---

## Problem

Two services need to communicate. Synchronous request-response is the default reach; it's also the wrong answer for many cases. Pick the right messaging shape based on how the caller handles the reply and who the receivers are.

## Criteria

- **Reply timing** — caller needs the answer now / tolerates seconds-to-minutes / doesn't need an answer at all.
- **Receiver fan-out** — one receiver / any of N workers / all interested subscribers.
- **Ordering** — strictly ordered / partition-ordered / unordered.
- **Back-pressure** — can the producer block if consumers are slow, or must it always succeed?
- **Availability coupling** — must both sides be up simultaneously?

## Recommendation

| Situation | Choose |
|---|---|
| Caller needs the answer now, latency critical, single receiver | [[pattern-rest-api]] or [[pattern-grpc-api]] |
| Caller needs eventual reply, work is long-running | [[pattern-async-request-reply]] |
| Work is distributed across N stateless workers, order doesn't matter | [[pattern-competing-consumers]] |
| Multiple independent subscribers need the same event | [[pattern-publish-subscribe]] |
| Producer must not block on slow consumers; producer/consumer decoupled in time | [[pattern-queue-based-load-leveling]] (queue between them) |
| System-wide integration across many services, eventual consistency acceptable | [[pattern-event-driven-architecture]] as the overall shape |

## Fallback

If undecided, put a queue between them. Queues turn "must be up at the same time" into "eventually", and add back-pressure for free. The cost is a second moving part; the gain is decoupled deploys and graceful degradation under load.
