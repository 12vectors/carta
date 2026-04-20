---
id: pattern-gateway-offloading
title: Gateway Offloading
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-security]]"
tags: [pattern, stable, api, gateway, cross-cutting]
applies_to:
  - "[[context-web-application]]"
prerequisites:
  - "[[pattern-api-gateway]]"
related: []
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-offloading"
---

## When to use

- Cross-cutting concerns (TLS, authn, rate limiting, WAF) duplicated across services.
- Compliance or security requires central enforcement and audit.
- Backend teams want to focus on domain logic, not plumbing.
- A single policy change must take effect without redeploying every service.

## When NOT to use

- Concern is inherently domain-specific (business authz, data filtering).
- Single service only — offloading adds a hop for no reuse benefit.
- Gateway vendor lock-in is unacceptable for the offloaded capability.
- Latency budget cannot absorb an extra hop for every request.

## Decision inputs

- Which concerns are genuinely shared vs service-specific.
- Policy change frequency — high frequency favours central offload.
- Audit and compliance scope — central point simplifies evidence.
- Gateway capability — TLS, JWT, WAF, compression, request/response rewrites.
- Fallback if gateway fails — services must still be safe by default.

## Solution sketch

Move shared, non-domain concerns out of every service and into the gateway: TLS termination, certificate rotation, JWT/OAuth2 validation, rate limiting, WAF rules, request logging, response compression, and IP allowlists. Domain services trust the gateway-provided identity (propagated as headers) and focus on business logic. Services still enforce authorisation — offloading authentication does not offload authorisation.

```
client ──TLS──> [gateway: authn, rate-limit, WAF, compress]
                           │  (trusted identity headers)
                           └──> service (domain logic + authz only)
```

See the Azure architecture centre article for common offload targets and failure modes.

## Trade-offs

| Gain | Cost |
|------|------|
| One place to fix/upgrade TLS, authn, WAF | Gateway becomes security-critical — must be hardened and HA |
| Services stay focused on domain logic | Services must still authorise; don't confuse authn with authz |
| Central audit and compliance evidence | Trust boundary — services must refuse direct calls bypassing gateway |
| Uniform policy across heterogeneous backends | Vendor/tooling lock-in for offloaded capabilities |

## Implementation checklist

- [ ] Identify concerns that are truly cross-cutting — not every duplication is shared.
- [ ] Terminate TLS at the gateway; enforce mTLS or network policy gateway-to-service.
- [ ] Validate JWTs at the gateway; pass identity in a signed/trusted header.
- [ ] Services reject requests that bypass the gateway (network policy or token check).
- [ ] Rate limiting and quotas per consumer identity.
- [ ] WAF rules in audit mode before enforce; review false positives.
- [ ] Central access log with correlation ID propagated to services.
- [ ] Failure mode documented — do services fail closed or open if gateway unreachable?

## See also

- [[pattern-api-gateway]] — parent pattern.
- [[pattern-gateway-routing]] — sibling; routes rather than offloads.
- [[pattern-gateway-aggregation]] — sibling; aggregates responses.
- [[pattern-oauth2-authorization]] — common authn offload target.
