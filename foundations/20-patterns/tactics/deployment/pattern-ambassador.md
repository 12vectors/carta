---
id: pattern-ambassador
title: Ambassador
type: pattern
category: deployment
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, deployment, proxy, resilience]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-sidecar]]"
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-retry-with-backoff]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/ambassador"
---

## When to use

- Standardising outbound client behaviour (retries, timeouts, circuit breaking, TLS) across many services.
- Adding resilience or auth to a legacy client that cannot be modified.
- Centralising service-discovery, routing, or traffic-shaping for outbound calls.
- Polyglot fleets where reimplementing a robust client in each language is wasteful.

## When NOT to use

- Single-language stacks with a well-maintained resilient client library.
- Latency-critical outbound calls where the localhost hop is unacceptable.
- Simple internal calls within a trusted network with no resilience needs.
- When a centralised API gateway already covers the same concerns.

## Decision inputs

- Protocols to proxy — HTTP, gRPC, database, message broker.
- Resilience policy — timeouts, retries, circuit breaker thresholds.
- Observability surface — outbound metrics, logs, traces from the ambassador.
- Configuration source — static, control plane, or service mesh.
- Failure behaviour when the ambassador itself is unavailable.

## Solution sketch

Deploy an outbound proxy as a sidecar to each service. The application calls `localhost:port` as if it were the remote dependency. The ambassador enforces timeouts, retries, circuit breaking, TLS, and auth; emits metrics, logs, and traces; and routes to the real target. Service mesh data planes (Envoy, Linkerd-proxy) are ambassador implementations at fleet scale.

```
[app] --localhost--> [ambassador] --mTLS + retries + CB--> [remote service]
                          \--metrics/traces--> [observability]
```

See the Microsoft docs for the canonical description.

## Trade-offs

| Gain | Cost |
|------|------|
| Consistent resilience across all languages and services | Extra hop, extra process per workload |
| Centralised policy updates without redeploying apps | Misconfiguration blast radius is fleet-wide |
| Rich outbound telemetry out of the box | Debugging now involves the proxy layer |
| Retrofits resilience onto legacy clients | Config/control-plane complexity if done at scale |

## Implementation checklist

- [ ] Choose ambassador implementation (Envoy, Linkerd-proxy, custom).
- [ ] Define default resilience policy (timeout, retry, breaker) per dependency.
- [ ] Configure TLS/mTLS termination at the ambassador.
- [ ] Emit per-destination metrics, logs, and traces.
- [ ] Define behaviour when the ambassador is down (fail closed vs. bypass).
- [ ] Test timeout, retry, and circuit-breaker paths end to end.
- [ ] Version and roll out policy changes progressively.
- [ ] Bound resource usage per ambassador instance.

## See also

- [[pattern-sidecar]] — ambassador is a sidecar specialised for outbound traffic.
- [[pattern-circuit-breaker]] — commonly enforced inside the ambassador.
- [[pattern-retry-with-backoff]] — retries configured centrally at the ambassador.
