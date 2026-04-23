---
id: context-web-application
title: Web Application
type: context
maturity: stable
tags: [context, stable]
signals:
  - "Serves HTTP requests to users or other services"
  - "Has a UI, API endpoints, authentication, sessions, or request-response cycles"
  - "Users interact with it through a browser or mobile client"
recommended_patterns:
  - "[[pattern-rest-api]]"
  - "[[pattern-api-gateway]]"
  - "[[pattern-input-validation]]"
  - "[[pattern-oauth2-authorization]]"
  - "[[pattern-rate-limiting]]"
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-timeout]]"
  - "[[pattern-health-check-endpoint]]"
  - "[[pattern-cache-aside]]"
  - "[[pattern-load-balancing]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-distributed-tracing]]"
  - "[[pattern-correlation-id]]"
  - "[[pattern-feature-flag]]"
  - "[[pattern-canary-release]]"
  - "[[pattern-blue-green-deployment]]"
  - "[[pattern-prompt-injection-defense]]"
recommended_standards: []
common_antipatterns:
  - "[[antipattern-god-service]]"
  - "[[antipattern-silent-failure]]"
related:
  - "[[context-event-driven-system]]"
  - "[[context-agentic-system]]"
sources:
  - "Building Microservices (Newman, 2021) ch. 1-3"
  - "Designing Data-Intensive Applications (Kleppmann, 2017) ch. 1"
---

## Description

A system that serves HTTP requests — to humans via a browser, to mobile clients via an API, or to other services. The defining shape is the request-response cycle, which drives decisions on error handling, scaling, and security.

## Key concerns

- **Latency.** P99 budgets in hundreds of milliseconds; architectural overhead compounds across calls.
- **Availability.** Downtime is user-visible; resilience patterns are non-optional.
- **Security.** Internet-facing by default; authN, authZ, and input validation are baseline.
- **Scalability.** Traffic is spiky; automatic horizontal scaling is expected.
- **Observability.** Structured logs and tracing are how incidents get diagnosed.

## Typical architecture

- **Monolith** — single deployable; simple start, hard to scale independently.
- **API + SPA** — frontend SPA over REST/GraphQL; clean separation, two pipelines.
- **Microservices** — independent services; team autonomy at the cost of distributed-systems complexity.
- **BFF** — thin per-client API; reduces client complexity, adds a layer.

## See also

- [[context-event-driven-system]] — web apps with async internals straddle both contexts.
- [[dtree-choose-api-style]] — pick between REST, GraphQL, and gRPC for the service's external API.
- [[dtree-choose-service-boundary]] — decide between monolith, modular monolith, service-based, and microservices shapes.
- [[dtree-choose-background-work]] — pick between inline tasks, durable queue, workflow engine, or serverless for non-blocking work.
