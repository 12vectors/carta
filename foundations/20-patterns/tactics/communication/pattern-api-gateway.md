---
id: pattern-api-gateway
title: API Gateway
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-security]]"
tags: [pattern, stable, api, gateway, edge]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-backend-for-frontend]]"
  - "[[pattern-gateway-aggregation]]"
  - "[[pattern-gateway-offloading]]"
  - "[[pattern-gateway-routing]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://microservices.io/patterns/apigateway.html"
  - "Microservices Patterns (Richardson, Manning, 2018) ch. 8 — https://www.manning.com/books/microservices-patterns"
---

## When to use

- Multiple backend services exposed as one external surface to clients.
- Cross-cutting concerns (authn, rate limiting, TLS) need one enforcement point.
- Clients should not know internal service topology or protocols.
- Independent teams want to evolve services without breaking external contracts.

## When NOT to use

- Single backend service — direct ingress is simpler.
- Strictly internal east-west traffic — use a service mesh instead.
- Ultra-low-latency paths where the extra hop exceeds the budget.
- Teams unwilling to own the gateway as a critical shared component.

## Decision inputs

- Number of backends and diversity of protocols (REST, gRPC, GraphQL, WS).
- Client types — web, mobile, partners — and whether each needs a distinct shape.
- Concerns to centralise (authn, throttling, logging, TLS termination, WAF).
- Managed vs self-hosted (AWS APIGW, Kong, Envoy, Apigee, Azure APIM).
- Expected request volume and latency budget per hop.

## Solution sketch

A single network entry point terminates TLS, authenticates the caller, applies rate limits, and routes to backends. Optionally aggregates, transforms, or translates protocols. Keep business logic *out* of the gateway; put it in backends or BFFs. For client-specific concerns, prefer a BFF per client type over one gateway that tries to please everyone.

```
clients ──> [API Gateway] ──> service A
                         ├──> service B
                         └──> service C
            (authn, TLS, rate-limit, routing, logging)
```

See Richardson ch. 8 and microservices.io for trade-offs vs direct-to-service.

## Trade-offs

| Gain | Cost |
|------|------|
| One place to enforce authn, rate limits, TLS | Single point of failure — must be HA and horizontally scaled |
| Hides backend topology from clients | Operational ownership and on-call for a critical path |
| Protocol translation and response shaping at the edge | Risk of becoming a god-object if business logic creeps in |
| Central observability across all backends | Extra hop — latency and cost per request |

## Implementation checklist

- [ ] Run gateway behind a load balancer; multiple instances, multi-AZ.
- [ ] Terminate TLS and validate auth tokens (JWT, OAuth2) at the edge.
- [ ] Per-route rate limits and quotas with identifiable consumers.
- [ ] Request/response size limits and timeout budgets per backend.
- [ ] Structured access logs with correlation IDs propagated downstream.
- [ ] No business logic in the gateway — transformations only.
- [ ] Health-check and circuit breaking on upstream backends.
- [ ] Canary/blue-green deploys; config changes reviewed like code.

## See also

- [[pattern-backend-for-frontend]] — per-client gateway variant.
- [[pattern-gateway-aggregation]] — fan out and merge responses.
- [[pattern-gateway-offloading]] — push cross-cutting concerns to the edge.
- [[pattern-gateway-routing]] — route by path, header, or version.
