---
id: dtree-choose-api-style
title: Choose an API Style
type: decision-tree
maturity: stable
tags: [decision-tree, stable, api, communication]
decides_between:
  - "[[pattern-rest-api]]"
  - "[[pattern-graphql-api]]"
  - "[[pattern-grpc-api]]"
criteria:
  - "Consumer class (public third-party, first-party web/mobile, internal service-to-service)"
  - "Query flexibility (fixed contract vs. caller-picked fields)"
  - "Schema enforcement (strict typed vs. loose JSON)"
  - "Latency profile"
  - "Tooling and ecosystem available to consumers"
related_patterns:
  - "[[pattern-api-gateway]]"
  - "[[pattern-backend-for-frontend]]"
---

## Problem

You need to pick a wire protocol and shape for a service's API. REST, GraphQL, and gRPC each optimise for different consumers and constraints.

## Criteria

- **Consumer class** — third-party public, first-party web/mobile, internal service-to-service.
- **Query flexibility** — do consumers need to pick fields and nesting, or is a fixed contract enough?
- **Schema enforcement** — strict typed contract required, or loose JSON acceptable?
- **Latency profile** — user-facing sub-100ms, or tolerant of normal HTTP overhead?
- **Tooling and ecosystem** — what can your consumers already parse and generate?

## Recommendation

| Situation | Choose |
|---|---|
| Public-facing API, many unknown consumers, discoverability matters | [[pattern-rest-api]] |
| Internal service-to-service, latency-sensitive, strict contracts, polyglot | [[pattern-grpc-api]] |
| Web/mobile clients want to pick fields, avoid over-fetch, aggregate many sources | [[pattern-graphql-api]] |
| Per-client shapes fighting a generic API | [[pattern-backend-for-frontend]] (layered on top of any of the above) |
| Mixed client classes through one endpoint | [[pattern-api-gateway]] fronting per-class backends |

## Fallback

When consumer class is unknown or mixed, default to REST. It has the widest toolchain, the lowest onboarding cost for unknown consumers, and the most honest failure modes. Migrate to gRPC or GraphQL only when measurable friction justifies the change.
