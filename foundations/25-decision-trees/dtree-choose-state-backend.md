---
id: dtree-choose-state-backend
title: Choose a Terraform State Backend
type: decision-tree
maturity: experimental
tags: [decision-tree, experimental, iac, state, backend]
decides_between:
  - "[[pattern-state-isolation]]"
related_patterns:
  - "[[pattern-state-isolation]]"
  - "[[pattern-federated-identity]]"
  - "[[pattern-rbac]]"
criteria:
  - "Primary cloud: AWS, GCP, Azure, multi-cloud, or air-gapped?"
  - "Locking primitive availability and operational comfort"
  - "Integration with existing apply identity (federated trust, IAM/SCP/org-policy reach)"
  - "Operational and licensing cost vs. self-managed maintenance"
  - "Compliance posture: data residency, encryption-at-rest control, audit retention"
  - "Number of stacks and growth trajectory"
sources:
  - "HashiCorp — Backend Configuration — https://developer.hashicorp.com/terraform/language/backend"
  - "HashiCorp — Recommended state storage practices — https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices"
  - "Google Cloud — Best practices for Terraform — https://cloud.google.com/docs/terraform/best-practices-for-terraform"
  - "AWS — Terraform state on S3 with DynamoDB locking — https://developer.hashicorp.com/terraform/language/backend/s3"
---

## Problem

Terraform-compatible engines need a state backend — the storage primitive that persists declared state, supports locking, and gates access. Multiple options exist with distinct cost, locking, and integration profiles. The choice typically follows the IaC engine and primary cloud, but enough variation exists to warrant explicit framing.

## Criteria

- **Primary cloud**: AWS native → S3+DynamoDB; GCP native → GCS; Azure native → Azure Storage; multi-cloud or vendor-managed → Terraform Cloud / Enterprise / Spacelift / env0.
- **Locking primitive**: native (GCS object versioning + native locking, Azure Storage native), bolt-on (S3 + DynamoDB), or service-managed (Terraform Cloud).
- **Identity integration**: backends that align with the cloud's federated-identity primitives reduce the credential-handling surface (GCS + Workload Identity Federation; S3 + IAM role with OIDC).
- **Cost**: cloud-native object storage is cents per stack per month; managed services (Terraform Cloud, Spacelift) are per-seat or per-run priced and add features (UI, run history, RBAC).
- **Compliance**: data residency, customer-managed keys, audit-log retention may dictate the choice in regulated workloads.
- **Stack count**: cloud-native scales linearly with bucket count; managed services typically scale better for hundreds of workspaces.

## Recommendation

| Situation | Backend |
|---|---|
| GCP-primary, Workload Identity Federation in use | **GCS** with native locking — pairs directly with WIF; provider-managed encryption is the default. |
| AWS-primary, IAM/OIDC trust in use | **S3 + DynamoDB** — the canonical Terraform-on-AWS backend; provider-managed encryption defaults. |
| Azure-primary | **Azure Storage** with native locking — same shape as GCS. |
| Multi-cloud, vendor-managed posture acceptable | **Terraform Cloud / Enterprise** — workspace-as-state, run history, RBAC, integrated VCS triggers. |
| Multi-cloud, OSS posture, willing to self-host | Pick one cloud's native backend and use cross-cloud federated trust to read/write. Avoid distributing state across clouds. |
| Air-gapped or on-prem | **Self-hosted** (S3-compatible storage like MinIO + lock service) or vendor on-prem (Terraform Enterprise). |
| Small team, single environment, strong CI integration desired | **Terraform Cloud free tier** — reduces operational overhead until stack count justifies cloud-native. |
| Compliance requires customer-managed keys | Cloud-native backend with CMEK enabled; verify the engine supports it cleanly (Terraform's S3 backend, GCS backend, Azure backend all support CMEK). |

The patterns in this knowledge base ([[pattern-state-isolation]]) assume the chosen backend supports locking, versioning, encryption-at-rest, and IAM scoped to a single apply identity. Any backend lacking those primitives needs compensating controls or a different choice.

## Fallback

When uncertain: **use the primary cloud's native backend** (GCS / S3+Dynamo / Azure Storage). It's the lowest-overhead choice, integrates with federated identity natively, and is well documented. Migrate to a managed service only when state-count growth or cross-team workspace needs justify the cost.
