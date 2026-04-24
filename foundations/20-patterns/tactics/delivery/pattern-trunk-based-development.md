---
id: pattern-trunk-based-development
title: Trunk-Based Development
type: pattern
category: delivery
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, delivery, branching]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
  - "[[context-ml-system]]"
prerequisites:
  - "[[pattern-fast-feedback-pipeline]]"
related:
  - "[[pattern-feature-flag]]"
  - "[[pattern-merge-queue]]"
  - "[[pattern-deployment-pipeline]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Trunk Based Development (Paul Hammant): https://trunkbaseddevelopment.com/"
  - "Patterns for Managing Source Code Branches (Martin Fowler, 2020): https://martinfowler.com/articles/branching-patterns.html"
---

## When to use

- Teams that want continuous integration in its original sense — everyone merges to main at least daily.
- Codebases where release cadence is hours or days, not weeks.
- Services that ship features behind [[pattern-feature-flag]] so half-done work lands safely.
- Teams paying the cost of long-lived feature branches in merge conflicts.

## When NOT to use

- Shipped products with hard version boundaries (libraries, OS, embedded) that need release branches for patch support.
- Organisations whose compliance process gates on long-lived review branches.
- Very small teams where branch strategy debate outweighs the wins.

## Decision inputs

- Team's feature-flag discipline — trunk-based without flags ships half-done work.
- CI speed — a 30-minute pipeline kills trunk-based flow (see [[pattern-fast-feedback-pipeline]]).
- Test-suite determinism (see [[pattern-deterministic-test-environment]]).
- Release-branch requirement for supported versions.
- Team's appetite for small, frequent commits vs larger coordinated merges.

## Solution sketch

```
main ─────●───●───●───●───●───●─────►
           \   \   \   \   \   \
            small short-lived feature branches, each merged within ~1 day
            unfinished work hidden behind feature flags
```

Branches exist for review and CI, not for feature accumulation. Flags gate incomplete behaviour. Release cuts (if any) branch off main, patches cherry-pick back — main never waits for a release.

## Trade-offs

| Gain | Cost |
|------|------|
| Continuous integration in practice, not just in name | Requires feature flags, fast CI, and strong test discipline |
| Merge-conflict volume drops sharply | Teams must trust each other's partial work on main |
| Release readiness is continuous | Operational gate moves from merge to deploy, which must be trustworthy |

## Implementation checklist

- [ ] Cap branch age — delete or merge any branch older than a few days.
- [ ] Require feature flags for any user-visible change still in progress.
- [ ] Ensure CI median under 10 minutes (Fowler rule) on main.
- [ ] Protect main with required status checks, not manual gatekeeping.
- [ ] If supported releases are required, branch at release time only; never pre-cut.
- [ ] Pair with [[pattern-merge-queue]] once merge contention becomes the bottleneck.

## See also

- [[pattern-feature-flag]] — hides in-progress work on main.
- [[pattern-fast-feedback-pipeline]] — prerequisite for sane trunk-based flow.
- [[pattern-merge-queue]] — serialises merges once team scale demands it.
- [[pattern-deployment-pipeline]] — what a green main feeds into.
