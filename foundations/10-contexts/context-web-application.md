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
  - "[[pattern-input-validation]]"
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-structured-logging]]"
recommended_standards: []
common_antipatterns:
  - "[[antipattern-god-service]]"
related:
  - "[[context-event-driven-system]]"
sources:
  - "Building Microservices (Newman, 2021) ch. 1-3"
  - "Designing Data-Intensive Applications (Kleppmann, 2017) ch. 1"
---

## Description

A system that serves HTTP requests — whether to human users via a browser, to mobile clients via an API, or to other services. Web applications are the most common system archetype and span everything from single-page apps backed by a REST API to complex multi-service platforms.

The defining characteristic is the request-response cycle: a client sends a request, the system processes it, and returns a response. This shapes everything from error handling (what does the caller see?) to scaling (how many concurrent requests?) to security (who is the caller?).

## Key concerns

- **Latency.** Users and downstream services expect responses within hundreds of milliseconds. Architectural choices that add latency compound across the call chain.
- **Availability.** Downtime is directly visible to users. Resilience patterns (circuit breakers, graceful degradation) matter more here than in batch systems.
- **Security.** Web applications are internet-facing by default. Authentication, authorisation, input validation, and secrets management are non-negotiable.
- **Scalability.** Traffic is often unpredictable. The architecture must handle load spikes without manual intervention.
- **Observability.** When something goes wrong in production, structured logging and distributed tracing are how you find out what happened.

## Typical architecture

Most web applications follow one of these shapes:

- **Monolith** — a single deployable unit handling all concerns. Simple to start, hard to scale independently. Appropriate for small teams and early-stage products.
- **API + SPA** — a frontend single-page application backed by a REST or GraphQL API. Clean separation of concerns but introduces CORS, authentication token management, and two deployment pipelines.
- **Microservices** — multiple independently deployable services communicating over HTTP or messaging. Enables independent scaling and team autonomy but introduces distributed systems complexity (consistency, network failures, observability).
- **Backend for Frontend (BFF)** — a thin API layer per client type (web, mobile, internal) that aggregates calls to backend services. Reduces client complexity at the cost of an additional layer.

## See also

- [[context-event-driven-system]] — web applications with asynchronous internals often combine both contexts
