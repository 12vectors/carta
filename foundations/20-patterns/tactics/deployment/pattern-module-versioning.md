---
id: pattern-module-versioning
title: Module Versioning
type: pattern
category: deployment
maturity: experimental
stage_floor: mvp
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, experimental, iac, modules, versioning, semver, supply-chain]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites: []
related:
  - "[[pattern-immutable-infrastructure]]"
  - "[[pattern-plan-review-gate]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Semantic Versioning 2.0.0 — https://semver.org/"
  - "Terraform: Up & Running (Brikman, O'Reilly, 2022 3rd ed.) ch. 8 'Production-Grade Infrastructure Code' — https://www.oreilly.com/library/view/terraform-up/9781098116736/"
  - "HashiCorp — Module Sources — https://developer.hashicorp.com/terraform/language/modules/sources"
  - "HashiCorp — Module Registry Protocol — https://developer.hashicorp.com/terraform/internals/module-registry-protocol"
  - "Google Cloud — Best practices for general style and structure — https://cloud.google.com/docs/terraform/best-practices/general-style-and-structure"
---

## When to use

- IaC consuming modules from any external source (registry, Git, S3/GCS).
- Multi-team environments where one team's module change must not silently propagate to another's apply.
- Production rollouts where a coordinated module upgrade is auditable and rollbackable.
- Compliance contexts requiring reproducibility of every applied change from source.
- Codebases mixing first-party and third-party modules.

## When NOT to use

- Single-repo monoliths with only relative-path module references (already pinned by repo SHA).
- Greenfield exploration where module APIs are still being shaped — pin once stabilised.
- Modules consumed exclusively via a vendored copy in the same repo.

## Decision inputs

- What pinning granularity — semver tag, exact tag, or commit SHA? Tag for libraries, SHA for supply-chain-sensitive contexts.
- Where do modules live — public registry, private registry, Git, vendored — and what auth applies?
- How are upgrades performed — manual PR, dependabot-style automation, scheduled refresh?
- Who decides when a major bump is rolled out, and what reviewer requirement applies?
- Are module versions audited for known-vulnerable bumps before merge?

## Solution sketch

Every module reference pins to a specific version; version sources are explicit; upgrades are reviewed.

```
module "vpc" {
  source = "git::ssh://git@github.com/org/modules.git//net-vpc?ref=v3.2.1"
  # ─────────────────────────────────────────────────────────  ↑
  #                                              pinned semver tag
}
```

- Pin every external module reference to a tag (`?ref=vX.Y.Z`) or exact commit SHA. Never `main`, `master`, or branch refs.
- Adopt SemVer for first-party modules; treat any input/output rename as a major bump.
- Document a module's contract in its README (inputs, outputs, side effects) so consumers can evaluate upgrades.
- Automate upgrade PRs (Dependabot, Renovate, equivalent); humans review, CI tests with the policy bundle.
- Cache module fetches in CI (Terraform plugin cache, registry cache) to avoid upstream outages blocking apply.

See SemVer.org for the contract; HashiCorp's module-sources doc for syntax across Git, registry, S3.

## Trade-offs

| Gain | Cost |
|---|---|
| Reproducible builds — same source produces the same plan | Pin upgrades become discrete, auditable events instead of ambient drift |
| Module changes propagate on a controlled schedule | Lag between module fix and downstream adoption |
| Supply-chain attacks via branch-ref takeover are blocked | Manual upgrade overhead unless automated |
| Easy to roll back a module upgrade — revert the pin | Storage and registry quota grow with version retention |
| CI plan output meaningfully changes only when *intent* changes | Tooling required to detect and alert on floating refs |

## Implementation checklist

- [ ] Replace every `?ref=main` / `?ref=master` / branch ref with a tag or SHA.
- [ ] Add a CI lint that fails on bare or branch refs in `source =` lines.
- [ ] Adopt SemVer for first-party modules; document the input/output contract.
- [ ] Configure Dependabot or Renovate for module bumps; gate on CI pass.
- [ ] Cache module fetches in CI to survive upstream outages.
- [ ] Document the upgrade approval path (who reviews, how rollback works).
- [ ] Audit module versions against published CVE / advisory feeds where applicable.
- [ ] Retire deprecated module versions on a published cadence; communicate to consumers.

## Stage-specific notes

- **At [[stage-prototype]]**: pinning to a tag is acceptable; SHA pinning is overkill.
- **At [[stage-mvp]]**: tag pinning required for external modules; first-party modules adopt SemVer.
- **At [[stage-production]]**: tag pinning everywhere; floating refs fail CI; upgrades reviewed.
- **At [[stage-critical]]**: SHA pinning where supply chain integrity is paramount; signed module artefacts where the registry supports it.

## See also

- [[pattern-immutable-infrastructure]] — module versions are part of what stays immutable.
- [[pattern-plan-review-gate]] — module bumps surface as plan diffs for review.
- [[principle-deploy-small-and-often]] — small, frequent module bumps beat big-bang refactors.
