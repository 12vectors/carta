---
id: pattern-state-isolation
title: State Isolation
type: pattern
category: security
maturity: experimental
stage_floor: mvp
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
tags: [pattern, experimental, iac, state, blast-radius, security]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites: []
related:
  - "[[pattern-secrets-management]]"
  - "[[pattern-rbac]]"
  - "[[pattern-federated-identity]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Terraform: Up & Running (Brikman, O'Reilly, 2022 3rd ed.) ch. 3 'How to Manage Terraform State' — https://www.oreilly.com/library/view/terraform-up/9781098116736/"
  - "HashiCorp — Terraform Backend Configuration — https://developer.hashicorp.com/terraform/language/backend"
  - "HashiCorp — Recommended Practices: state — https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices"
  - "Google Cloud — Best practices for Terraform — https://cloud.google.com/docs/terraform/best-practices-for-terraform#use_remote_state"
  - "AWS Prescriptive Guidance — Terraform state file management — https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/"
---

## When to use

- Multi-environment IaC (dev/stage/prod) where one env's state must not be readable from another's apply identity.
- Multi-team IaC where each team owns a distinct state slice and apply identity.
- Production state contains resource IDs, sensitive outputs, or credentials — treat as auth boundary.
- Multi-stage foundations (org → security → networking → workloads) where each stage owns its state.
- Compliance-bound environments (SOC2/PCI/HIPAA) requiring per-workload secrets and state separation.

## When NOT to use

Never skip in any production-bound IaC. Choose intensity instead:

- Solo-developer single-environment prototype on a laptop — local backend is acceptable temporarily.
- Pure module-only repositories with no live infrastructure (no state to isolate).
- Single-stack prototypes that will never touch production credentials.

## Decision inputs

- How many environments and teams need separate apply identities and state slices?
- What blast radius is acceptable if a single state backend is compromised or corrupted?
- Does state hold sensitive outputs (DB passwords, generated keys) or only resource IDs?
- What locking primitive does the backend support (DynamoDB, GCS object versioning, native)?
- Are there regulatory or compliance constraints that mandate customer-managed keys, or does provider-managed encryption meet the bar?
- What is the break-glass path for emergency state surgery, and is it audited?

## Solution sketch

One backend per stack — never shared across teams or environments. The state backend is treated as an auth boundary: only the apply identity for that stack can read or write it.

```
[apply identity: team-A]            [apply identity: team-B]
        │                                       │
        ▼                                       ▼
[state bucket: team-A]              [state bucket: team-B]
  ↳ provider-managed encryption       ↳ provider-managed encryption
  ↳ IAM: team-A apply SA only         ↳ IAM: team-B apply SA only
  ↳ versioning + locking              ↳ versioning + locking
  ↳ access audited                    ↳ access audited
```

- One backend per stack (env × team × stage); cross-stack outputs are explicit (e.g. `terraform_remote_state`, parameter store).
- Rely on provider-managed encryption at rest (default in modern backends — GCS, S3, Azure Storage, Terraform Cloud); enforce TLS in transit.
- Scope IAM on each state backend to a single apply identity; never to humans or other workloads.
- Enable versioning and object locking so concurrent writes cannot corrupt state.
- Audit log every state read; sensitive outputs in state are credentials.
- Provision the state backends themselves from a separate bootstrap stack with its own credentials.

See HashiCorp's recommended-practices doc for backend selection per cloud.

## Trade-offs

| Gain | Cost |
|---|---|
| Compromise of one state file does not expose others | More backends to provision, audit, rotate |
| Per-team apply identity scopes naturally to its own state slice | Cross-stack outputs require explicit plumbing |
| Provider-managed encryption is on by default — no key-rotation overhead, no lockout risk | Org loses the explicit kill-switch that customer-managed keys provide; not sufficient for some compliance regimes |
| Versioning + locking prevents two-engineer concurrent-apply corruption | Backend cost grows with the number of stacks |
| Audit log per state read makes sensitive-output exposure detectable | Audit volume grows; needs retention and alerting policy |

## Implementation checklist

- [ ] One backend per stack (env × team × stage); never share state across teams or environments.
- [ ] Provision state backends from a separate bootstrap stack with its own credentials.
- [ ] Verify provider-managed encryption at rest is enabled (default in modern backends); enforce TLS in transit.
- [ ] Scope IAM on each state backend to a single apply identity; deny human direct access by default.
- [ ] Enable versioning and locking on the state backend.
- [ ] `.gitignore` `*.tfstate`, `*.tfstate.backup`, and `.terraform/` in every IaC repo.
- [ ] Audit log every state read; alert on unexpected access patterns or principals.
- [ ] Document break-glass (who, how, audit-trail) for emergency state surgery.
- [ ] Periodically test a bootstrap-from-zero in dev to confirm the bootstrap stack still works.

## Stage-specific notes

- **At [[stage-prototype]]**: local backend acceptable, but never with production resources or credentials.
- **At [[stage-mvp]]**: remote backend per environment, provider-managed encryption, gitignored; per-team isolation can wait.
- **At [[stage-production]]**: per-stack backend, provider-managed encryption, versioning, locking, scoped IAM, audited reads.
- **At [[stage-critical]]**: production baseline plus formal break-glass with multi-approver, periodic backend-replication test, documented RTO/RPO; customer-managed keys when compliance (FedRAMP High, PCI-DSS Level 1) demands them.

## See also

- [[pattern-secrets-management]] — state files are credentials; the same vault-handling rules apply.
- [[pattern-rbac]] — apply-time identity scoping is what makes per-stack state meaningful.
- [[pattern-federated-identity]] — the apply identity reading state should be federated, not key-based.
- [[principle-least-privilege]] — the principle this pattern operationalises for state access.
- [[principle-defence-in-depth]] — backend IAM, CMEK, versioning, and audit are layered defences.
