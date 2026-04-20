---
id: pattern-service-based-architecture
title: Service-Based Architecture
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, style, distributed, coarse-grained-services]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-microservices]]"
  - "[[pattern-modular-monolith]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Fundamentals of Software Architecture (Richards & Ford, 2020)"
  - "https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/"
---

## When to use

- Monolith breaking up but the team isn't ready for microservices operational overhead.
- Applications that need independent deployability without per-service databases.
- Domains with 4–12 coarse-grained services aligned to subdomains.
- Teams lacking strong DevOps, observability, or distributed-tracing maturity.

## When NOT to use

- Fine-grained scaling or fault isolation per entity — go microservices.
- Strictly single-deployable systems — use [[pattern-modular-monolith]].
- Domains where a shared database is unacceptable (regulatory, multi-tenant isolation).
- Event-first systems — prefer [[pattern-event-driven-architecture]].

## Decision inputs

- Service granularity — domain-sized, not entity-sized.
- Shared vs partitioned database strategy.
- Synchronous vs asynchronous inter-service contracts.
- Deployment pipeline capability (per-service CI/CD readiness).
- Transaction boundaries — single DB simplifies, but couples services.

## Solution sketch

Decompose the system into a small number of **coarse-grained, independently deployable services** behind a UI or API gateway. Services typically share one database but own separate schemas or tables. Inter-service calls are remote (REST/gRPC) but kept minimal — most logic stays within one service.

```
        [ user interface / api gateway ]
          /        |        |        \
      [svc A]  [svc B]  [svc C]  [svc D]
          \        |        |        /
           [   shared database    ]
```

See Richards & Ford (linked) for the "middle ground" positioning between monolith and microservices.

## Trade-offs

| Gain | Cost |
|------|------|
| Independent deployability without microservices tax | Shared DB couples services at the schema layer |
| Fewer moving parts than microservices | Schema changes require cross-service coordination |
| Coarse services match team topology | Weaker fault isolation — DB is shared failure mode |
| Lower ops maturity bar than microservices | Not a long-term destination if scaling diverges per service |

## Implementation checklist

- [ ] Identify 4–12 coarse services aligned to subdomains.
- [ ] Define schema ownership — one service owns each table's writes.
- [ ] Pick an inter-service protocol and keep contracts stable.
- [ ] Stand up per-service CI/CD pipelines.
- [ ] Route through a gateway or UI facade.
- [ ] Instrument cross-service calls with correlation IDs.
- [ ] Document migration path to microservices if scaling diverges.

## See also

- [[pattern-microservices]] — next step if fine-grained scaling and isolation matter.
- [[pattern-modular-monolith]] — simpler step if independent deployment isn't needed.
- [[pattern-api-gateway]] — typical front door for service-based systems.
