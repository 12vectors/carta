---
id: pattern-test-double
title: Test Double
type: pattern
category: testing
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, testing, isolation]
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
  - "[[pattern-test-pyramid]]"
  - "[[pattern-deterministic-test-environment]]"
  - "[[pattern-contract-testing]]"
conflicts_with: []
contradicted_by: []
sources:
  - "xUnit Test Patterns (Gerard Meszaros, Addison-Wesley 2007) — chapters on Test Double, Test Stub, Mock Object, Fake Object"
  - "Mocks Aren't Stubs (Martin Fowler, 2007): https://martinfowler.com/articles/mocksArentStubs.html"
---

## When to use

- A collaborator's real implementation is slow, non-deterministic, or cost-bearing (DB, network, LLM, clock).
- You need to assert *how* code interacts with a collaborator (mock) or *what* it does given a collaborator's response (stub).
- You're writing a unit test and want to isolate the system under test from transitive dependencies.
- You need a lightweight in-process substitute (fake) for a real dependency to keep tests fast.

## When NOT to use

- Integration tests verifying the real wiring — use real implementations or high-fidelity fakes (e.g. testcontainers), not mocks.
- Contract-critical boundaries where the test should fail if the real service changes — use [[pattern-contract-testing]] instead.
- Pure functions with no collaborators — doubles add noise and prove nothing.
- When a double duplicates all the real behaviour to stay accurate — at that cost, use the real thing.

## Decision inputs

- What the test is asserting: state (stub), interaction (mock), or behaviour-through-substitute (fake).
- Cost of drift between the double and the real collaborator (mocks rot faster than fakes).
- Whether a contract test already covers the boundary you're doubling.
- Whether the real collaborator can be made fast and deterministic instead (often the better answer).
- Team familiarity with mocking libraries vs. hand-rolled fakes.

## Solution sketch

Five kinds, per Meszaros / Fowler:

| Kind | Purpose | Asserts |
|------|---------|---------|
| **Dummy** | Fill a parameter slot, never used | Nothing |
| **Stub** | Return canned data on call | State of system under test |
| **Spy** | Stub + record calls for later assertion | Both state and interaction |
| **Mock** | Pre-configured expectations verified on teardown | Interaction (verified automatically) |
| **Fake** | Working substitute with shortcuts (in-memory DB, map-based cache) | State, via a real implementation |

Pick the lightest kind that answers the test's question. Start with a stub; upgrade to a mock only when *how* the collaborator is called is the behaviour under test. Fakes pay off when the same substitute is reused across many tests.

See Fowler for the classical-vs-mockist debate; Meszaros for the full catalogue.

## Trade-offs

| Gain | Cost |
|------|------|
| Tests run fast and deterministically — no real DB, network, or LLM call | Doubles drift from real collaborators; green tests can pass while prod fails |
| Isolates the unit, so failures point at the unit under test | Overused mocks lock tests to implementation detail, punishing refactors |
| Shifts tests to the base of the pyramid where feedback is cheap | Fakes are real code that needs its own test coverage |
| Enables testing error paths that real collaborators rarely produce | Mock-heavy suites test the test doubles, not the system |

## Implementation checklist

- [ ] Pick the double kind that matches the assertion — stub for state, mock for interaction, fake for behaviour.
- [ ] Never mock types you do not own — wrap third-party libraries in an owned interface first (per GOOS).
- [ ] When a double duplicates non-trivial real behaviour, replace it with a high-fidelity fake or the real collaborator.
- [ ] Pair mocks with a [[pattern-contract-testing]] run so the double doesn't drift from the real contract.
- [ ] Ban mocks in integration and e2e tests — they belong at the unit layer of [[pattern-test-pyramid]].
- [ ] Keep fakes in a shared test-support module so they evolve once, not per test file.

## See also

- [[pattern-test-pyramid]] — doubles belong at the base.
- [[pattern-contract-testing]] — the safety net for mocked boundaries.
- [[pattern-deterministic-test-environment]] — doubles are one tactic for determinism among several.
- [[antipattern-flaky-test]] — overuse of real collaborators in unit tests is a top flakiness source.
