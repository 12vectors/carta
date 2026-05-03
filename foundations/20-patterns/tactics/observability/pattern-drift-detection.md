---
id: pattern-drift-detection
title: Drift Detection
type: pattern
category: observability
maturity: experimental
stage_floor: production
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-security]]"
tags: [pattern, experimental, iac, drift, reconciliation, observability]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites:
  - "[[pattern-state-isolation]]"
related:
  - "[[pattern-rbac]]"
  - "[[pattern-federated-identity]]"
  - "[[pattern-structured-logging]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Infrastructure as Code: Dynamic Systems for the Cloud Age (Morris, O'Reilly, 2020 2nd ed.) ch. 19 'Team Workflow' — https://www.oreilly.com/library/view/infrastructure-as-code/9781098114664/"
  - "Terraform: Up & Running (Brikman, O'Reilly, 2022 3rd ed.) — https://www.oreilly.com/library/view/terraform-up/9781098116736/"
  - "HashiCorp — Detecting drift in Terraform — https://developer.hashicorp.com/terraform/tutorials/state/resource-drift"
  - "Google Cloud — Best practices for Terraform — https://cloud.google.com/docs/terraform/best-practices-for-terraform"
  - "AWS — Detecting unmanaged configuration changes (CloudFormation drift detection) — https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html"
---

## When to use

- Production IaC where the cloud account also accepts manual changes (console, CLI, third-party tools).
- Multi-stage foundations where one stage's drift can break a downstream stage's plan.
- Compliance regimes (SOC2, PCI, HIPAA) requiring evidence that declared state matches reality.
- Any environment where break-glass changes happen and need reconciliation back to code.
- Codebases where `terraform import` or `terraform state` is used regularly to absorb out-of-band changes.

## When NOT to use

- Prototype or single-developer environments where drift is the working mode.
- Pure module-only repositories with no live infrastructure.
- Environments where the cloud account is locked down so tightly that no out-of-band change is possible — drift cannot occur, detection is overhead.

## Decision inputs

- What is the cadence at which drift is likely to occur (continuous, weekly, episodic)?
- Who is allowed to make out-of-band changes, and is that policy actually enforced?
- What detection latency is acceptable — minutes (alerting), hours (daily), days (weekly)?
- Should the detector auto-revert, file a ticket, page on-call, or just record?
- What identity does the detector run as, and is it scoped to read-only?
- Are partial plans (one stage drifted, others clean) tolerable, or must the report be account-wide?

## Solution sketch

A scheduled, read-only `plan` against every managed stack. Non-empty plans are alerts.

```
[scheduled trigger]
       │
       ▼
[plan-only identity per stack]   ← read-only credentials, never apply
       │
       ▼
[terraform plan / pulumi preview]
       │
       ├── empty plan  → record success, exit
       └── non-empty   → emit structured event:
                          { stack, run_id, resource_diffs, severity }
                          → alert / ticket / dashboard
```

- Run the detector on a fixed cadence (cron, scheduled workflow, control-plane job) — daily for production foundations, hourly for compliance-critical surfaces.
- Use a **plan-only identity** (separate from the apply identity) with read permissions on the cloud and the state backend. Never give the detector write or apply permissions.
- Emit structured findings — stack id, run correlation id, list of drifted resources, severity. Route to the same observability sink as apply-time logs.
- Treat a non-empty plan as a finding to acknowledge: either reconcile (re-apply, revert console change, or import) or record an explicit accept-as-drift decision.

See HashiCorp's drift-detection tutorial for backend-specific patterns and the AWS CloudFormation drift docs for the equivalent on that stack.

## Trade-offs

| Gain | Cost |
|---|---|
| Drift becomes a known signal rather than an incident-time discovery | Scheduling overhead and a separate plan-only identity to provision |
| Compliance evidence accumulates passively | Noisy first runs while existing drift is reconciled |
| Catches benign drift early before it cascades into broken plans | False positives from provider-side eventual-consistency or read-after-write skew |
| Detector can run with a constrained read-only identity | Read-only plan still consumes API quota and rate budget |
| Structured findings integrate into existing alerting and ticketing | Action policy (auto-revert vs ticket vs page) needs deliberate org choice |

## Implementation checklist

- [ ] Provision a plan-only identity per stack, scoped to the resources that stack manages.
- [ ] Schedule `terraform plan` (or equivalent) against every managed stack at a documented cadence.
- [ ] Emit structured findings — include stack id, run id, drifted resources, severity, timestamp.
- [ ] Route findings into the org's observability and alerting pipeline (audit log + dashboard + on-call alert per severity).
- [ ] Define an action policy per severity (auto-ticket, page, info-only) and document it in an ADR.
- [ ] Capture each accepted drift as either a code reconciliation, a `terraform import`, or an explicit accept-as-drift ADR.
- [ ] Record detector liveness — alert when the scheduled job itself fails to run.
- [ ] Periodically rotate the plan-only identity's credentials (or use federated identity).

## Stage-specific notes

- **At [[stage-prototype]]**: skip — drift is the working mode.
- **At [[stage-mvp]]**: optional; a manual `terraform plan` before each apply often suffices.
- **At [[stage-production]]**: required. Daily cadence minimum, structured findings, alerting on non-empty plans.
- **At [[stage-critical]]**: hourly cadence, paged on novel drift, audit-tracked acknowledgement of every finding, retention of detector output for compliance windows.

## See also

- [[pattern-state-isolation]] — the plan-only identity per stack is a corollary of state isolation.
- [[pattern-rbac]] — the detector identity must be read-scoped; this pattern provides the scoping mechanism.
- [[pattern-federated-identity]] — the detector should authenticate via OIDC, not long-lived keys.
- [[pattern-structured-logging]] — drift findings are observability signals; emit them through the same pipeline.
- [[antipattern-prototype-drift]] — what happens when this pattern is absent.
- [[principle-observe-before-optimising]] — drift detection is the IaC-shaped form of "measure before you change".
