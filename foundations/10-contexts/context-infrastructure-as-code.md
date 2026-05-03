---
id: context-infrastructure-as-code
title: Infrastructure as Code
type: context
maturity: experimental
tags: [context, experimental, iac, infrastructure, declarative]
signals:
  - "The system declares cloud or platform resources in code with a separate plan/apply (or equivalent) execution lifecycle"
  - "A persistent state representation tracks declared vs. actual resources; drift is a measurable risk"
  - "The repository provisions infrastructure rather than serving runtime traffic — no end-user requests hit this codebase"
  - "Apply-time identity holds elevated privilege (organisation, billing, IAM) far broader than any runtime workload it provisions"
  - "Changes are reviewed as code (pull requests) rather than as cloud-console clicks; emergency console changes need reconciliation"
  - "Blast radius is bounded by scope (account, project, folder, namespace), not by request rate"
recommended_patterns:
  - "[[pattern-state-isolation]]"
  - "[[pattern-drift-detection]]"
  - "[[pattern-policy-as-code]]"
  - "[[pattern-plan-review-gate]]"
  - "[[pattern-module-versioning]]"
  - "[[pattern-two-person-apply]]"
  - "[[pattern-blast-radius-scoping]]"
  - "[[pattern-immutable-infrastructure]]"
  - "[[pattern-secrets-management]]"
  - "[[pattern-federated-identity]]"
  - "[[pattern-rbac]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-correlation-id]]"
  - "[[pattern-deployment-stamps]]"
  - "[[pattern-modular-monolith]]"
  - "[[pattern-feature-flag]]"
recommended_standards: []
common_antipatterns:
  - "[[antipattern-state-in-vcs]]"
  - "[[antipattern-shared-apply-identity]]"
  - "[[antipattern-prototype-drift]]"
  - "[[antipattern-silent-failure]]"
related:
  - "[[context-internal-tool]]"
  - "[[context-batch-processing]]"
sources:
  - "Infrastructure as Code: Dynamic Systems for the Cloud Age (Morris, O'Reilly, 2020 2nd ed.) — https://www.oreilly.com/library/view/infrastructure-as-code/9781098114664/"
  - "Terraform: Up & Running (Brikman, O'Reilly, 2022 3rd ed.) — https://www.oreilly.com/library/view/terraform-up/9781098116736/"
  - "Google Cloud — Best practices for Terraform — https://cloud.google.com/docs/terraform/best-practices-for-terraform"
  - "AWS Well-Architected Framework — Operational Excellence Pillar — https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html"
  - "HashiCorp — Terraform recommended practices — https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices"
---

## Description

A repository whose primary output is declared infrastructure, not runtime code. A planning tool — Terraform, OpenTofu, Pulumi, CloudFormation, Bicep, Crossplane — reconciles intent (the code) with reality (provisioned resources). The repo serves no end-user traffic; operators and CI pipelines turn diffs into resources. Apply-time identity holds privilege broader than any runtime workload it provisions, and any change can affect resources nobody recently looked at. Blast-radius containment, identity scoping, and drift management are the central architectural problems.

## Key concerns

- **Apply-time identity is the highest-value credential in the org.** Federate, short-lived, audited per use.
- **Drift is baseline, not exception.** Schedule detection; reconcile, don't ignore.
- **Blast radius is bounded by scope structure** — accounts, projects, folders, liens — not by request rate.
- **Plan output is the safety contract.** PRs without rendered plans are unreviewable.
- **State files are credentials.** Isolate per environment; treat as auth boundaries.
- **Modules version like libraries.** Pin to semver tags; floating refs break reproducibility silently.

## Typical architecture

- **Sequential foundation stages** — org setup → security → networking → workloads, each owning a state slice and a distinct apply identity.
- **Config-as-data factories** — YAML (or equivalent) drives bulk resource creation; lean modules consume the data.
- **Per-team state isolation** — separate state backend per team plus a scoped apply-time identity; cross-team access is explicit IAM.
- **Workload Identity Federation for CI/CD** — pipelines authenticate via OIDC trust, never long-lived keys.
- **Policy-as-code enforcement** — org policies, OPA, Sentinel, or equivalents block disallowed configurations at plan time.
- **Drift detection as a scheduled job** — periodic plan runs alert when reality diverges from declared state.

> [!note] Currency
> Morris (2020) is the canonical technology-agnostic IaC text and remains accurate as of 2026 — its framing of state, drift, and pipeline-driven apply has not been substantively superseded. Brikman (2022) is within the five-year window. The HashiCorp and cloud-vendor links are living documents and authoritative for current practice.

## See also

- [[solution-cloud-landing-zone]] — the pre-composed multi-team foundation built from the patterns above.
- [[dtree-choose-iac-engine]] — pick the engine before composing patterns; affects state, plan/apply semantics.
- [[dtree-choose-state-backend]] — pick the backend that supports the state-isolation pattern in your cloud.
- [[context-internal-tool]] — IaC repos share the first-party, SSO-gated, elevated-credential shape; many tactics carry over.
- [[context-batch-processing]] — plan and apply are batch jobs; scheduled drift checks are batch workloads.
- [[principle-least-privilege]] — apply-time identity scoping is the central application of this principle.
- [[principle-zero-trust]] — every stage authenticates and authorises explicitly; "internal" is not a trust level.
- [[antipattern-prototype-drift]] — IaC repos that never harden (single global state, owner-grade credentials, ad-hoc console changes) drift fastest.
