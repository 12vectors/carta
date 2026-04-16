---
id: adr-0001-fastapi-as-default
title: FastAPI as Default Python API Framework
type: adr
maturity: stable
tags: [adr, stable]
status: accepted
date: 2025-03-15
supersedes: ""
superseded_by: ""
affects:
  - "[[pattern-rest-api]]"
related:
  - "[[standard-api-versioning]]"
sources:
  - "https://fastapi.tiangolo.com/"
  - "https://www.techempower.com/benchmarks/"
---

## Context

The organisation needed to standardise on a single Python API framework for building REST services. Without a standard, teams were independently choosing between Flask, Django REST Framework, and FastAPI, leading to inconsistent project structures, duplicated boilerplate, and difficulty moving engineers between teams.

Key requirements for the chosen framework:

- **OpenAPI support.** The org is adopting spec-first API development. The framework must generate OpenAPI-compliant documentation automatically and make it easy to validate implementation against a spec.
- **Request/response validation.** Input validation should be declarative and produce clear error messages without manual parsing code.
- **Async support.** Several services handle high-concurrency I/O-bound workloads (webhook delivery, third-party API aggregation) where async request handling provides measurable throughput improvements.
- **Developer experience.** Type hints, editor autocompletion, and minimal boilerplate reduce onboarding time and defect rates.

## Decision

FastAPI is the default framework for all new Python API services.

Teams may use a different framework only when a specific, documented technical constraint makes FastAPI unsuitable (e.g. a project that must integrate deeply with Django's ORM and admin for a content-management use case). Such exceptions require their own ADR explaining the rationale.

## Consequences

### Positive

- **Async-first architecture.** FastAPI is built on Starlette and supports `async def` endpoints natively. Services handling concurrent I/O workloads (database queries, external API calls, message queue consumers) benefit from async without additional middleware or libraries.
- **Automatic OpenAPI documentation.** FastAPI generates OpenAPI 3.x schemas from endpoint type hints and Pydantic models. This keeps documentation in sync with code and supports the org's spec-first workflow.
- **Pydantic validation.** Request bodies, query parameters, and path parameters are validated through Pydantic models. Invalid requests receive structured error responses automatically, eliminating hand-written validation code.
- **Type safety and editor support.** FastAPI's use of Python type hints provides autocompletion, inline documentation, and static analysis in modern editors, reducing common mistakes.
- **Performance.** FastAPI consistently ranks among the highest-throughput Python web frameworks in independent benchmarks, approaching the performance of Node.js and Go frameworks for I/O-bound workloads.

### Negative

- **Smaller ecosystem than Django.** Django's ecosystem of third-party packages (admin panel, ORM extensions, authentication backends) is significantly larger. Teams requiring these capabilities may need to build or adapt solutions.
- **Team learning curve for async patterns.** Engineers accustomed to synchronous Flask or Django code must learn async/await patterns, understand event loop behaviour, and avoid blocking calls in async endpoints. This requires targeted training and code review vigilance.
- **ORM integration is not built-in.** Unlike Django REST Framework, FastAPI does not ship with an ORM. Teams must choose and configure a database layer (SQLAlchemy, Tortoise ORM, or raw async drivers), adding a setup step.

## Alternatives considered

### Flask

Flask is the most widely used Python microframework and was the previous de facto choice for several teams.

- **Strengths:** Mature ecosystem, extensive documentation, large pool of developers with experience, simple mental model.
- **Why not chosen:** No built-in request validation (requires Flask-Marshmallow or similar), no automatic OpenAPI generation (requires Flask-Smorest or connexion), synchronous-only without additional ASGI wrappers. Retrofitting these capabilities adds complexity that FastAPI provides out of the box.

### Django REST Framework (DRF)

DRF is the standard choice for teams already using Django and needing a full-featured API toolkit.

- **Strengths:** Deep Django integration (ORM, admin, authentication), serializers with built-in validation, browsable API, mature pagination and filtering.
- **Why not chosen:** Heavyweight for pure API services that do not need Django's ORM or admin. Synchronous by default (Django's async support is still maturing). Generates OpenAPI via `drf-spectacular`, which works well but is a third-party add-on rather than a core feature. The overhead of a full Django project is unjustified when the service is a focused API with its own database layer.

## See also

- [[pattern-rest-api]] -- org-level REST API pattern that mandates FastAPI for Python services
- [[standard-api-versioning]] -- API versioning standard that FastAPI services must implement
