---
id: pattern-rest-api
title: REST API Design
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-performance]]"
tags: [pattern, stable, api, http, rest]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related: []
conflicts_with: []
contradicted_by: []
sources:
  - "RESTful Web APIs (Richardson & Amundsen, 2013)"
  - "https://martinfowler.com/articles/richardsonMaturityModel.html"
---

## When to use

- APIs consumed by external or third-party clients needing a widely understood contract.
- Multi-client systems (web, mobile, CLI) benefiting from a uniform interface.
- Microservice boundaries where independent deployability matters.
- Public-facing services where HTTP caching and discoverability pay off.

## When NOT to use

- Real-time bidirectional channels — use WebSockets or SSE.
- Internal high-throughput, low-latency service calls — prefer gRPC.
- Complex multi-entity mutations needing a single round trip — consider GraphQL.
- Internal CRUD with no external consumer and no public-contract need.

## Decision inputs

- Consumer profile (external vs internal) drives contract stability and versioning rigour.
- Latency budget — REST/JSON adds measurable overhead vs binary protocols.
- Richardson Maturity target (most teams stop at Level 2).
- Caching needs — ETags and Cache-Control are free wins for read-heavy APIs.
- Versioning strategy (URI path vs `Accept` header) — decide early.

## Solution sketch

Resources as nouns, HTTP verbs as intent, standard status codes, consistent error envelope, explicit pagination strategy. Minimal shape:

```
GET    /orders          POST   /orders
GET    /orders/{id}     PUT    /orders/{id}
PATCH  /orders/{id}     DELETE /orders/{id}
```

For full design guidance see Richardson & Amundsen; for maturity-level framing see the Fowler article.

## Trade-offs

| Gain | Cost |
|------|------|
| Universal HTTP tooling and developer familiarity | Verbose for complex ops — many round trips |
| Free HTTP caching on read-heavy workloads | Over-/underfetching unless sparse fieldsets are added |
| Technology-agnostic clients | No protocol-level schema — relies on OpenAPI discipline |
| Stateless — trivial horizontal scaling | Every request carries full auth context |

## Implementation checklist

- [ ] Resource URIs use plural nouns, kebab-case, consistent naming.
- [ ] OpenAPI 3.x spec authored before implementation.
- [ ] Standard status codes + consistent error envelope across endpoints.
- [ ] Pagination on every list endpoint (cursor or offset; documented).
- [ ] Rate limiting with `429` and `Retry-After`.
- [ ] Versioning strategy in place from day one.
- [ ] CORS allowlist configured for browser clients.
- [ ] Request ID propagation (`X-Request-Id`).

## See also

- [[pattern-circuit-breaker]] — protect REST clients from downstream failures.
- [[pattern-input-validation]] — validate at the boundary before reaching business logic.
