---
id: antipattern-slow-pipeline
title: Slow Pipeline
type: antipattern
category: delivery
maturity: stable
tags: [antipattern, stable, delivery, ci]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
mitigated_by:
  - "[[pattern-fast-feedback-pipeline]]"
related:
  - "[[pattern-test-pyramid]]"
  - "[[antipattern-flaky-test]]"
sources:
  - "Continuous Integration (Martin Fowler, 2024 rev): https://martinfowler.com/articles/continuousIntegration.html"
  - "Continuous Delivery (Humble & Farley, Addison-Wesley 2010) ch. 5"
---

## How to recognise

- PR CI routinely takes >30 minutes.
- Developers push, switch context, and forget the PR — context costs pile up.
- "I'll CI that tomorrow" becomes a habit; main-branch feedback arrives stale.
- Queue waits make [[pattern-trunk-based-development]] infeasible.
- Nobody remembers what a "fast build" felt like; 30 minutes is normalised.

## Why it happens

- Test suite grew without rebalancing; most time spent on a thick upper layer.
- No per-PR vs per-main split — every PR runs the full nightly suite.
- Parallelism unused; tests run serially on a single runner.
- Flaky tests trigger retries that double or triple apparent runtime.
- Caches absent or misconfigured; every run installs from scratch.

## Consequences

- Trunk-based development dies; long-lived branches reappear.
- Developers batch changes to amortise the wait — PRs get larger and harder to review.
- Release cadence drops to what the pipeline can swallow.
- Bug signal arrives hours late; context to fix is gone.

## How to fix

- Apply [[pattern-fast-feedback-pipeline]] — measure, split, parallelise, cache.
- Rebalance the suite per [[pattern-test-pyramid]] — move slow coverage down a layer or out to contracts.
- Quarantine flakes per [[antipattern-flaky-test]] — retries inflate runtime.
- Separate PR gating (fast) from main gating (thorough); do not run the full suite per PR.
- Treat pipeline time as an SLO with its own dashboard and weekly review.

## See also

- [[pattern-fast-feedback-pipeline]] — the remediation pattern.
- [[pattern-test-pyramid]] — reshape the suite before reshaping the pipeline.
- [[antipattern-flaky-test]] — compounding failure mode.
