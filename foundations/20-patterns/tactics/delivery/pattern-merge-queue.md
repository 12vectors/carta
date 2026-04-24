---
id: pattern-merge-queue
title: Merge Queue
type: pattern
category: delivery
maturity: stable
stage_floor: production
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, delivery, scaling]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-internal-tool]]"
prerequisites:
  - "[[pattern-fast-feedback-pipeline]]"
related:
  - "[[pattern-trunk-based-development]]"
conflicts_with: []
contradicted_by: []
sources:
  - "GitHub Merge Queue Docs: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request-with-a-merge-queue"
  - "Patterns for Managing Source Code Branches (Martin Fowler, 2020): https://martinfowler.com/articles/branching-patterns.html"
---

## When to use

- Main breaks often because two PRs pass CI independently but fail when combined.
- Merge volume on a shared service is high enough that manual rebase-and-merge is painful.
- The team is already on [[pattern-trunk-based-development]] and needs to preserve an always-green main.
- You want to batch-CI merges rather than run a full pipeline per PR serially.

## When NOT to use

- Low-traffic repositories where manual rebase is fine.
- Monorepos with strict build slicing where conflicts are already physically impossible.
- Release-branch workflows where main isn't the integration point.

## Decision inputs

- Main-break frequency from mid-air collisions.
- Merge cadence — queue shines above ~20 merges/day on one repo.
- CI minute budget — queue batching saves CI but adds latency.
- Queue-tool availability (GitHub, Graphite, Mergify, Bors).

## Solution sketch

```
PR approved ──► enter queue ──► queue rebases on queue head, runs CI batch ──► merge
                                                   │
                                                   └─ on failure, eject PR; next one picks up
```

The queue serialises the merge point. Each PR gets tested against the current queue head before merging, eliminating mid-air collisions. Batching multiple PRs through one CI run is a common optimisation.

## Trade-offs

| Gain | Cost |
|------|------|
| Main stays green despite high merge volume | PRs wait in queue — p95 time-to-merge grows |
| No manual rebase-and-retry loops | Requires fast, deterministic CI to avoid queue stalls |
| CI minutes drop through batching | Queue tool becomes part of the delivery critical path |

## Implementation checklist

- [ ] Enable the queue in your code host (GitHub, etc.) or install Bors/Mergify.
- [ ] Require the queue for the default branch; disable direct merges.
- [ ] Set queue CI timeout below the team's acceptable wait.
- [ ] Monitor queue depth and median wait time; alert on stalls.
- [ ] Keep [[pattern-fast-feedback-pipeline]] tight — queue amplifies any CI slowness.
- [ ] Reserve queue bypass for documented hotfix paths only.

## See also

- [[pattern-trunk-based-development]] — merge queue makes trunk-based viable at scale.
- [[pattern-fast-feedback-pipeline]] — hard prerequisite; slow CI destroys queue UX.
