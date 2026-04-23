---
id: pattern-health-check-endpoint
title: Health Check Endpoint
type: pattern
category: resilience
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, resilience, observability, operations]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-load-balancing]]"
  - "[[pattern-circuit-breaker]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://microservices.io/patterns/observability/health-check-api.html"
  - "Microservices Patterns (Richardson, Manning, 2018) ch. 11"
---

## When to use

- Service runs behind a load balancer or orchestrator that needs liveness signals.
- Kubernetes, ECS, or similar platforms requiring liveness/readiness probes.
- Blue/green or canary deploys needing a ready-to-serve signal.
- Dependency-aware routing where one unhealthy instance must drain traffic.
- Uptime monitors and synthetic checks need a cheap, stable URL.

## When NOT to use

- Short-lived functions where platform handles lifecycle without probes.
- Internal-only scripts with no traffic-routing layer consuming the signal.
- When the endpoint would expose sensitive internals without auth.

## Decision inputs

- Three distinct checks — liveness (am I running), readiness (can I serve), startup (am I initialised).
- Which dependencies to check and how deeply (shallow ping vs real query).
- Timeout and caching to keep the endpoint cheap under poll pressure.
- Auth and exposure — public `/healthz` vs authenticated `/health/deep`.
- Failure policy — readiness returning 503 must drain traffic, not restart.

## Solution sketch

Expose three endpoints with clear semantics:

- `/livez` — process responsive. No dependency checks. Failing = restart.
- `/readyz` — can serve traffic now (dependencies reachable, migrations done). Failing = drain from LB.
- `/startupz` — initial boot complete. Failing during startup = do not probe liveness yet.

Return 200 for healthy, 503 for unhealthy, a small JSON body with per-check status. Cache deep checks (DB, queues) for a few seconds to avoid poll amplification. Never couple liveness to downstream health — you will restart-loop on a dependency outage.

See microservices.io and Richardson ch. 11 for endpoint conventions.

## Trade-offs

| Gain | Cost |
|------|------|
| Automated traffic draining and restart decisions | Wrong liveness scope causes restart loops during dependency outage |
| Fast feedback on deploy readiness | Deep checks under heavy poll add load to dependencies |
| Standard surface for LBs, orchestrators, monitors | Public endpoint may leak version or dependency topology |
| Enables dependency-aware load balancing | Three endpoints to maintain and keep semantically distinct |

## Implementation checklist

- [ ] Implement `/livez`, `/readyz`, `/startupz` with distinct semantics.
- [ ] Keep liveness independent of downstream dependencies.
- [ ] Check real dependencies in readiness (DB ping, queue connect).
- [ ] Cache deep-check results for 2-5 seconds.
- [ ] Return structured JSON with per-check status and version.
- [ ] Gate detailed `/health/deep` behind auth or internal-only network.
- [ ] Wire orchestrator probes to the correct endpoint per phase.
- [ ] Test drain behaviour — readiness 503 removes instance from LB rotation.

## See also

- [[pattern-load-balancing]] — consumes readiness signal for routing.
- [[pattern-circuit-breaker]] — complementary, protects calls between services.
- [[pattern-structured-logging]] — log probe failures with context.
