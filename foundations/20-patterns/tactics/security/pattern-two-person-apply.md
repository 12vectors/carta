---
id: pattern-two-person-apply
title: Two-Person Apply
type: pattern
category: security
maturity: experimental
stage_floor: production
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
tags: [pattern, experimental, iac, two-person, governance, separation-of-duties]
applies_to:
  - "[[context-infrastructure-as-code]]"
prerequisites:
  - "[[pattern-rbac]]"
  - "[[pattern-plan-review-gate]]"
related:
  - "[[pattern-federated-identity]]"
  - "[[pattern-policy-as-code]]"
conflicts_with: []
contradicted_by: []
sources:
  - "NIST SP 800-53 Rev. 5 — AC-5 Separation of Duties — https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final"
  - "Google Cloud — Privileged Access Manager — https://cloud.google.com/iam/docs/pam-overview"
  - "AWS — IAM Access Analyzer policy generation and just-in-time access — https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html"
  - "GitHub — Branch protection rules and required reviews — https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches"
  - "Site Reliability Engineering (Beyer et al., O'Reilly, 2016) ch. 6 'Monitoring Distributed Systems' — https://sre.google/sre-book/monitoring-distributed-systems/"
---

## When to use

- Production foundations where a single mistaken apply could destroy multi-team or multi-tenant resources.
- Regulated environments (SOC2, PCI, HIPAA, FedRAMP) requiring documented separation of duties.
- Apply identities with org-wide or billing-level privilege.
- Emergency-change paths that bypass normal review (these need their own two-person rule).
- Environments with a history of "fat-finger" incidents traceable to lone actors.

## When NOT to use

- Solo-developer environments where no second person exists.
- Prototype or sandbox environments where speed dominates safety.
- Read-only operations (drift detection, plan-only roles) — apply is the privileged action, not plan.

## Decision inputs

- Where is the second-person check enforced — VCS branch protection, cloud-native PAM, both?
- Is the same person who authored the change allowed to be one of the approvers? Usually no.
- What is the emergency-change path, and does it have its own (delayed or post-hoc) two-person review?
- How is approver eligibility maintained — group membership, training, on-call rotation?
- What is the audit retention for approval events?

## Solution sketch

The apply step requires a second authorised principal beyond the change-author.

```
PR opened/updated  ─►  plan rendered  ─►  required approvers count = N (>=2 distinct)
                                                       │
                            merge gated on author ≠ approver
                                                       │
                                                       ▼
                                       apply runs as a constrained identity
                                       gated by a second policy layer
                                       (PAM entitlement / just-in-time grant /
                                        cloud-native multi-party authorisation)
```

- Enforce the rule in two places: VCS (branch protection, required reviews) **and** the apply identity layer (PAM, JIT access, cloud-native multi-party auth). Belt-and-braces.
- Disallow author-as-approver explicitly; rely on directory groups, not heuristics.
- Provide an emergency-change path with explicit auditing and post-hoc review — better than people circumventing the rule.
- Capture the approval event (who, when, what) into the same audit pipeline as apply logs.
- Test the gate periodically by attempting a self-approval and asserting it fails.

See NIST AC-5 for the canonical separation-of-duties statement; cloud-vendor PAM/JIT services for in-depth.

## Trade-offs

| Gain | Cost |
|---|---|
| Single-actor mistakes are caught before apply | Apply latency increases — second approver must be available |
| Compliance evidence accumulates per change | Approver fatigue if rule is applied to every trivial change |
| Removes "I can apply anything" from any one person's powers | Requires investment in approver training and rotation |
| Belt-and-braces VCS + apply-identity enforcement is robust | Two systems can disagree; reconciliation is operational |
| Emergency-change path remains available with audit | Emergency path can become the normal path if not policed |

## Implementation checklist

- [ ] Configure VCS branch protection requiring ≥2 distinct approvers on `main`.
- [ ] Disallow author-as-approver in branch protection config.
- [ ] Require status checks (plan, policy-as-code) green before merge.
- [ ] Enforce the apply identity behind a PAM/JIT/multi-party authorisation layer.
- [ ] Document the emergency-change path with explicit audit and post-hoc review.
- [ ] Capture approval events into the same audit log as apply.
- [ ] Test the gate quarterly: attempt self-approval, assert failure, document the result.
- [ ] Rotate approver groups on a published cadence; tie membership to training.

## Stage-specific notes

- **At [[stage-prototype]]**: skip; speed is the dominant pillar.
- **At [[stage-mvp]]**: optional; one knowledgeable reviewer is the floor.
- **At [[stage-production]]**: required; VCS branch protection minimum; PAM/JIT recommended.
- **At [[stage-critical]]**: belt-and-braces enforcement, audited emergency path with post-hoc review, periodic gate testing.

## See also

- [[pattern-plan-review-gate]] — the gate this pattern reinforces with an approver requirement.
- [[pattern-rbac]] — apply-time identity scoping; this pattern wraps an additional approval layer on top.
- [[pattern-federated-identity]] — approver and apply identities are federated, not key-based.
- [[pattern-policy-as-code]] — automated policies catch what reviewers might miss.
- [[principle-defence-in-depth]] — review + policy + multi-party authorisation are layered controls.
