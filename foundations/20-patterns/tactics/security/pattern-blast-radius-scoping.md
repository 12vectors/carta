---
id: pattern-blast-radius-scoping
title: Blast-Radius Scoping
type: pattern
category: security
maturity: experimental
stage_floor: production
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-security]]"
tags: [pattern, experimental, iac, blast-radius, isolation, hierarchy]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites: []
related:
  - "[[pattern-state-isolation]]"
  - "[[pattern-rbac]]"
  - "[[pattern-deployment-stamps]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Google Cloud — Resource hierarchy and security perimeters — https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy"
  - "AWS — Best practices for organizing AWS accounts — https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html"
  - "Azure — Cloud Adoption Framework: Management groups and subscriptions — https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/management-groups"
  - "Site Reliability Engineering (Beyer et al., O'Reilly, 2016) ch. 22 'Addressing Cascading Failures' — https://sre.google/sre-book/addressing-cascading-failures/"
  - "Infrastructure as Code: Dynamic Systems for the Cloud Age (Morris, O'Reilly, 2020 2nd ed.) ch. 6 'Building Environments from Infrastructure Stacks' — https://www.oreilly.com/library/view/infrastructure-as-code/9781098114664/"
---

## When to use

- Multi-team or multi-tenant cloud accounts where one team's mistake must not destroy another's resources.
- Production environments where the cost of a wide outage justifies upfront hierarchy investment.
- Regulated workloads requiring documented isolation between data classifications.
- Multi-environment foundations (dev/stage/prod) needing distinct failure domains.
- Mergers and acquisitions where existing cloud estates must be folded in without flat-merging IAM.

## When NOT to use

- Single-team prototypes — the hierarchy overhead exceeds the isolation benefit.
- Pure dev sandboxes where blast radius is acceptable as part of the working mode.
- Where the cloud provider's hierarchy primitives are too coarse — invest in network or application-layer isolation instead.

## Decision inputs

- What is the smallest unit you would willingly destroy and rebuild — that defines a stamp.
- Which axes drive isolation — environment (dev/prod), tenant, team, region, data classification?
- How are cross-stamp dependencies expressed — explicit data exchange, peering, none?
- What enforcement primitives exist — folder-level org policies, SCPs, network perimeters, separate accounts?
- Who owns each level of the hierarchy and approves changes that cross it?

## Solution sketch

The cloud hierarchy is the failure domain. Each scope has its own apply identity, state, and policies.

```
[Org]
 ├─ [Folder: prod]
 │    ├─ [Project: prod-team-A]   ← stamp; own apply SA, own state, own policies
 │    ├─ [Project: prod-team-B]
 │    └─ [Project: prod-shared-ingress]   ← deliberately shared, narrow scope
 ├─ [Folder: nonprod]
 │    └─ [Project: dev-team-A]
 └─ [Folder: bootstrap]
      └─ [Project: iac-core]      ← state buckets and apply identities live here
```

- Pick the hierarchy axes deliberately (env × team is common; layer in region or tenant where needed).
- Each leaf scope is a stamp with its own apply identity, state, and policy bundle.
- Scope-crossing operations require explicit cross-stack outputs or shared resources hosted in a narrow shared scope (ingress, observability, IaC core).
- Apply liens or deletion-protection on resources whose loss would cascade beyond their scope.
- Document the failure-domain map: a destroyed stamp affects what, recovers in how long, owned by whom.

See Google Cloud's resource-hierarchy guide and AWS's account-organising whitepaper for the canonical patterns; Azure's CAF for the equivalent on that stack.

## Trade-offs

| Gain | Cost |
|---|---|
| One stamp's mistake stays in one stamp | Cross-stamp coordination requires explicit plumbing |
| IAM is naturally scoped to the stamp boundary | Hierarchy refactors are costly — pick axes deliberately |
| Recovery and DR drills happen at stamp granularity | Ops cost grows with stamp count (audit, billing, monitoring) |
| Compliance posture per workload can vary by folder | Ownership ambiguity at folder boundaries needs governance |
| New tenants or teams onboard as new stamps without reshuffling | Bootstrapping the hierarchy takes weeks; reshaping it takes longer |

## Implementation checklist

- [ ] Define hierarchy axes deliberately (env × team × region) and document the rationale.
- [ ] Provision each leaf scope with its own apply identity and state backend.
- [ ] Apply org policies / SCPs / management-group policies at the right hierarchy levels.
- [ ] Apply liens or deletion-protection on cross-stamp shared resources.
- [ ] Document the failure-domain map (what's in each stamp, blast radius if destroyed, recovery owner).
- [ ] Review the hierarchy quarterly; merge or split scopes that no longer fit.
- [ ] Provision shared scopes (ingress, observability, IaC core) deliberately with narrow IAM.
- [ ] Run a tabletop "lose this stamp" exercise per quarter; verify recovery owners and runbooks.

## Stage-specific notes

- **At [[stage-prototype]]**: skip; flat scope is fine.
- **At [[stage-mvp]]**: env-axis isolation (dev/prod separation) is the floor.
- **At [[stage-production]]**: env × team isolation; deletion-protection on shared infrastructure; documented failure-domain map.
- **At [[stage-critical]]**: layer region as a third axis; tested DR drills per stamp; multi-party authorisation on cross-stamp changes.

## See also

- [[pattern-state-isolation]] — per-stamp state is the first concrete realisation of this pattern.
- [[pattern-rbac]] — apply-time identity scoping aligns to the stamp boundary.
- [[pattern-deployment-stamps]] — the runtime-side analogue; same isolation principle, different layer.
- [[principle-design-for-failure]] — the principle this pattern operationalises.
- [[principle-minimize-coordination]] — narrow stamp boundaries reduce coordination by design.
