---
id: principle-deploy-small-and-often
title: Deploy Small and Often
type: principle
maturity: stable
pillar: "[[pillar-operational-excellence]]"
related_patterns:
  - "[[pattern-health-check-endpoint]]"
  - "[[pattern-deployment-stamps]]"
  - "[[pattern-strangler-fig]]"
tags: [principle, stable, operational-excellence, deployment]
---

## Statement

Ship the smallest change that can work, as often as possible. Big-bang deploys amplify every risk in them.

## Rationale

The blast radius of a deploy scales with the size of the change. Small deploys isolate cause when something breaks, cut review to minutes, and let recovery be a quick revert rather than a forensic investigation. Teams that deploy daily recover faster than teams that deploy monthly, not because their code is better but because their deploy muscle is stronger.

## How to apply

- Break large changes into independently-shippable slices, even when the feature takes weeks.
- Use feature flags to decouple deploy from release.
- Automate rollback; practice it in non-production quarterly.
- Deploy during working hours; a bug at 2pm is cheaper than a bug at 2am.

## Related patterns

- [[pattern-health-check-endpoint]] — orchestrator-driven rolling deploys.
- [[pattern-deployment-stamps]] — deploy to one stamp at a time.
- [[pattern-strangler-fig]] — slice a rewrite into shippable pieces.
