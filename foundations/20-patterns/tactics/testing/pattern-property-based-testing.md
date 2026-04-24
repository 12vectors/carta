---
id: pattern-property-based-testing
title: Property-Based Testing
type: pattern
category: testing
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, testing, generative]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-ml-system]]"
  - "[[context-agentic-system]]"
prerequisites: []
related:
  - "[[pattern-test-pyramid]]"
  - "[[pattern-contract-testing]]"
conflicts_with: []
contradicted_by: []
sources:
  - "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs (Claessen & Hughes, ICFP 2000): https://www.cse.chalmers.se/~rjmh/QuickCheck/"
  - "Property Tests + Contracts = Integration Tests (Hillel Wayne, 2017): https://www.hillelwayne.com/post/pbt-contracts/"
  - "Hypothesis Docs (Python): https://hypothesis.readthedocs.io/en/latest/"
---

## When to use

- Functions with stateable invariants (round-trip, idempotence, ordering, bounds).
- Parsers, serialisers, encoders, state machines — example tests will miss edge cases.
- Regulatory or financial code where a single slipped input is costly.
- Refactors where you want the old and new implementations compared across many inputs.

## When NOT to use

- Plain CRUD where example tests already cover behaviour cheaply.
- Code whose correctness has no specification — you'll generate noise.
- UI and side-effect-heavy paths where generators are hard to author.
- Performance-sensitive suites — PBT runs hundreds of cases per property.

## Decision inputs

- Can you state an invariant that holds for every valid input?
- How expensive is one invocation (generator cost multiplies)?
- Is a mature library available (Hypothesis, fast-check, QuickCheck, jqwik)?
- Acceptable runtime budget per property (200–500 iterations typical).
- Is contract authoring plausible — contracts + PBT compose per Wayne.

## Solution sketch

A property is a predicate that must hold for every input. The library generates random inputs, shrinks failures to minimal counterexamples, and reports them.

```
property: reverse(reverse(xs)) == xs   for any list xs
library:  run N random xs → report shrunk xs on first failure
```

Contracts + PBT: if a function has contracts, the PBT becomes "no contract violation across the input space."

## Trade-offs

| Gain | Cost |
|------|------|
| Finds edge cases no example test would cover | Requires articulable invariants — many domains lack them |
| Counterexample shrinking yields minimal reproducible failures | Generator authoring is an art; biased generators miss bugs |
| Composes with contracts to cover a huge input space cheaply | Hundreds-of-cases runtime; keep at unit layer |

## Implementation checklist

- [ ] Pick the language's canonical library (Hypothesis, fast-check, QuickCheck, jqwik).
- [ ] State the property; write only the generator it needs.
- [ ] Use built-in strategies before rolling a custom generator.
- [ ] Seed the RNG reproducibly so CI failures are diagnosable.
- [ ] Cap iteration count to keep suite time bounded.
- [ ] Regression-test every shrunk counterexample as an explicit example.

## See also

- [[pattern-test-pyramid]] — PBT lives at the unit or contract layer.
- [[pattern-contract-testing]] — combines cleanly with PBT per Wayne.
