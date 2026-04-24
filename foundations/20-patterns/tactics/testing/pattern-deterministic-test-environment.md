---
id: pattern-deterministic-test-environment
title: Deterministic Test Environment
type: pattern
category: testing
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, testing, reproducibility]
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
  - "[[pattern-test-double]]"
conflicts_with: []
contradicted_by: []
sources:
  - "xUnit Test Patterns — 'Erratic Test' (Gerard Meszaros, Addison-Wesley 2007)"
  - "Flaky Tests at Google and How We Mitigate Them (John Micco, 2016): https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html"
---

## When to use

- Any suite past trivial size — flakes compound and destroy signal.
- Tests that touch time, randomness, filesystem, network, or shared DB.
- CI-first development where a non-deterministic local pass is worse than no pass.
- When re-running sometimes "fixes" a failing test — determinism is already gone.

## When NOT to use

- Load and chaos tests that require randomness — determinism is an anti-goal there.
- Exploratory test runs against live services that aren't merge-gating.

## Decision inputs

- Sources of non-determinism: clocks, RNG, external network, parallelism, test order.
- Target flake rate (Google's acceptable rate is under ~1.5%).
- Infrastructure for per-test DB/queue isolation (testcontainers, ephemeral schemas).
- Tolerance for "retry on flake" — band-aid, not a fix.

## Solution sketch

Close each non-determinism source:

- **Time** — inject a clock; forbid `now()` on paths under test.
- **Randomness** — seed every RNG deterministically per test.
- **External services** — stub via [[pattern-test-double]] or cover with contract tests; forbid network egress from unit tests.
- **Shared state** — give each test an isolated schema/queue/tempdir; tear down.
- **Ordering** — randomise order but deterministically; fail if order-dependent.

## Trade-offs

| Gain | Cost |
|------|------|
| Green means green; red means a real bug | Every non-determinism source costs infra to close |
| Retries become diagnosis tools, not coping mechanisms | Teams used to flake-as-normal find the tighten-up painful |
| CI gating becomes trustworthy | Parallelism is harder without ordering assumptions |

## Implementation checklist

- [ ] Ban raw clock/RNG access in production code paths reachable from tests.
- [ ] Run the suite in randomised order nightly; fix anything that flakes.
- [ ] Measure flake rate per test; quarantine offenders above threshold.
- [ ] Use testcontainers (or equivalent) for real-DB integration tests.
- [ ] Forbid network egress from unit tests (firewall, sentinel errors on connect).
- [ ] Surface [[antipattern-flaky-test]] offenders; don't silently retry.

## See also

- [[antipattern-flaky-test]] — the failure mode this pattern prevents.
- [[pattern-test-pyramid]] — each layer has its own determinism recipe.
- [[pattern-test-double]] — a primary tool for closing non-determinism.
