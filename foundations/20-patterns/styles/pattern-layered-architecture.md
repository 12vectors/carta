---
id: pattern-layered-architecture
title: Layered Architecture
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, style, monolith, separation-of-concerns]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-modular-monolith]]"
  - "[[pattern-hexagonal-architecture]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Software Architecture Patterns (Richards, O'Reilly, 2015) ch. 1"
  - "https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/"
---

## When to use

- Small-to-medium CRUD-shaped applications with a single dominant data model.
- Teams new to the domain — layering makes responsibilities obvious and onboarding cheap.
- Systems where technical concerns (UI, business, persistence) drive structure more than business subdomains.
- Starter architecture when future shape is unclear — easy to refactor outward.

## When NOT to use

- High-throughput systems — each request traverses every layer, adding latency.
- Systems with many independent deployment or scaling units.
- Rich domains where business rules don't map cleanly onto technical layers.
- Applications needing plug-in extensibility — prefer [[pattern-microkernel]].

## Decision inputs

- Number of distinct subdomains — one or few favours layering; many favours modularisation.
- Deployment model — single deployable unit fits layering naturally.
- Change frequency per layer — frequent cross-layer changes signal the wrong boundary.
- Team size and seniority — layers are a well-understood default.
- Testability needs — closed layers ease unit-testing but make mocking chains verbose.

## Solution sketch

Stack components in horizontal layers — typically presentation, business, persistence, database. Each layer has a single, well-defined role. Layers are **closed**: requests pass through every layer in order, never skip. Open a layer only with explicit justification (e.g. a shared utility layer bypassed for performance).

```
[ Presentation ]
[ Business     ]
[ Persistence  ]
[ Database     ]
```

See Richards ch. 1 (linked) for the "architecture sinkhole" anti-pattern and tuning guidance.

## Trade-offs

| Gain | Cost |
|------|------|
| Familiar, low-friction default for most teams | Every request pays the full-stack traversal cost |
| Clear separation of technical concerns | Encourages technical cohesion over domain cohesion |
| Easy to test each layer in isolation | Cross-layer features require coordinated changes |
| Single deployable unit — simple ops | Doesn't scale layers independently |

## Implementation checklist

- [ ] Define layers and their responsibilities in writing.
- [ ] Enforce closed-layer access with module boundaries or lint rules.
- [ ] Justify and document any open layer exceptions.
- [ ] Place domain logic in the business layer — not in controllers or repositories.
- [ ] Keep persistence concerns out of the business layer.
- [ ] Integration-test the full stack end-to-end.
- [ ] Watch for the sinkhole anti-pattern (layers that only pass through).

## See also

- [[pattern-modular-monolith]] — organise by domain module instead of technical layer.
- [[pattern-hexagonal-architecture]] — invert dependencies so domain doesn't depend on infrastructure.
- [[pattern-microkernel]] — alternative shape for extensible applications.
