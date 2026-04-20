---
id: dtree-choose-service-boundary
title: Choose a Service Boundary
type: decision-tree
maturity: stable
tags: [decision-tree, stable, architecture, service-boundary]
decides_between:
  - "[[pattern-layered-architecture]]"
  - "[[pattern-modular-monolith]]"
  - "[[pattern-service-based-architecture]]"
  - "[[pattern-microservices]]"
criteria:
  - "Team count and structure"
  - "Release cadence (weekly uniform vs. per-team independent)"
  - "Scale profile (uniform vs. uneven hot spots)"
  - "Operational maturity (distributed tracing, service mesh, on-call)"
  - "Domain boundary clarity"
related_patterns:
  - "[[pattern-hexagonal-architecture]]"
  - "[[pattern-strangler-fig]]"
---

## Problem

Choose how to split the system into deployable units. Going too small (microservices too early) buys distributed-systems complexity without buying anything else; going too large locks out team autonomy and independent release.

## Criteria

- **Team count and structure** — one team / several aligned teams / many independent teams.
- **Release cadence** — weekly uniform / per-module / per-team independent.
- **Scale profile** — uniform load / uneven hot spots / very uneven.
- **Operational maturity** — can the team run distributed tracing, service-mesh, on-call for many services?
- **Domain boundaries** — are bounded contexts already clear, or is the domain still being discovered?

## Recommendation

| Situation | Choose |
|---|---|
| One team, early product, domain still being discovered | [[pattern-layered-architecture]] |
| One team, domain stabilising, want modularity without operational overhead | [[pattern-modular-monolith]] |
| A few teams, clear domain chunks, want per-domain release | [[pattern-service-based-architecture]] |
| Many teams, clear bounded contexts, uneven scale profile, strong ops maturity | [[pattern-microservices]] |
| Migrating a monolith toward smaller services | [[pattern-strangler-fig]] is the path; destination is one of the above |

Layer [[pattern-hexagonal-architecture]] orthogonally for testability and swappable adapters — it applies at any granularity.

## Fallback

When in doubt, go larger. Modular monolith first, microservices later. The cost of splitting too early is high and early; the cost of splitting later, via strangler-fig, is spread over time and optional. Martin Fowler's "MonolithFirst" argues this explicitly.
