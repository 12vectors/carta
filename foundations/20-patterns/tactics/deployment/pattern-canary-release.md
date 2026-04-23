---
id: pattern-canary-release
title: Canary Release
type: pattern
category: deployment
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, deployment, release, progressive-delivery]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-load-balancing]]"
  - "[[pattern-red-metrics]]"
related:
  - "[[pattern-blue-green-deployment]]"
  - "[[pattern-feature-flag]]"
  - "[[pattern-distributed-tracing]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Canary Release (Fowler, 2014) — https://martinfowler.com/bliki/CanaryRelease.html"
  - "Canarying Releases (Site Reliability Workbook, Google) — https://sre.google/workbook/canarying-releases/"
---

## When to use

- Release risk is real and a percentage-based traffic ramp reduces blast radius.
- You have per-request metrics that can distinguish canary vs. baseline error and latency.
- Traffic router supports weighted splits (service mesh, LB, gateway).
- Rollback needs to happen fast based on a measurable signal, not a human judgement call.
- Team has the observability to detect canary-specific regressions within minutes.

## When NOT to use

- Low-volume services where a small traffic percentage doesn't produce statistically useful signal quickly.
- Stateful workloads where canary and baseline must not share state.
- Schema changes that aren't backward-compatible.
- No per-cohort metrics — if you can't compare canary vs. baseline, the pattern loses its point.
- Ultra-low-latency paths where the split-routing overhead is unacceptable.

## Decision inputs

- Initial traffic percentage and the ramp schedule (1% → 10% → 50% → 100%).
- Automatic-rollback thresholds on error rate, latency, saturation.
- Cohort stability — sticky sessions or per-request sampling.
- Minimum observation window before each ramp step.
- Who pages when the canary fails and who authorises promotion.

## Solution sketch

Deploy the new version alongside the current version. Configure the router to send a small percentage of traffic (1–5%) to the canary. Compare per-cohort metrics (error rate, P95/P99 latency, saturation) against the baseline. If the canary is within tolerances over a measured window, ramp up. If not, route all traffic back to baseline. Automation of the ramp-and-rollback decision is the distinguishing feature — canary-by-hand is just blue-green with extra steps.

```
[traffic] ---> [LB 95%] ---> [v1 baseline]
               [LB  5%] ---> [v2 canary]   <- metrics compared against baseline
```

## Trade-offs

| Gain | Cost |
|------|------|
| Bounded blast radius — failures hit a small cohort | Requires per-cohort metrics and automated comparison |
| Real-traffic validation before full promotion | Longer total release time vs. blue-green flip |
| Signal to roll back is measurable, not subjective | Operationally heavier — cohort routing, automated promotion |
| Complementary to feature flags for per-user rollouts | Statistical significance needs real traffic volume |

## Implementation checklist

- [ ] Pick the traffic-split mechanism (service mesh, LB, gateway).
- [ ] Define the per-cohort metrics (RED at minimum: Rate, Errors, Duration).
- [ ] Encode ramp steps and dwell times as config, not ritual.
- [ ] Define automatic-rollback thresholds per metric.
- [ ] Ensure baseline and canary are tagged for tracing and log filtering.
- [ ] Alert on rollback events with correlation IDs.
- [ ] Document manual-override path for emergency freeze and promote.
- [ ] Test a canary rollback in staging before first production use.

## See also

- [[pattern-blue-green-deployment]] — atomic flip vs. progressive ramp; same goal, different trade-offs.
- [[pattern-feature-flag]] — user-level rollout on top of canary traffic.
- [[pattern-red-metrics]] — the per-cohort signal that decides ramp vs. rollback.
- [[pattern-distributed-tracing]] — attribute each request to canary or baseline.
