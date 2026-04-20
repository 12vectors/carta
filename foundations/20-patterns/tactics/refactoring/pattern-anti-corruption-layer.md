---
id: pattern-anti-corruption-layer
title: Anti-Corruption Layer
type: pattern
category: refactoring
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, refactoring, ddd, integration]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-strangler-fig]]"
  - "[[pattern-hexagonal-architecture]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Domain-Driven Design (Evans, Addison-Wesley, 2003)"
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer"
---

## When to use

- Integrating a new clean model with a legacy or third-party system with incompatible semantics.
- During strangler-fig migrations to stop legacy concepts leaking into the new domain.
- Talking to a vendor API whose model should not shape yours.
- Multiple bounded contexts that must interoperate without merging.

## When NOT to use

- Both sides already share the same domain model and language.
- Trivial integrations where a direct adapter is simpler and the cost is negligible.
- Throwaway or short-lived integrations.
- When the legacy model *is* acceptable — do not add a layer for its own sake.

## Decision inputs

- Translation surface — commands, queries, events, or all three.
- Placement — own service, sidecar, or in-process module.
- Ownership — new side owns the ACL (usual) vs. shared team.
- Failure semantics — legacy unavailability must not corrupt new-side state.
- Contract versioning for both sides.

## Solution sketch

Place a dedicated translation module between the new (clean) model and the legacy/external model. It owns the mapping: field renames, type coercions, semantic reconciliation, and error-code translation. The new side speaks **only** to the ACL, never to the legacy directly. The ACL may call legacy via HTTP, DB, message, or client library — that is its concern, not the domain's.

```
[new domain] --clean commands/events--> [ACL] --legacy calls--> [legacy system]
```

See Evans ch. 14 for the DDD framing and the Microsoft docs for a cloud-centric example.

## Trade-offs

| Gain | Cost |
|------|------|
| New domain stays clean regardless of legacy shape | Extra module or service to build and operate |
| Single place to absorb legacy semantic drift | Translation can become a bottleneck or coupling hub |
| Enables parallel evolution of both sides | Easy to underestimate mapping complexity |
| Natural home for legacy-specific retry and fallback | Adds a hop — latency and failure mode |

## Implementation checklist

- [ ] Define the clean domain model first, independent of legacy.
- [ ] Enumerate commands, queries, and events crossing the boundary.
- [ ] Document every field mapping and semantic reconciliation.
- [ ] Isolate the ACL — no legacy types in the new domain's code.
- [ ] Handle legacy failures at the ACL; expose clean-domain errors outward.
- [ ] Version the clean contract independently of the legacy.
- [ ] Test with legacy contract tests and new-domain unit tests separately.
- [ ] Plan ACL retirement once legacy is gone (strangler-fig end state).

## See also

- [[pattern-strangler-fig]] — ACL commonly sits between new and legacy during migration.
- [[pattern-hexagonal-architecture]] — the ACL is an adapter on the outside of the hexagon.
