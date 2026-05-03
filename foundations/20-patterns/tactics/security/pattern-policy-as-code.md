---
id: pattern-policy-as-code
title: Policy as Code
type: pattern
category: security
maturity: experimental
stage_floor: production
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
tags: [pattern, experimental, iac, policy, opa, sentinel, governance]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites:
  - "[[pattern-plan-review-gate]]"
related:
  - "[[pattern-rbac]]"
  - "[[pattern-state-isolation]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Open Policy Agent — https://www.openpolicyagent.org/docs/latest/"
  - "Conftest — Test your configuration files — https://www.conftest.dev/"
  - "HashiCorp Sentinel — https://developer.hashicorp.com/sentinel"
  - "Google Cloud — Organization Policy Service — https://cloud.google.com/resource-manager/docs/organization-policy/overview"
  - "AWS — Service Control Policies — https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html"
---

## When to use

- Regulated environments (SOC2, PCI, HIPAA, FedRAMP) needing auditable, automated guardrails.
- Multi-team IaC where central platform standards must be enforced uniformly.
- Production foundations where post-apply discovery of forbidden config is unacceptable.
- Cost guardrails (no oversized instances, no untagged resources, no unrestricted egress).
- Security baselines that must hold across every team and stack.

## When NOT to use

- Prototype or single-team IaC where review by a knowledgeable human is the only gate.
- Where the cost of the policy-engine infrastructure (CI runtime, rule maintenance) exceeds the value of the rules it enforces.
- As a substitute for cloud-native preventive controls — combine with org policies, SCPs, or equivalent.

## Decision inputs

- Are policies enforced at plan time, apply time, or both? Plan-time fails fast; cloud-native enforces in depth.
- What policy engine (OPA/Conftest, Sentinel, native cloud policies, custom) — driven by skills, ecosystem, and licensing.
- Are policies advisory (warn) or blocking (fail)? Mixed posture often works (warn first, block on next quarter).
- Where do exceptions live — inline annotations, a separate exceptions file, or per-stack overrides — and who approves them?
- How are policies versioned and tested? Treat them as code: test fixtures, regression suites, semver.

## Solution sketch

Run the policy engine against the rendered plan in CI, before apply.

```
[PR] → terraform plan → plan.json
                          │
                          ▼
                [policy engine: OPA/Sentinel/Conftest]
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
           pass: continue       fail: block merge
                                + structured findings
```

- Render the plan to a machine-readable artefact (`terraform show -json plan.out`) so the engine evaluates declared *changes*, not source code.
- Layer enforcement: plan-time policies (fast, granular), cloud-native policies (defence in depth), org-level SCPs (universal).
- Categorise rules by severity (advisory, warning, blocking); start advisory, promote to blocking on a published cadence.
- Version policy bundles independently from infrastructure code; pin to a tagged release in CI.
- Test policies with fixtures of known-good and known-bad plans; fail CI if a fixture flips.

See OPA docs and Conftest for plan-time evaluation; Sentinel for Terraform Cloud-native; cloud-vendor policy services for in-depth.

## Trade-offs

| Gain | Cost |
|---|---|
| Forbidden configurations fail at PR time, not at apply or audit | Policy engine becomes a critical CI dependency |
| Auditable evidence of enforcement for every change | Rule maintenance is real ongoing work — bad rules erode trust |
| Layered with cloud-native policies, defence in depth | Two policy systems can disagree; reconciliation is operational |
| Exception path is explicit and reviewable | Exception sprawl recreates the problem if not pruned |
| Catches drift between intended and declared state at plan time | Engine output noise needs structured triage to stay useful |

## Implementation checklist

- [ ] Choose a policy engine (OPA/Conftest, Sentinel, native cloud) based on stack and team skill.
- [ ] Render plan as machine-readable JSON in CI before policy evaluation.
- [ ] Author the first dozen rules covering tagging, region restrictions, resource sizes, public exposure.
- [ ] Categorise each rule by severity; document promotion path from advisory to blocking.
- [ ] Pin the policy bundle to a tagged release in CI; do not pull `main`.
- [ ] Add fixture tests for every rule (known-good plan, known-bad plan).
- [ ] Document the exception process (where, who approves, how it expires).
- [ ] Layer with cloud-native preventive controls (org policies, SCPs) for defence in depth.
- [ ] Surface findings in the PR comment alongside the plan output.

## Stage-specific notes

- **At [[stage-prototype]]**: skip; review by a knowledgeable human is the gate.
- **At [[stage-mvp]]**: optional; cloud-native preventive policies often sufficient.
- **At [[stage-production]]**: required for security-critical and cost rules; advisory acceptable for stylistic rules.
- **At [[stage-critical]]**: blocking enforcement, audited exceptions with documented expiry, regression-tested rule bundle.

## See also

- [[pattern-plan-review-gate]] — policy-as-code is one of the gate's enforcement layers.
- [[pattern-rbac]] — apply-time identity scoping is the other half of the security story.
- [[principle-defence-in-depth]] — plan-time + cloud-native + SCP enforcement layered.
- [[principle-zero-trust]] — every change verified explicitly before apply.
