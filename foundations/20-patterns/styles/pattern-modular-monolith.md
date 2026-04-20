---
id: pattern-modular-monolith
title: Modular Monolith
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, style, monolith, modularity]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-layered-architecture]]"
  - "[[pattern-hexagonal-architecture]]"
conflicts_with: []
contradicted_by:
  - "[[pattern-microservices]]"
sources:
  - "https://martinfowler.com/bliki/MonolithFirst.html"
---

## When to use

- Default starting point for a new system — boundaries aren't yet proven.
- Small to mid teams where distributed-system overhead outweighs the benefit.
- Domains still being learned — cheap to move module boundaries.
- Applications that need strong in-process invariants and transactions.

## When NOT to use

- Teams already at a scale that demands independent deployability per module.
- Subsystems with genuinely divergent scaling, compliance, or availability needs.
- Organisations with many teams blocked on a single deploy pipeline.
- Workloads whose modules must be written in different languages or runtimes.

## Decision inputs

- Team count and deploy-pipeline contention.
- Strength of current module boundaries (imports, schemas, tests).
- Frequency and cost of cross-module changes.
- Operational maturity — distributed ops readiness.
- Expected migration path if extraction becomes necessary.

## Solution sketch

Single deployable unit, internally structured as **independent modules** with explicit public APIs. Modules do not reach into each other's internals or databases. Calls cross module boundaries only through published interfaces. Shared DB is acceptable but each module owns its tables. Boundaries rehearsed here become extraction seams if microservices are warranted later.

```
  [-------- single deployable ---------]
  | [module A]  [module B]  [module C] |
  |   api \       api |       / api    |
  |        \          |      /         |
  |         [ shared runtime ]         |
  [------------------------------------]
             [  database  ]
```

See Fowler's "Monolith First" (linked) for the argument that modules should precede services.

## Trade-offs

| Gain | Cost |
|------|------|
| Simple deploy, debug, and local dev | One deploy pipeline — team contention at scale |
| In-process calls — no network failure modes | Requires discipline to keep modules from coupling |
| Strong transactions across module boundaries | Shared runtime = shared failure domain |
| Cheap to refactor boundaries | Not a terminal state at large team sizes |

## Implementation checklist

- [ ] Define modules by subdomain, not by technical layer.
- [ ] Publish each module's API; forbid internal imports across modules.
- [ ] Enforce boundaries via build tool, lint, or package visibility.
- [ ] Own tables per module; forbid cross-module DB reads.
- [ ] Route cross-module calls through module APIs, not shared helpers.
- [ ] Track cross-module change frequency — a signal for extraction.
- [ ] Document the extraction path to services if scaling demands it.

## See also

- [[pattern-microservices]] — contradicting alternative when independent deploy is mandatory.
- [[pattern-layered-architecture]] — compatible internal shape for individual modules.
- [[pattern-hexagonal-architecture]] — common module-internal organisation.
- [[pattern-strangler-fig]] — migration pattern when extracting modules to services.
