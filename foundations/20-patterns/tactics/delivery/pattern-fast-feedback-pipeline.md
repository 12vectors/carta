---
id: pattern-fast-feedback-pipeline
title: Fast-Feedback Pipeline
type: pattern
category: delivery
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, delivery, ci]
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
  - "[[pattern-deployment-pipeline]]"
  - "[[pattern-trunk-based-development]]"
  - "[[pattern-deterministic-test-environment]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Continuous Integration (Martin Fowler, 2024 revision): https://martinfowler.com/articles/continuousIntegration.html"
  - "Continuous Delivery (Humble & Farley, Addison-Wesley 2010) ch. 5"
---

## When to use

- Any team that commits to main more than once a day — slow CI kills the loop.
- Codebases where developers already wait long enough that they switch tasks mid-CI.
- Precondition for [[pattern-trunk-based-development]].
- Remediation for [[antipattern-slow-pipeline]].

## When NOT to use

- Prototype-stage projects where a 30-minute test run is still rare.
- Suites whose correctness cost outweighs speed (safety-critical code, model training runs).

## Decision inputs

- Current median CI time on main and on PR.
- Test-suite layer distribution (see [[pattern-test-pyramid]]) — long suites usually have too much at the top.
- Parallelism budget — CI minutes vs concurrency cost.
- Flakiness rate — retries inflate apparent slowness (see [[antipattern-flaky-test]]).

## Solution sketch

Target: PR pipeline ≤10 minutes, main pipeline ≤20 minutes. Achieve via:

```
                 ┌─ unit tests (sharded, parallel)
PR commit ──►   ─┤─ lint / type-check
                 └─ affected-subset integration tests
                                                    ┌─ full integration
green PR ──► merge ──► main pipeline               ─┤─ contract verification
                                                    └─ deploy to preview / staging
```

Split per-PR (fast, merge-gating) from per-main (thorough, deploy-gating). Parallelise and shard. Cache aggressively. Kill tests that don't earn their time.

## Trade-offs

| Gain | Cost |
|------|------|
| Developers stay in flow — commit, ship, repeat | Parallelism and caching infrastructure to maintain |
| Trunk-based development becomes feasible | Tests must be deterministic and well-isolated |
| Failures land on the author while the change is fresh | Aggressive splitting can hide integration bugs until late |

## Implementation checklist

- [ ] Measure PR pipeline P50 and P95 weekly; set SLOs.
- [ ] Split unit/integration/e2e layers onto distinct jobs that run in parallel.
- [ ] Shard slow test suites; target per-shard runtime under 5 minutes.
- [ ] Cache language and dependency layers; invalidate only on lock-file change.
- [ ] Drop or move any test that consistently exceeds its layer's budget.
- [ ] Gate PRs on the fast path; run thorough suite on main only.

## See also

- [[pattern-deployment-pipeline]] — the fast pipeline feeds into it.
- [[pattern-trunk-based-development]] — requires this pattern in place.
- [[antipattern-slow-pipeline]] — the failure mode this pattern prevents.
