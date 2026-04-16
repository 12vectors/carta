---
id: pattern-rate-limiting
title: Rate Limiting (Platform Team)
type: pattern
category: resilience
maturity: stable
tags: [pattern, resilience, stable]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-retry-with-backoff]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://stripe.com/blog/rate-limiters"
  - "https://cloud.google.com/architecture/rate-limiting-strategies-techniques"
  - "Building Microservices (Newman, 2021) ch. 11"
---

## When to use

- Your API is exposed to external consumers (partners, public developers, mobile clients) and you need to protect against abuse or accidental overload.
- Internal services that are resource-constrained and could be overwhelmed by a burst from a single caller.
- You need to enforce fair usage across multiple tenants or API consumers.
- Regulatory or contractual requirements impose request limits on specific operations (e.g. payment initiation, identity verification).

## When NOT to use

- Purely internal services where all callers are trusted and load is predictable — circuit breakers and autoscaling are usually sufficient.
- Services where every request must succeed regardless of volume (use queuing instead).
- When the bottleneck is a downstream dependency, not your own capacity — rate limiting your API won't protect the downstream. Use a circuit breaker there instead.

## Decision inputs

- **Where does enforcement happen?** API gateway (simplest, coarse-grained), application middleware (more control, finer-grained), or both.
- **What algorithm?** Token bucket (smooth, allows bursts), sliding window (predictable), fixed window (simplest but has edge-of-window spikes).
- **What key?** Per API key, per user, per IP, per endpoint, or a combination.
- **What limits?** Requests per second, per minute, per day — often tiered by plan or consumer type.
- **What response on limit?** HTTP 429 with `Retry-After` header is standard.

## Solution sketch

1. Choose an enforcement point — API gateway for coarse limits, application middleware for fine-grained.
2. Implement token bucket or sliding window counter, backed by a shared store (Redis is standard) for multi-instance deployments.
3. Key rate limits by consumer identity (API key, user ID) and optionally by endpoint.
4. Return `429 Too Many Requests` with a `Retry-After` header and include rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) on all responses.
5. Log rate limit events for monitoring — high rates of 429s from a single consumer may indicate a misconfigured integration rather than abuse.

## Trade-offs

| Gain | Cost |
|------|------|
| Protects service availability under load | Adds infrastructure dependency (Redis or similar) |
| Prevents abuse and ensures fair usage | Legitimate traffic may be rejected during spikes |
| Enables tiered pricing models | Requires coordination on limit values across teams |
| Provides visibility into usage patterns | Client SDKs need retry logic for 429 responses |

## Implementation checklist

- [ ] Rate limiting enforcement point chosen and documented.
- [ ] Algorithm selected (token bucket, sliding window, or fixed window) with justification.
- [ ] Rate limit store deployed (Redis) with HA configuration.
- [ ] Standard rate limit headers included on all API responses.
- [ ] 429 responses include `Retry-After` header.
- [ ] Rate limit values documented per consumer tier.
- [ ] Monitoring and alerting on rate limit hit rates.
- [ ] Client documentation updated with rate limit details and retry guidance.

## See also

- [[pattern-circuit-breaker]] — protects against downstream failures; rate limiting protects against upstream overload
- [[pattern-retry-with-backoff]] — clients hitting rate limits should retry with backoff
