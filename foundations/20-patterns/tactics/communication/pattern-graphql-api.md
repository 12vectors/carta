---
id: pattern-graphql-api
title: GraphQL API
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, api, graphql, query]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-rest-api]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://graphql.org/learn/"
  - "https://spec.graphql.org/"
---

## When to use

- Clients need flexible field selection across related entities in a single round trip.
- Multiple client types (web, mobile) fetch overlapping but distinct shapes.
- Aggregating data from several backends behind a unified schema.
- Schema-first contract with strong typing matters for the consumer teams.

## When NOT to use

- Simple CRUD with a single client — REST is cheaper.
- Public APIs needing HTTP caching semantics and edge-cache friendliness.
- File uploads, binary streams, or real-time bidirectional transport.
- Teams without capacity to own schema design, resolver perf, and depth limits.

## Decision inputs

- Shape diversity across clients — low diversity rarely justifies the overhead.
- Backend count the resolver layer must fan out to.
- Read/write ratio — GraphQL mutations offer fewer advantages than queries.
- Caching strategy — persisted queries + CDN, or per-field server cache.
- Tooling maturity in the stack (Apollo, Relay, Strawberry, gqlgen).

## Solution sketch

A single schema defines types, queries, mutations, and subscriptions. Resolvers fetch fields independently; `DataLoader` batches and caches within a request. Clients send a query document specifying exactly the fields needed. One endpoint (`POST /graphql`), one response shape. Enforce depth and complexity limits server-side; use persisted queries in production to lock down allowed shapes and enable CDN caching.

```
Client query ──> /graphql ──> resolvers ──> DataLoader ──> backends
                    │
                    └── depth / complexity / cost guards
```

See the GraphQL spec for execution semantics and graphql.org for schema-design guidance.

## Trade-offs

| Gain | Cost |
|------|------|
| Clients fetch exactly what they need — no over/underfetching | N+1 resolver problem without DataLoader discipline |
| Strong typing and schema-driven tooling | HTTP caching mostly forfeited without persisted queries |
| Single round trip for nested data across backends | Depth/complexity attacks need explicit guards |
| Schema evolves additively without breaking clients | Operational complexity — resolver perf, tracing, auth per field |

## Implementation checklist

- [ ] Schema-first design with code generation for types and clients.
- [ ] DataLoader (or equivalent) for every resolver touching a backend.
- [ ] Depth limit, complexity/cost analysis, and query timeout enforced.
- [ ] Persisted queries for production clients; reject arbitrary ad-hoc queries.
- [ ] Field-level authorisation at resolver boundaries.
- [ ] Error envelope convention (errors array + extensions for codes).
- [ ] Tracing with per-resolver spans.
- [ ] Schema registry and CI check for breaking changes.

## See also

- [[pattern-rest-api]] — alternative; better for simple CRUD and HTTP caching.
- [[pattern-api-gateway]] — GraphQL often sits at the gateway layer.
- [[pattern-backend-for-frontend]] — BFFs frequently expose GraphQL.
