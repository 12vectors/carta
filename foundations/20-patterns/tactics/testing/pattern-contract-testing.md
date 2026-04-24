---
id: pattern-contract-testing
title: Contract Testing
type: pattern
category: testing
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, testing, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
prerequisites: []
related:
  - "[[pattern-test-pyramid]]"
  - "[[pattern-test-double]]"
  - "[[pattern-rest-api]]"
  - "[[pattern-async-request-reply]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Consumer-Driven Contracts: A Service Evolution Pattern (Ian Robinson, 2006): https://martinfowler.com/articles/consumerDrivenContracts.html"
  - "Pact Docs: https://docs.pact.io/"
---

## When to use

- Two or more services exchange messages across a stable boundary and must evolve independently.
- Mock-based unit tests are at risk of drifting from real provider behaviour.
- A full e2e environment is too slow for per-commit verification.
- One provider serves multiple consumers and you need to catch breaking changes before release.

## When NOT to use

- Boundaries that change weekly — contract maintenance outweighs the benefit.
- A single deployable where all callers ship together.
- Ad-hoc helpers with only one consumer inside the same codebase.
- Business-rule verification — contracts cover message shape, not provider logic.

## Decision inputs

- Consumer count and how independently each deploys.
- Message format stability (REST, gRPC, event schema).
- Broker availability for contract storage (Pact Broker, Spring Cloud Contract).
- Gating appetite — block on broken contracts, or alert only.
- Provider team's capacity to run reciprocal verification.

## Solution sketch

Consumer-driven variant:

```
Consumer: test asserts "I expect this response shape" → generates a pact file.
Broker:   stores the pact, versioned per consumer + provider.
Provider: replays each consumer pact against its real implementation → verified.
```

Consumer CI fails if its pact changes without coordination. Provider CI fails if its implementation breaks any consumer's pact. See Pact docs for toolchain; Robinson for the design intent.

## Trade-offs

| Gain | Cost |
|------|------|
| Catches breaking boundary changes without a full e2e run | Both sides must adopt the tool and ritual |
| Replaces mocks with executable contracts that can't silently drift | Scope must stay narrow — whole-behaviour contracts explode |
| Enables safe independent deploys | Broker and version management become CI infra |

## Implementation checklist

- [ ] Pick one side to start from — consumer-driven is simpler in microservice meshes.
- [ ] Host contracts in a shared broker with per-commit publishing.
- [ ] Generate pacts on every consumer CI build.
- [ ] Run provider verification against all published consumer pacts.
- [ ] Tag contracts by environment so deploys know which pacts must pass.
- [ ] Keep mocks for *internal* collaborators, contracts for *external* ones.

## See also

- [[pattern-test-pyramid]] — contracts sit between unit and integration.
- [[pattern-rest-api]], [[pattern-async-request-reply]] — the common contract boundaries.
- [[pattern-test-double]] — what contract testing replaces at stable seams.
