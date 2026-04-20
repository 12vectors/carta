---
id: pillar-operational-excellence
title: Operational Excellence
type: pillar
maturity: stable
tags: [pillar, stable, operational-excellence]
realised_by:
  - "[[principle-automate-everything-repetitive]]"
  - "[[principle-observe-before-optimising]]"
  - "[[principle-deploy-small-and-often]]"
tradeoffs_with:
  - "[[pillar-cost]]"
sources:
  - "https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/"
  - "https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/"
---

## Description

Operational excellence is the system's ability to run, change, and recover predictably. It covers deployment, observability, incident response, runbooks, automation, and the feedback loops that let the team improve the system over time.

## When this dominates

- Systems with frequent change and low tolerance for deployment-induced regressions.
- Platforms supporting many teams or many environments, where operational load scales with footprint.
- Mission-critical services where mean time to detect and mean time to recover dominate availability maths.

## Trade-offs

| Gain | Cost |
|------|------|
| Faster, safer change through automation and observability | Tooling, CI, and monitoring infrastructure add up ([[pillar-cost]]) |
| Lower MTTR through runbooks and automated recovery | Maintaining those runbooks is continuous work |
| Confidence to deploy small and often | Upfront investment in test automation and release tooling |

## Realised by

- [[principle-automate-everything-repetitive]] — manual toil scales poorly.
- [[principle-observe-before-optimising]] — instrument first; guess never.
- [[principle-deploy-small-and-often]] — shrink the blast radius of each change.
- [[pattern-structured-logging]], [[pattern-distributed-tracing]], [[pattern-health-check-endpoint]] — patterns that realise these principles.
