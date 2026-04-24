---
id: pattern-test-pyramid
title: Test Pyramid
type: pattern
category: testing
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, testing, quality-gates]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
  - "[[context-ml-system]]"
prerequisites: []
related:
  - "[[pattern-contract-testing]]"
  - "[[pattern-deterministic-test-environment]]"
  - "[[pattern-test-double]]"
conflicts_with: []
contradicted_by: []
sources:
  - "The Practical Test Pyramid (Ham Vocke, 2018): https://martinfowler.com/articles/practical-test-pyramid.html"
  - "Write tests. Not too many. Mostly integration. (Kent C. Dodds, 2019): https://kentcdodds.com/blog/write-tests"
---

## When to use

- A codebase that will be maintained and extended — suite shape matters the moment change becomes routine.
- Suite runtime is non-trivial and you need to decide where to spend the budget.
- Flaky or slow tests are eroding trust in the signal and you need to rebalance.
- Starting a new service and deciding how many tests to invest per layer.

## When NOT to use

- Throwaway scripts or spikes where any test costs more than it returns.
- Pure library code where property tests carry most of the weight (see [[pattern-property-based-testing]]).
- I/O-dominated services where unit tests under-detect bugs and integration tests do the real work — consider Dodds' "Testing Trophy" shape instead (contradicted position, not wrong).

## Decision inputs

- Target total suite runtime (Fowler's CI rule of thumb: under 10 minutes for fast feedback).
- Cost of a flaky test at each layer — unit flakes are cheap to fix; e2e flakes burn hours of triage.
- What a given test is actually verifying: behaviour, wiring, or acceptance.
- Which service boundaries are stable enough for [[pattern-contract-testing]] to replace integration tests.
- Test-environment determinism (see [[pattern-deterministic-test-environment]]) — a flaky base makes the shape meaningless.

## Solution sketch

Three layers; width indicates relative test count.

```
     /──\     e2e / acceptance    (slow, few, brittle)
    /────\    integration         (service boundaries, real I/O fakes)
   /──────\   unit                (pure logic, no I/O)
```

Many fast unit tests, fewer integration tests at service seams, very few end-to-end tests for acceptance-critical journeys. The pyramid is a *shape guideline*, not a ratio — the point is that cost rises sharply going up, so each test should sit at the lowest layer that still verifies what matters.

See Vocke for the full treatment. Dodds argues for more integration and fewer unit (the "Testing Trophy"); read both before picking a shape for a new codebase.

## Trade-offs

| Gain | Cost |
|------|------|
| Fast feedback dominated by cheap unit tests | Lower layers miss integration bugs; upper layers still required |
| Refactors don't break most tests because behaviour is tested away from wiring | Shape bias hides the fact that *what* you test matters more than *where* |
| Flaky-test containment is tractable — flakes concentrate at the top, not the base | Assumes function-level units map to behaviour; pure-function codebases may need fewer units and more contract tests |

## Implementation checklist

- [ ] Define the three layers concretely for this codebase (e.g. unit = no Docker; integration = real Postgres via testcontainers; e2e = browser driver against staging).
- [ ] Set a runtime budget per layer; fail CI when a layer exceeds it.
- [ ] Forbid unit tests that boot a database or HTTP server — those belong in integration.
- [ ] Keep e2e suites focused on acceptance-critical user journeys; every e2e costs maintenance forever.
- [ ] Report layer distribution in CI; flag regressions that invert the shape.
- [ ] Pair with [[pattern-deterministic-test-environment]] so every layer is reproducible.

## See also

- [[pattern-contract-testing]] — replaces a class of integration tests at stable service boundaries.
- [[pattern-property-based-testing]] — complements the pyramid for pure-logic code.
- [[pattern-test-double]] — lower layers lean heavily on stubs and fakes.
- [[pattern-deterministic-test-environment]] — flakiness makes the pyramid worthless.
- [[antipattern-flaky-test]] — what happens when determinism slips at any layer.
- [[antipattern-snapshot-overreliance]] — a common failure mode at the top of the pyramid.
- [[pattern-test-data-builder]] — reduces setup noise across the lower layers.
