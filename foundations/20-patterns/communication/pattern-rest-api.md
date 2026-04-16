---
id: pattern-rest-api
title: REST API Design
type: pattern
category: communication
maturity: stable
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

- Building APIs consumed by external or third-party clients where a widely understood contract matters.
- Multi-client systems (web, mobile, CLI) that benefit from a uniform interface and content negotiation.
- Defining boundaries between microservices where independent deployability and technology heterogeneity are goals.
- Exposing public-facing services where discoverability, self-documentation, and HTTP caching provide significant value.

## When NOT to use

- Real-time bidirectional communication (prefer WebSockets or Server-Sent Events).
- Internal high-throughput, low-latency service-to-service calls where binary protocols like gRPC reduce serialisation overhead and provide strict schema enforcement via Protobuf.
- Simple CRUD operations with no external consumers and no foreseeable need for a public contract -- a direct database integration or internal RPC may be simpler.
- Scenarios requiring complex, multi-entity mutations in a single interaction -- consider GraphQL or a dedicated command endpoint instead of forcing multiple round trips.

## Decision inputs

- **Who are the API consumers?** External developers need stable contracts, versioning, and thorough documentation. Internal teams may tolerate tighter coupling.
- **What are the latency requirements?** REST's text-based serialisation (JSON) and HTTP/1.1 overhead add measurable latency compared to binary protocols. Measure whether this matters for your P99.
- **Do you need hypermedia controls?** Richardson Maturity Level 3 (HATEOAS) adds discoverability but increases payload size and client complexity. Most teams operate effectively at Level 2 (HTTP verbs + resources).
- **What caching behaviour is expected?** REST over HTTP gives you ETags, Cache-Control, and conditional requests essentially for free. If your read-to-write ratio is high, this is a significant advantage.
- **How will the API evolve?** Consider URI versioning (`/v2/orders`) vs. header-based versioning (`Accept: application/vnd.api.v2+json`) early -- retrofitting a versioning strategy is painful.

## Solution sketch

Design resources around domain nouns, not verbs. Each resource gets a canonical URI, and HTTP methods convey intent:

```
GET    /orders          # list orders (supports pagination, filtering)
POST   /orders          # create a new order
GET    /orders/{id}     # retrieve a specific order
PUT    /orders/{id}     # full replacement of an order
PATCH  /orders/{id}     # partial update
DELETE /orders/{id}     # remove an order
```

Use standard HTTP status codes consistently: `201 Created` with a `Location` header for successful creation, `404 Not Found` for missing resources, `409 Conflict` for concurrency violations, `422 Unprocessable Entity` for domain validation failures.

Structure error responses with a consistent envelope:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Order quantity must be positive",
    "details": [{ "field": "quantity", "reason": "must be > 0" }]
  }
}
```

For pagination, use cursor-based pagination for large or frequently changing datasets and offset-based pagination when clients need random page access. Include `Link` headers or a `meta` object with `next`/`prev` references.

## Trade-offs

| Gain | Cost |
|------|------|
| Widely understood by developers and supported by virtually all HTTP tooling and frameworks | Verbose for complex operations -- a single user action may require multiple round trips |
| HTTP caching (ETags, Cache-Control, conditional GETs) reduces server load on read-heavy workloads | Overfetching and underfetching are inherent -- clients get fixed resource shapes unless you add sparse fieldsets or embed expansion |
| Technology-agnostic -- any language or platform that speaks HTTP can be a client | No built-in schema enforcement at the protocol level (unlike gRPC/Protobuf); requires discipline around OpenAPI specs |
| Stateless request model simplifies horizontal scaling and load balancing | Statelessness means every request must carry full authentication context, increasing header overhead |

## Implementation checklist

- [ ] Define resource URIs following consistent naming conventions (plural nouns, kebab-case)
- [ ] Document the API with an OpenAPI 3.x specification before implementation begins
- [ ] Implement content negotiation (`Accept` / `Content-Type` headers) and default to `application/json`
- [ ] Use standard HTTP status codes and a consistent error response structure across all endpoints
- [ ] Add pagination to all list endpoints -- choose cursor-based or offset-based and document the choice
- [ ] Implement rate limiting and return `429 Too Many Requests` with `Retry-After` header
- [ ] Version the API from day one using the chosen strategy (URI path or header)
- [ ] Enable CORS with an explicit allowlist if the API is consumed from browser clients
- [ ] Add request ID propagation (`X-Request-Id`) for traceability across services

## See also

- [[pattern-circuit-breaker]] -- protect REST clients from cascading failures when downstream APIs are unhealthy
- [[pattern-input-validation]] -- validate all input at the API boundary before it reaches business logic
