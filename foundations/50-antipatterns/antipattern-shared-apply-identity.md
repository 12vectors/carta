---
id: antipattern-shared-apply-identity
title: Shared Apply Identity
type: antipattern
category: security
maturity: experimental
tags: [antipattern, experimental, iac, identity, blast-radius, security]
applies_to:
  - "[[context-infrastructure-as-code]]"
mitigated_by:
  - "[[pattern-rbac]]"
  - "[[pattern-federated-identity]]"
  - "[[pattern-blast-radius-scoping]]"
sources:
  - "NIST SP 800-53 Rev. 5 — AC-6 Least Privilege — https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final"
  - "Google Cloud — Best practices for using service accounts — https://cloud.google.com/iam/docs/best-practices-service-accounts"
  - "AWS — IAM best practices: principle of least privilege — https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"
  - "OWASP — Authorization Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"
---

## How to recognise

- One service account, role, or principal applies infrastructure across multiple teams, environments, or stacks.
- The CI pipeline authenticates as a single identity that holds org-wide or folder-wide privilege.
- IAM bindings on the apply identity grant `roles/owner`, `roles/editor`, or `*:*` across many projects/accounts.
- Audit logs cannot distinguish which team or change caused a given resource mutation — every event traces back to the same principal.
- Onboarding a new team means adding their projects to the existing apply identity's scope, not creating a new identity.

## Why it happens

- Bootstrapping convenience: the team set up one CI identity and never re-scoped it as projects multiplied.
- Avoidance of cloud-IAM complexity: per-team identities require disciplined IAM modelling that takes initial effort.
- Tooling assumption: some CI platforms encourage one credential set per repo; multi-team monorepos collapse to a single principal.
- Org-policy lag: cloud-native primitives for federated identity exist but the bootstrap shortcut never gets revisited.
- "We trust our team" framing: shared identity feels acceptable internally, but the threat model is not just outsiders.

## Consequences

- Compromise of the apply identity is a full-organisation incident, not a per-team incident.
- Per-team blast radius is unbounded — any team's pipeline can mutate any other team's resources.
- Audit logs lose granularity; post-incident attribution requires correlating PR metadata externally to apply events.
- Cross-team mistakes (wrong project specified) succeed instead of failing at the IAM layer.
- Compliance posture suffers: SOC2 and PCI require demonstrated separation of duties, undermined by shared principals.

## How to fix

- Adopt `[[pattern-rbac]]` and `[[pattern-blast-radius-scoping]]`: one apply identity per stack, scoped to that stack's resources only.
- Migrate to `[[pattern-federated-identity]]` so each pipeline authenticates via OIDC trust to a stack-specific principal — no long-lived shared keys.
- Audit existing IAM grants on the shared identity; remove any role that exceeds a single stack's scope.
- Provision per-team apply identities in a central bootstrap stack so creation is auditable and templated.
- Update CI pipelines to authenticate as the per-stack identity; remove the shared credential from secret stores.
- Rotate or delete the shared identity once migration is complete; alert on any regrowth.

## Stage-specific notes

- **At [[stage-prototype]]**: one shared identity is tolerable; document it as bootstrap debt.
- **At [[stage-mvp]] and beyond**: per-environment identities at minimum; per-team where teams exist.
- **At [[stage-production]]**: per-stack identities required; shared identity is a finding.
- **At [[stage-critical]]**: per-stack federated identities, audited per-use, with PAM/JIT gates on apply.

## See also

- [[pattern-rbac]] — the primary mitigation; identity scoping per stack.
- [[pattern-federated-identity]] — eliminates long-lived shared keys.
- [[pattern-blast-radius-scoping]] — identity scoping aligns to the stamp boundary.
- [[pattern-two-person-apply]] — even per-stack identities benefit from a multi-party gate.
- [[principle-least-privilege]] — the principle violated by shared identities.
