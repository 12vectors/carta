---
id: principle-automate-everything-repetitive
title: Automate Everything Repetitive
type: principle
maturity: stable
pillar: "[[pillar-operational-excellence]]"
related_patterns:
  - "[[pattern-health-check-endpoint]]"
  - "[[pattern-structured-logging]]"
tags: [principle, stable, operational-excellence, automation]
---

## Statement

If you've done it twice manually, script it. If you've scripted it twice, make it self-serve. Toil scales poorly.

## Rationale

Manual operations drift, miss steps, and don't scale with system footprint. Worse, they concentrate knowledge in the operator — a staffing risk and a bus-factor problem. Automation is a one-time cost that pays back for every subsequent run and makes operations reviewable, testable, and auditable.

## How to apply

- Every production change goes through CI/CD, not a shell prompt.
- Runbooks are executable, not prose — scripts, not wikis.
- Observability, deploys, and recovery actions are self-serve for developers.
- Track toil: estimate hours per quarter spent on manual ops; target it for automation.

## Related patterns

- [[pattern-health-check-endpoint]] — let the orchestrator handle restart loops.
- [[pattern-structured-logging]] — make log-based automation and alerting possible.
