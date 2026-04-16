---
id: antipattern-god-service
title: God Service
type: antipattern
category: communication
maturity: stable
tags: [antipattern, stable, communication, monolith]
applies_to:
  - "[[context-web-application]]"
mitigated_by:
  - "[[pattern-rest-api]]"
related: []
sources:
  - "Building Microservices (Newman, 2021) ch. 3"
  - "Monolith to Microservices (Newman, 2019) ch. 2"
---

## How to recognise

- **One service owns most of the business logic.** Feature requests across unrelated domains (payments, notifications, user management, reporting) all land in the same codebase.
- **Most changes require deploying the same service.** The deploy log shows the same artefact being released for nearly every ticket, regardless of which team or feature area is involved.
- **The service owns many database tables.** A single schema contains tables spanning multiple bounded contexts -- orders, users, inventory, and billing all live side by side.
- **Teams step on each other's changes.** Merge conflicts are frequent, integration branches are long-lived, and unrelated pull requests block each other because they touch the same service.
- **Build and test times are disproportionately long.** The CI pipeline for this one service dwarfs every other service in the organisation.

## Why it happens

- **Starts as a monolith that grows without boundaries.** The initial architecture was appropriate for a small team and a narrow scope, but no one drew lines between domains as the product expanded.
- **"Just add it to the main service" is the path of least resistance.** Creating a new service requires infrastructure, deployment pipelines, and cross-service communication -- adding a module to the existing service takes minutes.
- **Bounded contexts aren't identified early.** Without deliberate domain modelling, developers gravitate toward the existing codebase rather than reasoning about where a capability belongs.
- **Shared database coupling.** Once multiple features share tables or join across domain boundaries, extracting a service becomes a data migration problem that nobody wants to tackle.

## Consequences

- **Long deploy cycles.** Every change, no matter how small, requires building, testing, and deploying the entire monolith. A one-line fix in billing triggers the full test suite for user management, notifications, and everything else.
- **High blast radius for failures.** A memory leak in the reporting module takes down payments. An unhandled exception in notifications crashes the order pipeline. There is no isolation between concerns.
- **Team coupling.** Independent teams cannot ship independently. Release coordination becomes a bottleneck, and a single team's regression blocks everyone else.
- **Difficult to scale individual features.** The entire service must scale uniformly even when only one capability (e.g. search) is under load. This wastes resources and limits responsiveness to traffic spikes.
- **Cognitive overload.** New developers face a massive codebase with unclear boundaries. Onboarding takes longer, and the risk of unintended side effects from changes increases.

## How to fix

1. **Identify bounded contexts.** Use domain-driven design techniques (event storming, context mapping) to draw explicit boundaries around cohesive sets of business capabilities.
2. **Extract services along domain boundaries.** Start with the highest-churn areas -- the modules that change most frequently and cause the most merge conflicts get the most benefit from extraction.
3. **Apply the strangler fig pattern.** Route new traffic for a capability to a new service while the god service continues to handle existing traffic. Gradually migrate until the old code path can be removed.
4. **Break the shared database.** Give each extracted service its own data store. Use integration events or API calls to synchronise data that must cross boundaries -- do not share tables.
5. **Establish service contracts early.** Define APIs (using OpenAPI or similar specifications) between the god service and extracted services before writing implementation code. This prevents reintroducing tight coupling.

## See also

- [[pattern-rest-api]] -- defines the communication contract between extracted services
- [[context-web-application]] -- the system context where god services most commonly appear
