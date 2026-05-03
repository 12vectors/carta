---
id: pattern-immutable-infrastructure
title: Immutable Infrastructure
type: pattern
category: deployment
maturity: experimental
stage_floor: mvp
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-security]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, experimental, iac, immutable, replace-not-mutate]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites: []
related:
  - "[[pattern-deployment-stamps]]"
  - "[[pattern-state-isolation]]"
  - "[[pattern-drift-detection]]"
  - "[[pattern-module-versioning]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Infrastructure as Code: Dynamic Systems for the Cloud Age (Morris, O'Reilly, 2020 2nd ed.) ch. 4 'Patterns for Defining Infrastructure' — https://www.oreilly.com/library/view/infrastructure-as-code/9781098114664/"
  - "HashiCorp — The Tao of HashiCorp: Immutability — https://www.hashicorp.com/resources/the-tao-of-hashicorp"
  - "Kief Morris — Immutable Server (article, periodically updated) — https://martinfowler.com/bliki/ImmutableServer.html"
  - "Site Reliability Engineering (Beyer et al., O'Reilly, 2016) ch. 8 'Release Engineering' — https://sre.google/sre-book/release-engineering/"
  - "Google Cloud — Best practices for Terraform — https://cloud.google.com/docs/terraform/best-practices-for-terraform"
---

## When to use

- Production resources where reproducibility from declared state is required.
- Environments adopting GitOps where the repo is the source of truth.
- Compliance contexts requiring evidence that no out-of-band change was made.
- Workloads where rebuild-from-zero must be testable on demand.
- Multi-team IaC where mutated resources confuse ownership and audit.

## When NOT to use

- Stateful resources whose data is the value (databases, object stores) — apply immutability to the *configuration*, not the data.
- High-cardinality long-lived resources (massive networks, ML training clusters) where rebuild cost is prohibitive.
- Where vendor primitives don't support replace semantics cleanly (some PaaS resources).

## Decision inputs

- Which resources are safe to replace — stateless compute, networks, IAM bindings?
- Which require in-place mutation due to data — databases, object stores, persistent disks?
- What is the rebuild test cadence — never, on PR, periodic?
- How is `terraform taint` / `terraform state rm` use governed — banned, audited, allowed?
- What replace strategy applies — create-before-destroy, blue-green at the resource level?

## Solution sketch

Replace, don't mutate. The repo declares the desired state; the apply path produces it from zero.

```
declared change
      │
      ▼
[plan]   ─────►  resource diff: replace old, create new
      │
      ▼
[apply]  ─────►  create new resource → switch references → destroy old
                 (lifecycle: create_before_destroy = true where possible)
```

- Use `lifecycle { create_before_destroy = true }` (or equivalent) on resources that can support it.
- Ban manual `terraform taint`, `state rm`, and console edits in production paths; if used, accompany with an ADR and reconciliation step.
- Stateful resources (databases, object stores) hold mutable data but immutable *configuration* — the schema and parameters get replaced; the data persists across rebuilds via backup/restore or detached volumes.
- Periodically rebuild a non-prod environment from zero; treat divergence as a defect.
- Compose with module-versioning so the inputs to the apply are themselves immutable.

See Morris ch. 4 for the patterns; HashiCorp's "Tao" essay for the philosophical framing.

## Trade-offs

| Gain | Cost |
|---|---|
| Resources are reproducible from source — no archeology to debug state | Replace operations have transient unavailability or capacity demand |
| `apply` is the only mutation path, simplifying audit | Resources holding live data need explicit migration plans |
| Drift becomes an exception, not a working mode | Some provider primitives don't support replace cleanly |
| Test "rebuild from zero" exercises real recovery | Periodic rebuilds consume cloud-provider quota |
| Composes naturally with module versioning and state isolation | Forbidding manual surgery slows down emergencies; needs documented break-glass |

## Implementation checklist

- [ ] Set `lifecycle { create_before_destroy = true }` (or equivalent) on resources that can replace cleanly.
- [ ] Ban manual `terraform taint` / `state rm` in production paths; allow only via documented ADR.
- [ ] Catalogue stateful resources separately; document each one's data-migration path on rebuild.
- [ ] Schedule a periodic non-prod rebuild-from-zero exercise; alert on divergence.
- [ ] Reject PRs that introduce manual side-effects (`local-exec`, `null_resource`) without justification.
- [ ] Document a break-glass procedure that uses immutable primitives where possible.
- [ ] Pair with [[pattern-module-versioning]] so module inputs are themselves immutable.

## Stage-specific notes

- **At [[stage-prototype]]**: aspirational; mutation is expected during exploration.
- **At [[stage-mvp]]**: replace-on-rebuild for stateless resources; document stateful exceptions.
- **At [[stage-production]]**: required for stateless production resources; manual mutation banned without ADR.
- **At [[stage-critical]]**: rebuild-from-zero validated on a published cadence; signed apply artefacts.

## See also

- [[pattern-deployment-stamps]] — stamps are the unit at which immutability operates in production.
- [[pattern-state-isolation]] — replacement is meaningful only when the state defining the resource is well-bounded.
- [[pattern-drift-detection]] — surfaces violations of immutability as findings.
- [[pattern-module-versioning]] — the inputs to immutable apply are themselves immutable.
- [[principle-design-for-failure]] — replace-not-mutate is one of the strongest forms of designing for failure.
