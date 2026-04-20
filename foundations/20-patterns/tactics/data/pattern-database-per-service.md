---
id: pattern-database-per-service
title: Database per Service
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, data, microservices, bounded-context]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-microservices]]"
related:
  - "[[pattern-saga]]"
  - "[[pattern-transactional-outbox]]"
  - "[[pattern-cqrs]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://microservices.io/patterns/data/database-per-service.html"
  - "Microservices Patterns (Richardson, Manning, 2018) ch. 2 — https://www.manning.com/books/microservices-patterns"
---

## When to use

- Running microservices that must deploy and scale independently.
- Services own distinct bounded contexts with non-overlapping data.
- Schema changes in one service must not block others.
- Different services have different storage needs (relational, document, search).
- Team topology assigns one team per service and its data.

## When NOT to use

- Modular monoliths — shared schema with enforced boundaries is cheaper.
- Reporting or analytics workloads that span all data.
- Teams without capacity to run multiple datastores in production.
- When strong cross-entity transactional consistency is non-negotiable.

## Decision inputs

- Bounded-context map — which data belongs to which service.
- Cross-service query needs and their latency tolerance.
- Operational budget for running N datastores (backup, patch, monitor).
- Cross-service consistency model (sagas, eventual, read-through APIs).
- Reporting strategy — replicate to a warehouse, not join across services.

## Solution sketch

Each service owns its datastore exclusively. No other service reads or writes it directly; all access goes through the owning service's API or via events it publishes. Data shared across services is synchronised asynchronously (events, CDC, replication to a read model) rather than joined at query time.

```
[Service A] -> [DB A]        [Service B] -> [DB B]
     \                             /
      \-- API / events ----------/
```

Cross-service transactions use sagas with compensations, not 2PC. Reporting and analytics extract from each store into a separate warehouse; they do not query operational stores across services. Choose the storage technology per service based on its workload.

## Trade-offs

| Gain | Cost |
|------|------|
| Services deploy, scale, and evolve schemas independently | No cross-service joins — queries become API calls or events |
| Storage technology can match each service's workload | N databases to back up, patch, monitor, secure |
| Failure in one store does not take down others | Cross-service consistency requires sagas or eventual models |
| Clear data ownership aligned to team boundaries | Reporting needs a separate extract/warehouse path |

## Implementation checklist

- [ ] Map bounded contexts to services; write the data ownership down.
- [ ] Forbid direct cross-service database access (network rules, reviews).
- [ ] Choose the persistence technology per service deliberately.
- [ ] Define cross-service consistency strategy (saga, eventual, read API).
- [ ] Set up per-service backup, restore, and patching runbooks.
- [ ] Build or buy an extract path to a shared warehouse for reporting.
- [ ] Document how to add a new service's datastore (paved path).
- [ ] Monitor each store independently; page the owning team only.

## See also

- [[pattern-microservices]] — the architectural style that makes this necessary.
- [[pattern-saga]] — cross-service consistency without distributed transactions.
- [[pattern-transactional-outbox]] — reliable event publication from each service.
- [[pattern-cqrs]] — common pattern for cross-service read models.
