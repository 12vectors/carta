---
id: pattern-microservices
title: Microservices
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, style, distributed, bounded-contexts]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-modular-monolith]]"
related:
  - "[[pattern-service-based-architecture]]"
  - "[[pattern-event-driven-architecture]]"
conflicts_with: []
contradicted_by:
  - "[[pattern-modular-monolith]]"
sources:
  - "Building Microservices, 2nd ed (Newman, O'Reilly, 2021)"
  - "https://martinfowler.com/articles/microservices.html"
---

## When to use

- Multiple teams need independent deploy cadence on separate subdomains.
- Services have genuinely different scaling, availability, or compliance needs.
- Bounded contexts are well-understood — monolith-first learning is done.
- Strong platform, CI/CD, observability, and on-call capability already in place.

## When NOT to use

- Small team or unclear domain — split prematurely and you freeze wrong boundaries.
- Low ops maturity — no tracing, no service catalog, no platform team.
- Transactional, tightly coupled domain with many cross-entity invariants.
- Cost-sensitive workloads — per-service overhead dominates small systems.

## Decision inputs

- Team topology — one team per service is the coupling target.
- Data ownership model — each service owns its database.
- Inter-service protocol mix (sync REST/gRPC vs async events).
- Transaction strategy — sagas, outbox, compensations.
- Platform readiness — tracing, service mesh, deployment automation.

## Solution sketch

Decompose into **small, independently deployable services** aligned to bounded contexts. Each service owns its data (see [[pattern-database-per-service]]) and exposes an explicit contract. Services communicate via remote calls or events. No shared database, no shared runtime. See Newman (linked) and Fowler's article for decomposition and organisational prerequisites.

```
[team A]        [team B]        [team C]
 [svc A] <----> [svc B] <-----> [svc C]
 [db A ]        [db B ]         [db C ]
        \         |            /
         [  event bus / gateway ]
```

Start from a [[pattern-modular-monolith]] — extract services along proven seams.

## Trade-offs

| Gain | Cost |
|------|------|
| Independent deploy, scale, and tech choice per service | Distributed-system complexity on every interaction |
| Team autonomy — Conway-aligned boundaries | Requires mature platform, tracing, CI/CD, on-call |
| Fault isolation per service | Cross-service transactions need sagas, outbox, eventual consistency |
| Scales organisationally | Wrong boundaries are expensive to fix later |

## Implementation checklist

- [ ] Start from a modular monolith; extract along proven seams.
- [ ] One team owns each service end-to-end.
- [ ] One database per service; no shared schemas.
- [ ] Define contracts (OpenAPI, Protobuf, AsyncAPI) and version them.
- [ ] Stand up tracing, correlation IDs, and a service catalog.
- [ ] Adopt sagas or outbox for cross-service workflows.
- [ ] Automate deploy, rollback, and canary per service.
- [ ] Track service dependencies and enforce versioning policy.

## See also

- [[pattern-modular-monolith]] — prerequisite and contradicting alternative.
- [[pattern-service-based-architecture]] — coarser, lower-cost middle ground.
- [[pattern-event-driven-architecture]] — common inter-service backbone.
- [[pattern-database-per-service]] — non-negotiable data boundary.
- [[pattern-saga]] — transactional workflow across services.
