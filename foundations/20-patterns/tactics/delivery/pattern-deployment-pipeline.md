---
id: pattern-deployment-pipeline
title: Deployment Pipeline
type: pattern
category: delivery
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, delivery, automation]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
  - "[[context-ml-system]]"
prerequisites:
  - "[[pattern-build-once-deploy-many]]"
related:
  - "[[pattern-fast-feedback-pipeline]]"
  - "[[pattern-preview-environment]]"
  - "[[pattern-canary-release]]"
  - "[[pattern-blue-green-deployment]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Deployment Pipeline (Martin Fowler, 2013): https://martinfowler.com/bliki/DeploymentPipeline.html"
  - "Continuous Delivery (Humble & Farley, Addison-Wesley 2010) ch. 5"
---

## When to use

- Any system deploying to production more than manually — even weekly releases benefit.
- When "release day" carries dread — the pipeline absorbs risk a release meeting can't.
- Regulated environments needing traceability from commit to deployment.
- Any team aiming for continuous delivery (deploy on green).

## When NOT to use

- One-off scripts or pinned-version libraries where a single build-and-publish suffices.
- Truly manual-release environments (firmware, App Store) — the pipeline stops at artefact, human drives the rest.

## Decision inputs

- Stage gates — which environments must the pipeline promote through?
- Approval model — fully automated, manual gate, or mixed?
- Rollback mechanism and target SLO.
- Observability hook — does the pipeline verify post-deploy health?
- Artefact immutability (see [[pattern-build-once-deploy-many]]).

## Solution sketch

Stages run in sequence; each grants more confidence at higher cost.

```
commit ──► build + unit ──► integration + contract ──► deploy staging ──► smoke
                                                                  │
                                                                  ├── canary 1% ──► metrics check ──► canary 25% ──► full
                                                                  │                                      │
                                                                  └──────────────── auto-rollback on breach ◄──
```

Earlier stages are fast and cheap; later stages run less often but catch what earlier stages can't. A commit is not "released" — it's "promoted" through the pipeline.

## Trade-offs

| Gain | Cost |
|------|------|
| Release becomes a routine, not an event | Non-trivial infrastructure; stages must be maintained |
| Every production deploy is traceable to a commit | Tooling lock-in to pipeline definition format |
| Mixes well with [[pattern-canary-release]] and [[pattern-blue-green-deployment]] | Failed rollbacks become a category of incident |

## Implementation checklist

- [ ] Define stages as code (pipeline-as-code: Actions, Jenkinsfile, Azure DevOps YAML).
- [ ] Each stage consumes the same artefact (see [[pattern-build-once-deploy-many]]).
- [ ] Pair staged rollout with a health check; auto-rollback on SLO breach.
- [ ] Emit stage-transition events to a dashboard every team can read.
- [ ] Document the rollback procedure and test it quarterly.
- [ ] Gate production promotions on smoke tests and observability signals, not on calendar time.

## See also

- [[pattern-build-once-deploy-many]] — prerequisite for a sane pipeline.
- [[pattern-fast-feedback-pipeline]] — the pre-stage loop authors live in.
- [[pattern-canary-release]], [[pattern-blue-green-deployment]] — common promotion mechanisms.
- [[pattern-preview-environment]] — per-PR stage bolted on the pipeline.
- [[antipattern-snowflake-ci]] — what happens when pipelines grow bespoke.
