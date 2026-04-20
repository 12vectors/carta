---
id: pattern-backend-for-frontend
title: Backend for Frontend (BFF)
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, api, bff, gateway]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-api-gateway]]"
  - "[[pattern-microservices]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://samnewman.io/patterns/architectural/bff/"
---

## When to use

- Distinct client types (web, iOS, Android, partner) have diverging data needs.
- One generic API is drifting toward lowest-common-denominator shapes.
- Client teams are blocked waiting on a shared backend team.
- Mobile bandwidth or battery makes payload shaping per client worth it.

## When NOT to use

- Single client type — a plain API gateway or service API suffices.
- Client variations are cosmetic only — handle them client-side.
- Team cannot staff per-client backends — one neglected BFF is worse than none.
- Contract needs to be a public, stable surface for arbitrary third parties.

## Decision inputs

- Number of client types and how their data shapes actually differ.
- Ownership model — ideally the client team owns its BFF.
- Auth model — BFF often holds session/cookie and exchanges for downstream tokens.
- Shared logic risk — what must stay in downstream services, not duplicated per BFF.
- Deployment topology — BFF co-located with client CDN or API edge.

## Solution sketch

One backend per client type, each tailored to that client's screens and flows. BFFs call downstream domain services (which own the data), aggregate and reshape, and expose a client-optimised contract. Keep business rules in the downstream services; BFF responsibilities are shape, aggregation, client-specific auth/session, and light orchestration.

```
iOS app  ──> iOS BFF  ─┐
Web app  ──> Web BFF  ─┼──> domain services
Partner  ──> Partner BFF┘
```

See Sam Newman's write-up for the origin and scoping rules.

## Trade-offs

| Gain | Cost |
|------|------|
| Client-optimised payloads — fewer round trips, smaller responses | One backend per client type to build, deploy, operate |
| Client team owns its backend — faster iteration | Risk of duplicated logic across BFFs if domain boundaries slip |
| Client-specific auth (cookies/session) cleanly contained | Harder to reuse for a new client — expect another BFF |
| Shield domain services from client churn | More deploy targets; more CI/CD and observability surface |

## Implementation checklist

- [ ] One BFF per client type; no sharing between iOS and Android "to save effort".
- [ ] BFF owned by the client team that consumes it.
- [ ] Business logic stays in domain services; BFF orchestrates and reshapes.
- [ ] Session/cookie termination at BFF; downstream uses short-lived tokens.
- [ ] Response shape evolves with client releases; versioning per client.
- [ ] Timeouts and circuit breakers on every downstream call.
- [ ] Per-BFF observability — its own dashboards and alerts.

## See also

- [[pattern-api-gateway]] — parent pattern; BFF is a per-client specialisation.
- [[pattern-gateway-aggregation]] — BFFs commonly aggregate responses.
- [[pattern-microservices]] — BFFs typically front a microservice estate.
