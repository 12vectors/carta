---
id: pattern-correlation-id
title: Correlation Identifier
type: pattern
category: observability
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, observability, correlation]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-distributed-tracing]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-publish-subscribe]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Enterprise Integration Patterns (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/CorrelationIdentifier.html"
---

## When to use

- Any request that fans out to multiple services, queues, or jobs.
- Async workflows where a reply must be matched to its original request.
- Debugging across service boundaries where `trace_id` is unavailable.
- Audit trails that must link user action to downstream effects.

## When NOT to use

- Single-service, single-process requests with no downstream calls.
- Systems already fully covered by distributed tracing with reliable propagation — the tracing IDs *are* the correlation IDs.
- Ephemeral fire-and-forget work where no causal chain matters.

## Decision inputs

- ID format — UUIDv4, ULID, or existing `traceparent` — and collision risk.
- Generation point — always at the edge, never inside downstream services.
- Propagation surface — HTTP headers, gRPC metadata, message headers, job payloads.
- Reuse policy — accept inbound IDs from trusted callers, generate otherwise.
- Logging convention — mandatory field on every log line and span.

## Solution sketch

Generate a unique ID at the system boundary (API gateway, edge service, producer). Attach it to the inbound context and propagate it through **every** downstream call — HTTP header (`X-Correlation-Id` or W3C `traceparent`), message metadata, job arguments. Emit it on every log line and error. For request/reply over async transports, echo it back on the reply so the originator can match.

```
[client] --X-Correlation-Id: abc-123--> [svc-A] --abc-123--> [svc-B]
                                              \--abc-123--> [queue msg]--> [worker]
```

See Hohpe & Woolf (linked in sources) for the request/reply variant.

## Trade-offs

| Gain | Cost |
|------|------|
| Cross-service log joins without full tracing infra | Requires discipline in every service and library |
| Async request/reply matching | One broken hop loses correlation for the rest |
| Lightweight — a single string | Separate concept from `trace_id` unless unified on W3C |
| Low-cost foundation for later tracing | Not a substitute for span-level causal graphs |

## Implementation checklist

- [ ] Pick one ID format and document it.
- [ ] Generate at the edge; accept inbound IDs only from trusted sources.
- [ ] Standardise header name (`X-Correlation-Id` or `traceparent`).
- [ ] Propagate across HTTP, gRPC, and message metadata.
- [ ] Carry the ID through background jobs and scheduled work.
- [ ] Add the ID to every structured log line as a mandatory field.
- [ ] Return the ID in error responses to support client-side troubleshooting.
- [ ] Test propagation across at least one async boundary.

## See also

- [[pattern-distributed-tracing]] — when unified on W3C, the trace ID *is* the correlation ID.
- [[pattern-structured-logging]] — correlation IDs are the join key.
- [[pattern-publish-subscribe]] — propagate via message headers through the broker.
