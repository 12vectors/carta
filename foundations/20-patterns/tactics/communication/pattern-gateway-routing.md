---
id: pattern-gateway-routing
title: Gateway Routing
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, api, gateway, routing]
applies_to:
  - "[[context-web-application]]"
prerequisites:
  - "[[pattern-api-gateway]]"
related: []
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-routing"
---

## When to use

- One external hostname fronts many backend services.
- Backends are being split, merged, or renamed without changing client URLs.
- Versioning, canary, or blue-green traffic splits need a central decision point.
- Path or header routing rules change more often than service code.

## When NOT to use

- Single backend — DNS or a plain load balancer is enough.
- Routing logic depends on request body inspection — too expensive at the edge.
- Clients must reach services directly for latency reasons.
- Routing rules encode business logic — that belongs in a service, not a gateway.

## Decision inputs

- Route keys — path, host, header, query param, or client identity.
- Change velocity of routes — does it justify hot-reload vs redeploy?
- Canary and weighted split requirements.
- Per-route timeout, retry, and circuit-breaker policies.
- Config source — file, control plane, or service registry.

## Solution sketch

Gateway inspects incoming requests and forwards to the right backend based on declarative rules: path prefix, host, header, or weighted split. Rules are config, not code. Keep routing stateless — no session stickiness unless a backend genuinely requires it. For version rollouts, add a new route and shift weight; for refactors, map old paths to new services without changing the client URL.

```
GET /orders/*   ──> orders-service
GET /users/*    ──> users-v2 (90%)  / users-v1 (10%)
POST /events    ──> events-ingest
```

See the Azure architecture centre article for canary, shadowing, and failure variants.

## Trade-offs

| Gain | Cost |
|------|------|
| Stable external URLs despite backend churn | Gateway owns a critical mapping — misconfig = outage |
| Canary and weighted splits without client changes | Complex rules become their own deploy risk |
| Per-route policies (timeout, retry, auth) in one place | Debugging "where did my request go?" needs good logs |
| Service refactors invisible to clients | Adds a hop; rule evaluation cost per request |

## Implementation checklist

- [ ] Routes declared as config (YAML/CRD), reviewed like code.
- [ ] CI check for overlapping or shadowed rules.
- [ ] Per-route timeouts and retry policies; no global defaults masking outliers.
- [ ] Canary/weighted splits backed by metrics before full shift.
- [ ] Access log records matched route and selected backend.
- [ ] Hot-reload config without dropping in-flight requests.
- [ ] Rollback plan — previous route config kept and revertible.

## See also

- [[pattern-api-gateway]] — parent pattern.
- [[pattern-gateway-aggregation]] — sibling; aggregates rather than routes.
- [[pattern-gateway-offloading]] — sibling; centralises cross-cutting concerns.
- [[pattern-load-balancing]] — downstream of routing; distributes within a backend pool.
