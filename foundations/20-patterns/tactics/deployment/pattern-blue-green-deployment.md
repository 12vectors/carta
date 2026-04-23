---
id: pattern-blue-green-deployment
title: Blue-Green Deployment
type: pattern
category: deployment
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, deployment, release, zero-downtime]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-internal-tool]]"
prerequisites:
  - "[[pattern-health-check-endpoint]]"
related:
  - "[[pattern-canary-release]]"
  - "[[pattern-feature-flag]]"
  - "[[pattern-deployment-stamps]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Blue Green Deployment (Fowler, 2010) — https://martinfowler.com/bliki/BlueGreenDeployment.html"
  - "https://docs.aws.amazon.com/whitepapers/latest/overview-deployment-options/bluegreen-deployments.html"
---

## When to use

- Zero-downtime releases required and users won't tolerate short error windows.
- Rollback must be instantaneous — flip traffic back, not redeploy.
- Deployable is stateless enough that two parallel copies can run simultaneously.
- Release risk is high enough that a rollback drill is worth practising.

## When NOT to use

- Stateful services where running two versions against the same store corrupts data.
- Cost-sensitive systems where paying for a second full environment is unaffordable.
- Schema changes that are not backward-compatible between the two versions.
- Very frequent deploys where the cost of switch-and-warm-up dominates release velocity.

## Decision inputs

- Traffic-switching mechanism — DNS, load balancer, service mesh, or router.
- Warm-up time and readiness-signal latency for the new environment.
- Data layer strategy — shared store, read-only parallel, or dual-write.
- Roll-forward vs. rollback criteria and who authorises each.
- How long the "green" side stays warm after the switch.

## Solution sketch

Run two identical production environments — "blue" (current) and "green" (candidate). Deploy the new release to green while blue serves traffic. Run smoke and health checks on green. Switch the router (or DNS, or load balancer) to send traffic to green. Keep blue idle but warm as an instant rollback target. After a validation window, decommission blue or promote it to be the next green.

```
[traffic] ---> [LB] --switch--> [green v2]   (idle: blue v1)
               [LB] ----------> [blue v1]    (idle: green v2)
```

## Trade-offs

| Gain | Cost |
|------|------|
| Zero downtime and instant rollback by router switch | Two full production environments — infrastructure cost doubles around the deploy |
| Full pre-traffic validation on the new environment | Requires backward-compatible schemas and shared data strategy |
| Clear, testable rollback procedure | Longer-running schema migrations must finish before the flip |
| Natural pairing with feature flags for dark launches | Session stickiness or in-memory state complicates the switch |

## Implementation checklist

- [ ] Choose the switch point (LB, DNS, service mesh route).
- [ ] Ensure readiness endpoint accurately reflects dependency health.
- [ ] Make schema changes backward-compatible (see [[pattern-expand-contract-migration]]).
- [ ] Document rollback procedure as executable script, not prose.
- [ ] Practice a rollback in staging before the first production flip.
- [ ] Decide the warm-idle window for the previous environment.
- [ ] Automate traffic warm-up / shadow traffic before the flip if needed.
- [ ] Emit a release event with correlation IDs for observability.

## See also

- [[pattern-canary-release]] — gradual traffic shift; complementary to or substitute for blue-green.
- [[pattern-feature-flag]] — decouple deploy from release; can run blue-green without a feature-exposure flip.
- [[pattern-health-check-endpoint]] — required for the readiness gate before switching.
- [[pattern-expand-contract-migration]] — how to evolve schemas safely during the window.
