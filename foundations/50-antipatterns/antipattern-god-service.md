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

- One service owns business logic across unrelated domains.
- Most feature work deploys the same artefact regardless of team.
- A single schema holds tables from multiple bounded contexts.
- Teams collide in merge conflicts on the same service.
- CI for this service dwarfs every other service's CI.

## Why it happens

- Monolith grew without anyone drawing domain boundaries.
- "Just add it to the main service" is cheaper than spinning up a new one.
- Bounded contexts were never identified through domain modelling.
- Shared tables made later extraction a data-migration problem no one owns.

## Consequences

- Long deploy cycles — every change rebuilds everything.
- High blast radius — a fault in one domain takes others down.
- Team coupling — no team ships independently.
- Uniform scaling — the whole service scales to the hottest feature's needs.
- Onboarding drag — unclear boundaries slow new contributors.

## How to fix

- Identify bounded contexts (event storming, context mapping).
- Extract along domain boundaries, starting with the highest-churn areas.
- Apply the strangler fig: route new traffic to new services, drain the old.
- Split the database — per-service ownership, integrate via events or APIs.
- Define service contracts (OpenAPI) before writing the implementation.

## See also

- [[pattern-rest-api]] — the contract between extracted services.
- [[context-web-application]] — the context where god services most commonly appear.
