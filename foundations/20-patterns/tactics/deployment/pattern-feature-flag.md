---
id: pattern-feature-flag
title: Feature Flag
type: pattern
category: deployment
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, deployment, release, feature-toggles]
applies_to:
  - "[[context-web-application]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
prerequisites: []
related:
  - "[[pattern-canary-release]]"
  - "[[pattern-blue-green-deployment]]"
  - "[[pattern-strangler-fig]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Feature Toggles (aka Feature Flags) (Hodgson / Fowler, 2017) — https://martinfowler.com/articles/feature-toggles.html"
  - "https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/feature-flags.html"
---

## When to use

- Deploy and release must be decoupled — code ships without exposing the feature.
- Progressive rollout by cohort (percentage, tenant, region, persona) is required.
- Long-lived branches cause merge pain — flag the new path and ship both.
- Kill-switch needed for risky behaviour (new integrations, paid tier, agent tools).
- A/B testing or experiment design calls for deterministic cohorting.

## When NOT to use

- Short-lived toggle for a single release — regular branch-and-deploy is simpler.
- Safety-critical code where flag misconfiguration is worse than a delayed release.
- Teams without the discipline to clean up stale flags — debt compounds fast.
- Environments where config drift between nodes can't be ruled out.

## Decision inputs

- Flag lifetime (release toggle, experiment, ops kill-switch, long-lived permission).
- Evaluation context (user, tenant, region, request attribute).
- Flag store (env var, config file, SaaS provider, database) and latency budget.
- Consistency across nodes and caching strategy at read time.
- Ownership and the process for retiring stale flags.

## Solution sketch

Wrap new code paths in a named conditional that reads from a flag store. The flag's value can be global, percent-based, or context-driven (by user, tenant, region). Deploy the code with the flag off; turn it on progressively or for specific cohorts. For experiments, record exposure and outcome per cohort. For kill-switches, ensure the flag can be read without depending on the subsystem it disables.

```
if flags.get("new_checkout_flow", ctx=request.user):
    return new_checkout(request)
else:
    return legacy_checkout(request)
```

Classify flags by lifetime (release, experiment, ops, permission). The lifetime determines the retirement policy.

## Trade-offs

| Gain | Cost |
|------|------|
| Decouple deploy from release; rollback is a config change | Every flag is a branch in the code — test matrix grows |
| Progressive exposure and fast kill-switches | Stale flags rot and become silent liabilities if not retired |
| Unblocks trunk-based development | Flag-eval store becomes a runtime dependency on every path it guards |
| Enables experimentation and cohort rollouts | Misconfigured flags look like bugs in the new code |

## Implementation checklist

- [ ] Classify the flag by lifetime (release / experiment / ops / permission).
- [ ] Record the retirement criterion and date for short-lived flags.
- [ ] Use a flag store with caching and a documented refresh latency.
- [ ] Log exposure (flag, user, value, timestamp) for experiments.
- [ ] Fail safe: if the flag store is unreachable, default to the off state.
- [ ] Add a dashboard of active flags and their age.
- [ ] Build a retirement workflow into the sprint, not a future cleanup epic.
- [ ] Alert on flags older than the retirement policy.

## See also

- [[pattern-canary-release]] — traffic-level progressive rollout; flags do the user-level variant.
- [[pattern-blue-green-deployment]] — environment-level; flags are feature-level; combine for defence in depth.
- [[pattern-strangler-fig]] — flags are the gate that selects between legacy and replacement paths.
