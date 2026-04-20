---
id: pattern-hexagonal-architecture
title: Hexagonal Architecture (Ports and Adapters)
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, style, ports-and-adapters, testability]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-layered-architecture]]"
  - "[[pattern-modular-monolith]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html"
  - "Cockburn, Hexagonal Architecture (2005) — https://alistair.cockburn.us/hexagonal-architecture/"
---

## When to use

- Rich domain logic that must outlive any specific UI, DB, or messaging technology.
- Systems with multiple entry points (HTTP, CLI, queue, scheduler) against one domain.
- Teams practising TDD or DDD — domain testing without infrastructure is a first-class goal.
- Migrations where infrastructure will change under stable business rules.

## When NOT to use

- Thin CRUD apps — indirection cost outweighs isolation benefit.
- Small scripts or prototypes with no durable domain model.
- Teams unfamiliar with dependency inversion — misapplied ports produce noise.
- Performance-critical paths where adapter indirection adds measurable cost.

## Decision inputs

- Number of external actors (UIs, queues, schedulers) driving the domain.
- Number of infrastructure dependencies (DBs, APIs, buses) serving the domain.
- Test strategy — domain unit tests without infra are a primary driver.
- Expected lifetime of infrastructure choices.
- Language and DI support for interface-based inversion.

## Solution sketch

Domain sits at the centre. **Ports** are interfaces the domain defines: **driving ports** (inbound — what the domain offers) and **driven ports** (outbound — what the domain needs). **Adapters** implement ports against concrete technologies (HTTP, SQL, Kafka). Domain depends on nothing outside itself.

```
[ http adapter ]                    [ sql adapter ]
        \                                /
   (driving port)              (driven port)
            \                      /
             [----- domain -----]
            /                      \
   (driving port)              (driven port)
        /                                \
[ cli adapter ]                     [ kafka adapter ]
```

See AWS prescriptive guidance and Cockburn's original (both linked) for port/adapter taxonomy.

## Trade-offs

| Gain | Cost |
|------|------|
| Domain testable without infrastructure | More interfaces, wiring, and DI configuration |
| Infrastructure swappable without domain changes | Over-abstraction risk for thin domains |
| Multiple entry points share one domain | Extra indirection on every external call |
| Forces explicit domain boundary | Newcomers may confuse ports with repositories or DTOs |

## Implementation checklist

- [ ] Identify the domain and forbid infra imports from it.
- [ ] Define driving ports for each external actor.
- [ ] Define driven ports for each external dependency.
- [ ] Wire adapters via DI at the application edge.
- [ ] Unit-test the domain with in-memory adapter fakes.
- [ ] Lint or enforce direction of dependencies (domain -> nothing external).
- [ ] Document the adapter catalog and port contracts.

## See also

- [[pattern-layered-architecture]] — simpler alternative when inversion isn't needed.
- [[pattern-modular-monolith]] — often implemented with hexagonal modules inside.
- [[pattern-anti-corruption-layer]] — adapter specifically for untrusted external models.
