---
id: antipattern-flaky-test
title: Flaky Test
type: antipattern
category: testing
maturity: stable
tags: [antipattern, stable, testing, reliability]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
  - "[[context-ml-system]]"
mitigated_by:
  - "[[pattern-deterministic-test-environment]]"
  - "[[pattern-test-double]]"
related:
  - "[[pattern-test-pyramid]]"
sources:
  - "Flaky Tests at Google and How We Mitigate Them (John Micco, 2016): https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html"
  - "xUnit Test Patterns — 'Erratic Test' (Meszaros, 2007)"
---

## How to recognise

- A test passes or fails on rerun with no code change.
- Developers habitually retry CI to turn red green.
- A "quarantine" suite of known-flaky tests keeps growing.
- Failures disappear in isolation but reappear in the full suite.
- Post-mortems name timing, ordering, or shared resources as the cause.

## Why it happens

- Shared state — DB rows, filesystem, global singletons not reset between tests.
- Real clocks, real network, real RNG used where a test double belongs.
- Parallelism or ordering exposes race conditions absent in isolation.
- Third-party services or LLMs invoked in paths that should be stubbed.
- Sleep-based waits instead of explicit conditions.

## Consequences

- Signal lost — nobody trusts a red result; real bugs ship as "probably flaky".
- CI retries mask genuine regressions and waste compute.
- Onboarding suffers — new developers learn retries are a ritual.
- Team velocity drops around tests no one can reliably diagnose.

## How to fix

- Apply [[pattern-deterministic-test-environment]] — close every non-determinism source.
- Quarantine flakes immediately with a named owner and a deadline.
- Never exit quarantine by adding retries — require a root cause.
- Measure per-test flake rate in CI; block merges that introduce new flakes.
- If the dependency is genuinely environmental, move the test up the pyramid layer where the dependency is real.

## See also

- [[pattern-deterministic-test-environment]] — the primary fix.
- [[pattern-test-double]] — most common structural remedy.
- [[pattern-test-pyramid]] — flakes cluster at the top; rebalance.
