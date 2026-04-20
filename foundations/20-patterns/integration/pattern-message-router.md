---
id: pattern-message-router
title: Message Router
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, messaging, routing, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-content-based-router]]"
  - "[[pattern-publish-subscribe]]"
conflicts_with: []
contradicted_by: []
sources:
  - "EIP (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageRouter.html"
---

## When to use

- One input channel feeds several destination channels chosen per-message.
- Senders should not know destination addresses or topology.
- Routing logic must be changeable without touching producers or consumers.
- Composing pipelines from reusable, single-purpose endpoints.
- Abstracting legacy queue naming from upstream services.

## When NOT to use

- Only one downstream exists — direct delivery is simpler.
- Every consumer needs every message (use publish-subscribe).
- Routing decision requires peeking into payload (use content-based router).
- Extra hop would violate latency SLOs.

## Decision inputs

- Routing key source — header, topic, env, or tenant.
- Change frequency of the routing rules (config vs code).
- Statelessness — can the router be replicated trivially?
- Error handling when no route matches — DLQ, default, drop.
- Observability: per-route counts, latencies, failure rates.
- Who owns the routing rules and how are they deployed?

## Solution sketch

A stateless filter reads each message, inspects a routing key, and forwards it — unchanged — to exactly one of N output channels.

```
[In] -> [Router] --key=A--> [Channel A]
                \--key=B--> [Channel B]
                \--else---> [Default / DLQ]
```

- Router is **stateless** and **side-effect free** — logging aside.
- Do not transform the message; pair with a translator if shapes diverge.
- Always define a default route — never silently drop.
- Externalise rules (config, feature flags) to avoid redeploys for route changes.
- Emit metrics per output to catch drift in traffic shape.

## Trade-offs

| Gain | Cost |
|------|------|
| Producers and consumers decoupled from topology | Extra hop — latency and one more moving part |
| Routing rules change without touching endpoints | Router becomes a choke point if stateful or slow |
| Enables reusable, single-purpose endpoints | Debugging needs end-to-end tracing across hops |
| Cleanly separates "where" from "what" | Config drift between rules and downstream reality |

## Implementation checklist

- [ ] Choose routing key and document its source (header, metadata, topic).
- [ ] Keep the router stateless; scale horizontally.
- [ ] Externalise rules in config; version them.
- [ ] Define a default/fallback route — never drop silently.
- [ ] Emit per-route counters and latencies.
- [ ] Propagate correlation IDs untouched — see `[[pattern-correlation-id]]`.
- [ ] Integration-test each branch, including the default.
- [ ] Alert on traffic drift between expected and observed route shares.

## See also

- [[pattern-content-based-router]] — specialisation that routes on payload.
- [[pattern-publish-subscribe]] — when every consumer needs a copy, not one of them.
- [[pattern-message-translator]] — pair with a router when shapes differ per destination.
