---
id: pattern-content-based-router
title: Content-Based Router
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, messaging, routing, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-message-router]]"
related:
  - "[[pattern-message-translator]]"
conflicts_with: []
contradicted_by: []
sources:
  - "EIP (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/ContentBasedRouter.html"
---

## When to use

- Routing depends on payload fields, not just headers or topic.
- Heterogeneous messages share a channel but need different downstream handlers.
- Multi-tenant or multi-region dispatch where the tenant/region is in the body.
- Priority or category fields inside the message drive the decision.
- Upstream cannot be changed to set a header — inspect body instead.

## When NOT to use

- A header or topic already carries the key — a plain message router is enough.
- Payloads are encrypted end-to-end and the router cannot decrypt them.
- Large payloads make inspection expensive — use claim check first, then route.
- Routing logic is domain-heavy and would drift with business rules — move into a handler.

## Decision inputs

- Fields inspected and their schema stability.
- Parser cost vs message volume — JSON path, XPath, compiled schema.
- Schema evolution strategy — how does the router handle new or missing fields?
- Fallback when the routing field is missing or invalid.
- Whether the router may peek at sensitive fields (PII, regulatory scope).
- Rule complexity — config-driven predicates vs compiled code.

## Solution sketch

Parse each incoming message, evaluate predicates against its content, and forward to the matching output. Router remains stateless and does not modify the message.

```
[In] -> [Content Router] --type=order--> [Orders]
                         --type=refund--> [Refunds]
                         --else---------> [Default / DLQ]
```

- Use a **schema-aware parser** (JSON Schema, Avro, Protobuf) for safety.
- Compile predicates once; do not re-parse rules per message.
- Always handle missing/malformed fields explicitly — never NPE into a DLQ storm.
- Keep rules declarative; avoid embedding business logic that belongs in a handler.
- Consider a translator downstream if each route expects a different shape.

## Trade-offs

| Gain | Cost |
|------|------|
| Routes heterogeneous messages without changing producers | Parser and predicate cost on every message |
| Rules express intent clearly in one place | Coupled to message schema — evolution risk |
| No new headers or topics needed to route | Harder to cache — full-body inspection |
| Centralises dispatch; simplifies handlers | PII exposure if router peeks at sensitive fields |

## Implementation checklist

- [ ] Define and version the schema the router reads.
- [ ] Compile predicates once at startup; profile under peak load.
- [ ] Explicit handling for missing or malformed routing fields.
- [ ] Default route to DLQ with context; never drop silently.
- [ ] Emit per-rule match counts; alert on unmatched spikes.
- [ ] Review PII and access scope — router may need least-privilege decryption.
- [ ] Integration-test every route, plus malformed and missing-field cases.
- [ ] Document rule ownership and change process.

## See also

- [[pattern-message-router]] — prerequisite; header-based routing is the simpler base.
- [[pattern-message-translator]] — often paired when each route expects a different shape.
- [[pattern-claim-check]] — keep large payloads out of the router's inspection path.
