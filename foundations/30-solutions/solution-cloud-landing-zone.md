---
id: solution-cloud-landing-zone
title: Cloud Landing Zone
type: solution
maturity: experimental
tags: [solution, experimental, iac, landing-zone, foundation, multi-team]
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
applies_to:
  - "[[context-infrastructure-as-code]]"
composes:
  - "[[pattern-blast-radius-scoping]]"
  - "[[pattern-state-isolation]]"
  - "[[pattern-federated-identity]]"
  - "[[pattern-rbac]]"
  - "[[pattern-secrets-management]]"
  - "[[pattern-plan-review-gate]]"
  - "[[pattern-policy-as-code]]"
  - "[[pattern-two-person-apply]]"
  - "[[pattern-module-versioning]]"
  - "[[pattern-immutable-infrastructure]]"
  - "[[pattern-drift-detection]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-correlation-id]]"
prerequisites: []
related: []
sources:
  - "Google Cloud — Enterprise foundations blueprint (Cloud Foundation Fabric / FAST) — https://cloud.google.com/architecture/security-foundations"
  - "AWS — AWS Control Tower / Landing Zone Accelerator — https://aws.amazon.com/solutions/implementations/landing-zone-accelerator-on-aws/"
  - "Microsoft — Azure landing zones — https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/"
  - "Infrastructure as Code: Dynamic Systems for the Cloud Age (Morris, O'Reilly, 2020 2nd ed.) ch. 6 — https://www.oreilly.com/library/view/infrastructure-as-code/9781098114664/"
---

## Problem

A multi-team organisation wants to provision a cloud account ready for production workloads — with security, identity, audit, and isolation baselines in place — without each team reinventing the foundation. The need is for a *system shape* (not a single pattern) that gives every team a scoped place to land, with the org's controls wired in by default.

## Composition

The landing zone is built in sequential stages, each producing a stamp that downstream stages and teams consume.

```
[Stage 0: Bootstrap]
   ├─ folder/account hierarchy           → pattern-blast-radius-scoping
   ├─ state buckets + locking            → pattern-state-isolation
   ├─ federated identity providers       → pattern-federated-identity
   └─ root apply identity (PAM-gated)    → pattern-rbac + pattern-two-person-apply

[Stage 1: Security]
   ├─ org policies / SCPs                → pattern-policy-as-code
   ├─ secrets vault + rotation           → pattern-secrets-management
   └─ audit log aggregation              → pattern-structured-logging + pattern-correlation-id

[Stage 2: Networking + Shared Services]
   ├─ shared ingress projects (narrow scope)         → pattern-blast-radius-scoping
   ├─ network perimeter, DNS, LB                     → (cloud-specific patterns)
   └─ scheduled drift detection                      → pattern-drift-detection

[Stage 3: Workload Stamps (per team / per env)]
   ├─ per-team apply identity (federated)            → pattern-federated-identity + pattern-rbac
   ├─ per-team state backend                         → pattern-state-isolation
   ├─ per-team policy bundle (subset of org policies) → pattern-policy-as-code
   ├─ plan-review-gated CI/CD                        → pattern-plan-review-gate + pattern-two-person-apply
   ├─ pinned module references                       → pattern-module-versioning
   └─ replace-don't-mutate posture                   → pattern-immutable-infrastructure
```

The stamps in stage 3 are produced by a project / account factory that consumes per-team config-as-data. New teams onboard as new stamps.

## Decision inputs

- Cloud target — drives stage 0 hierarchy primitives (folders/projects, OUs/accounts, management-groups/subscriptions).
- Tenant model — single-tenant teams, multi-tenant per stamp, or hybrid?
- Compliance scope — SOC2 / PCI / HIPAA / FedRAMP scope dictates how much of stage 1 is mandatory vs. advisory.
- Team count and growth trajectory — small static teams may skip stage 3's factory and provision stamps explicitly.
- Centralised vs. distributed ownership — does platform own the foundation only, or also each team's stamp interior?

## Trade-offs

| Gain | Cost |
|---|---|
| New teams onboard with controls already in place — no team-by-team security review | Initial bootstrap is multi-quarter work; stage 0 is the highest-risk apply the org will run |
| Apply blast radius bounded to a single stamp by construction | Cross-stamp coordination requires explicit plumbing (cross-stack outputs, shared ingress) |
| Audit posture is uniform across teams | Hierarchy refactors are expensive; pick axes deliberately |
| Compliance evidence accumulates passively from per-stage logs | Stages must be applied in order; out-of-order apply produces broken state |
| Drift detection covers every stamp uniformly | Detector must scale to N stamps; alert-routing per stamp is operational work |

## Implementation sequence

1. **Stage 0 — Bootstrap (one-time, highest stakes).** Create the folder/account hierarchy, the iac-core project housing state buckets and apply identities, and the federated-identity providers. Apply this stage with a documented manual bootstrap; subsequent stages use the federated path. Apply [[pattern-state-isolation]], [[pattern-federated-identity]], [[pattern-rbac]], [[pattern-blast-radius-scoping]].
2. **Stage 1 — Security baselines.** Org policies / SCPs / management-group policies; centralised secrets vault; audit log aggregation. Apply [[pattern-policy-as-code]], [[pattern-secrets-management]], [[pattern-structured-logging]], [[pattern-correlation-id]].
3. **Stage 2 — Shared infrastructure.** Networking, DNS, shared ingress projects, observability stack, drift-detection workflows. Apply [[pattern-drift-detection]] across stages 0–2.
4. **Stage 3 — Per-team stamps.** Project/account factory consumes config-as-data per team; each stamp has its own state, identity, and policy bundle. Apply [[pattern-plan-review-gate]], [[pattern-two-person-apply]], [[pattern-module-versioning]], [[pattern-immutable-infrastructure]].
5. **Steady state.** Drift detection runs scheduled; standards (`standard-pinned-module-refs`, `standard-state-isolation`, `standard-no-long-lived-keys`) enforced via PR review and CI; new teams onboard as factory entries.

## Stage-specific notes

- **At [[stage-prototype]]**: out of scope; landing zones are an mvp+ investment.
- **At [[stage-mvp]]**: stages 0–1 minimum; stage 3 ad-hoc, factory not yet justified.
- **At [[stage-production]]**: full stages 0–3; drift detection scheduled; standards enforced.
- **At [[stage-critical]]**: as production plus tested DR drills per stamp, signed apply artefacts, customer-managed keys where compliance demands.

## See also

- [[context-infrastructure-as-code]] — the context this solution targets.
- [[dtree-choose-iac-engine]] — choose the engine before composing the solution.
- [[dtree-choose-state-backend]] — informs the state-isolation choice in stage 0.
