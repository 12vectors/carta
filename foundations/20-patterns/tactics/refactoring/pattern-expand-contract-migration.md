---
id: pattern-expand-contract-migration
title: Expand-Contract Migration (Parallel Change)
type: pattern
category: refactoring
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, refactoring, schema-evolution, migration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
prerequisites: []
related:
  - "[[pattern-strangler-fig]]"
  - "[[pattern-anti-corruption-layer]]"
  - "[[pattern-feature-flag]]"
  - "[[pattern-blue-green-deployment]]"
conflicts_with: []
contradicted_by: []
sources:
  - "ParallelChange (Fowler, 2014) — https://martinfowler.com/bliki/ParallelChange.html"
  - "Refactoring Databases (Ambler & Sadalage, Addison-Wesley, 2006)"
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction"
---

## When to use

- Schema or interface change must ship without downtime or data loss.
- Producers and consumers deploy independently and cannot be updated atomically.
- Rolling deploys, blue-green, or canary mean old and new code run concurrently.
- Data already in production must be preserved through the change.
- The change is larger than "rename" — structural shape is evolving.

## When NOT to use

- Single-process, single-writer systems where an atomic switch is safe.
- Greenfield schemas with no deployed data yet.
- Changes that are purely additive (new optional field) where no migration is needed.
- Teams willing to tolerate a maintenance window; then a straight migration is cheaper.
- Throwaway prototypes where migration cost isn't repaid.

## Decision inputs

- Backward compatibility window — how long must the old shape remain readable?
- Writer count and coordination — single-writer vs. multi-writer across services.
- Data volume — does backfill fit in an online migration or need batching?
- Observability — how is coverage of old vs. new shape measured during the window?
- Contraction trigger — when is it safe to remove the old path?

## Solution sketch

Three phases, each independently deployable:

1. **Expand.** Add the new shape alongside the old. Producers write to both. Consumers read from new if present, else old. Nothing is removed yet.
2. **Migrate.** Backfill existing data into the new shape. Flip consumers to read only from new. Old shape is still written but no longer read.
3. **Contract.** Stop writing the old shape. After a safety window, remove the old fields, columns, or endpoints entirely.

```
t=0  old               t=1  old + new (dual-write)   t=2  new (old removed)
     [schema v1]            [schema v1 + v2]              [schema v2]
     writes:old             writes:both; reads:new        writes:new
     reads:old              (backfill v1→v2 between)      reads:new
```

Each phase is its own deploy. A rollback at any phase goes back to the previous stable state, never forward through an incomplete contract.

## Trade-offs

| Gain | Cost |
|------|------|
| Zero-downtime schema and interface evolution | Three deploys and a coordinated timeline, not one |
| Safe rollback at every phase | Dual-write storage and read-path branching during the window |
| Works across independently-deployed services | Easy to get stuck in "expand" forever — contraction must be scheduled |
| Pairs naturally with feature flags for consumer flips | Requires discipline to clean up the old path after contraction |

## Implementation checklist

- [ ] Design the new shape before starting — expand phase ships with the end state in mind.
- [ ] Make writes additive: producers write both old and new during the dual-write window.
- [ ] Build the backfill as an idempotent, restartable job ([[pattern-idempotency-key]]).
- [ ] Monitor coverage: percentage of rows / messages with the new shape.
- [ ] Flip consumers behind a [[pattern-feature-flag]] so the switch is a config change.
- [ ] Define and schedule the contraction trigger before starting expand — not after.
- [ ] Remove the old shape in its own PR once the safety window closes.
- [ ] Write an ADR recording the old shape's removal; future readers need context.

## See also

- [[pattern-strangler-fig]] — same spirit at the service level; expand-contract is the schema/interface companion.
- [[pattern-anti-corruption-layer]] — protects the new model while dual-reading persists.
- [[pattern-feature-flag]] — the mechanism that flips consumer reads.
- [[pattern-blue-green-deployment]] — schema must be backward-compatible during the flip; expand-contract is how you get there.
- [[pattern-idempotency-key]] — guards the backfill job.
