---
id: pattern-plan-review-gate
title: Plan Review Gate
type: pattern
category: deployment
maturity: experimental
stage_floor: mvp
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, experimental, iac, plan, review, ci, gitops]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites: []
related:
  - "[[pattern-policy-as-code]]"
  - "[[pattern-two-person-apply]]"
  - "[[pattern-federated-identity]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Atlantis — Terraform Pull Request Automation — https://www.runatlantis.io/"
  - "HashiCorp — Terraform Cloud / VCS-driven workflows — https://developer.hashicorp.com/terraform/cloud-docs/run/ui"
  - "Terraform: Up & Running (Brikman, O'Reilly, 2022 3rd ed.) ch. 8 'Production-Grade Infrastructure Code' — https://www.oreilly.com/library/view/terraform-up/9781098116736/"
  - "GitOps Working Group — OpenGitOps Principles — https://opengitops.dev/"
  - "Google Cloud — DevOps Capabilities: Continuous Delivery — https://cloud.google.com/architecture/devops/devops-tech-continuous-delivery"
---

## When to use

- Any IaC repository where reviewers need to see *what changes*, not *what code says might change*.
- Multi-stage foundations where a change in one stage may have non-obvious downstream effects.
- Production environments where unintended deletions or replacements are unacceptable.
- Compliance contexts requiring evidence that every applied change was reviewed against an explicit diff.
- Teams adopting GitOps where the PR is the change-record.

## When NOT to use

- Solo-developer prototypes where the reviewer and the author are the same person.
- Read-only IaC repos (modules-only, with no live state) where there is nothing to plan against.
- Highly exploratory environments where the cost of rendering plans exceeds the value of review.

## Decision inputs

- Where does plan rendering happen — runner-side (CI), service-side (Terraform Cloud, Atlantis), or both?
- Who or what posts the plan output — bot, human, neither? Bot-rendered plans on the PR are the canonical surface.
- Is the plan artefact persisted (audit, replay), or only attached to the PR comment?
- How is plan/apply parity guaranteed — plan artifact pinned and reused at apply, or fresh plan at apply?
- Are sensitive outputs scrubbed from the rendered plan before posting?

## Solution sketch

The PR is the change-request; the plan is the diff under review.

```
PR opened/updated
      │
      ▼
[CI: terraform init + plan]
      │
      ├── plan.out (artefact, pinned)
      ├── plan.txt (human-readable, posted as PR comment)
      └── plan.json (for policy-as-code evaluation)
                          │
                          ▼
              reviewer reads diff + policy results
                          │
                       merge → apply uses pinned plan.out
```

- Generate a *binary* plan artefact (`plan.out`) that apply consumes verbatim — no second plan at apply time.
- Render a human-readable summary as the canonical PR comment; update on every push.
- Apply runs only on merge, against the pinned plan artefact, and only for the merged commit SHA.
- Fail the PR check if the plan artefact is missing, stale, or unsigned.
- Scrub provider-tagged sensitive outputs from the rendered text; keep the binary plan in a access-controlled artefact store.

See Atlantis for an open-source reference implementation; Terraform Cloud and equivalents bake this in.

## Trade-offs

| Gain | Cost |
|---|---|
| Reviewers see exact changes, not inferences from source code | Plan-render time adds to PR latency |
| Apply uses the plan that was reviewed — no surprise drift between review and apply | Pinned plans go stale; cadence of refresh becomes operational concern |
| Audit trail per change is the PR + the plan artefact | Storage cost for plan artefacts and PR-comment archives |
| GitOps-aligned: the PR is the change-record | Bot tooling becomes a critical CI dependency |
| Layers naturally with policy-as-code and two-person-apply | Sensitive-output scrubbing is bespoke per provider |

## Implementation checklist

- [ ] Generate `plan.out` (binary) and `plan.txt` (human-readable) on every PR push.
- [ ] Post or update a single PR comment with the latest plan summary; never spam multiple comments.
- [ ] Persist `plan.out` as a CI artefact, accessible to the apply job.
- [ ] Run apply against the pinned `plan.out` only — refuse to apply with a fresh plan.
- [ ] Tie merge eligibility to a green plan check + required reviewer count.
- [ ] Scrub sensitive outputs (DB passwords, tokens) from the rendered plan text.
- [ ] Fail the PR check if `plan.out` is older than a documented freshness window.
- [ ] Show plan + policy + cost estimate in one consolidated PR comment where possible.

## Stage-specific notes

- **At [[stage-prototype]]**: optional; local `terraform plan` review may be sufficient.
- **At [[stage-mvp]]**: bot-rendered plan on PR is the floor; pinned-artefact apply is recommended.
- **At [[stage-production]]**: pinned `plan.out` consumed at apply, scrubbed text in comment, required reviewer count.
- **At [[stage-critical]]**: signed plan artefacts, multi-approver gates, retained plan artefacts for the compliance window.

## See also

- [[pattern-policy-as-code]] — runs against the same plan artefact; strengthens the gate.
- [[pattern-two-person-apply]] — adds approver requirement on top of the rendered plan.
- [[pattern-federated-identity]] — the identity that posts and applies plans should be federated, not key-based.
- [[principle-deploy-small-and-often]] — small plans are reviewable; large plans are theatre.
