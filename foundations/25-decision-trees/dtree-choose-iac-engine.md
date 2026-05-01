---
id: dtree-choose-iac-engine
title: Choose an IaC Engine
type: decision-tree
maturity: experimental
tags: [decision-tree, experimental, iac, terraform, opentofu, pulumi, cloudformation, bicep, crossplane]
decides_between:
  - "[[pattern-state-isolation]]"
related_patterns:
  - "[[pattern-state-isolation]]"
  - "[[pattern-module-versioning]]"
  - "[[pattern-immutable-infrastructure]]"
criteria:
  - "Cloud target: single-cloud, multi-cloud, hybrid, or on-prem?"
  - "Team's primary language and skills: HCL, TypeScript/Python/Go, YAML, declarative-only?"
  - "Licensing posture: BUSL-acceptable, OSS-only, or vendor-supported preferred?"
  - "Maturity of ecosystem and module availability for the chosen target"
  - "Integration with existing CI/CD, policy-as-code, and audit tooling"
  - "Migration cost from any existing IaC to the chosen engine"
sources:
  - "HashiCorp — Terraform language overview — https://developer.hashicorp.com/terraform/language"
  - "OpenTofu — https://opentofu.org/"
  - "Pulumi — https://www.pulumi.com/docs/concepts/"
  - "AWS CloudFormation — https://docs.aws.amazon.com/cloudformation/"
  - "Microsoft Bicep — https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview"
  - "Crossplane — https://docs.crossplane.io/"
---

## Problem

The org needs to provision cloud infrastructure declaratively. Multiple IaC engines exist with substantively different language models, licensing, and ecosystems. The choice is sticky — migration after adoption is expensive — so the decision deserves explicit framing.

## Criteria

- **Cloud target**: single-cloud (CloudFormation/Bicep work), multi-cloud (Terraform/OpenTofu/Pulumi/Crossplane), Kubernetes-native (Crossplane).
- **Language model**: HCL (Terraform/OpenTofu), general-purpose programming (Pulumi: TS/Py/Go/.NET), JSON/YAML (CloudFormation), DSL (Bicep), Kubernetes CRDs (Crossplane).
- **Licensing**: post-2023 Terraform is BUSL — restricted in some commercial contexts. OpenTofu is the OSS fork, MPL-2.0. CloudFormation/Bicep are vendor-tied free. Pulumi has a vendor backend with self-hosted alternatives.
- **Ecosystem maturity**: module availability, registry tooling, community size, longevity.
- **Operational integration**: existing CI, policy-as-code engines, audit pipelines. State management primitives differ across engines.
- **Migration cost**: greenfield is free; migrating from one to another is multi-quarter work for non-trivial estates.

## Recommendation

| Situation | Engine |
|---|---|
| Multi-cloud, OSS posture, large existing module ecosystem | **OpenTofu** — drop-in fork of pre-BUSL Terraform; aligns with the IaC patterns in this knowledge base. |
| Multi-cloud, vendor-supported posture acceptable | **Terraform** (current HashiCorp distribution) — same module ecosystem, vendor-backed; check BUSL compatibility with your usage. |
| Multi-cloud, team prefers a general-purpose programming language | **Pulumi** — strong typing, IDE support, but smaller community and a more bespoke state model. |
| AWS-only, deep integration with AWS-native services | **CloudFormation** — but consider Terraform/OpenTofu if other clouds may enter. |
| Azure-only, deep integration with Azure-native services | **Bicep** — same reasoning as CloudFormation for AWS. |
| Kubernetes-native infrastructure, GitOps-first | **Crossplane** — manage cloud resources as K8s CRDs; pairs naturally with Argo/Flux. |
| Greenfield with dual-engine intent (Terraform + OpenTofu) | **OpenTofu primary, Terraform-compatible** — keeps optionality without doubling state-management overhead. |

The patterns and standards in this knowledge base assume a Terraform-compatible engine (Terraform, OpenTofu) for state, plan, and apply semantics. Choosing CloudFormation, Bicep, Pulumi, or Crossplane requires reinterpreting some pattern guidance for that engine's primitives.

## Fallback

When criteria are ambiguous and migration cost is the dominant factor: **stay with what you have**. The cost of moving a non-trivial IaC estate between engines almost always exceeds the marginal benefit of the alternative. Document the choice in an ADR and revisit only when a hard constraint (a cloud the current engine can't reach, a licensing change, a team-skill shift) forces the question.
