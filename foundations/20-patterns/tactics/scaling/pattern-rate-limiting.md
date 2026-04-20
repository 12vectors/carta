---
id: pattern-rate-limiting
title: Rate Limiting
type: pattern
category: scaling
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, scaling, rate-limiting, abuse-prevention]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-throttling]]"
  - "[[pattern-queue-based-load-leveling]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Scaling your API with rate limiters (Paul Tarjan, Stripe, 2018) -- https://stripe.com/blog/rate-limiters"
---

## When to use

- Public or partner APIs where per-client quotas prevent one tenant starving others.
- Abuse-prone endpoints: login, signup, password reset, OTP, checkout.
- Paid tiers with contractual request-per-minute allowances.
- Protecting expensive endpoints (search, exports, inference) from runaway clients.
- Noisy-neighbour mitigation in multi-tenant systems.

## When NOT to use

- Internal RPCs inside a single trust boundary — use capacity planning and backpressure.
- Batch pipelines where throughput limits belong at the consumer (see queue-based load leveling).
- As a substitute for authentication — unauthenticated limits are cheap to bypass via IP rotation.

## Decision inputs

- **Identity axis**: per API key, user, IP, tenant, endpoint, or composite — drives the key.
- Algorithm: fixed-window, sliding-window, token bucket (burst-tolerant), leaky bucket (smooth).
- Quota values per tier, and burst allowance.
- Shared vs per-node counters — distributed requires Redis/memcached or equivalent.
- Response contract: `429 Too Many Requests`, `Retry-After`, `X-RateLimit-*` headers.
- Failure mode when the counter store is down (fail-open vs fail-closed).

## Solution sketch

Distinguish from throttling: **rate limiting** rejects requests above a per-client quota; **throttling** shapes total server load. Both can coexist.

```
key = f(api_key or user_id or ip, route)
allow, remaining, reset = bucket.consume(key, cost=1)
if not allow: return 429 with Retry-After and X-RateLimit-* headers
```

- **Token bucket** is the default: allows bursts up to bucket size, refills at rate R.
- Store counters in a low-latency shared store (Redis with Lua or atomic INCR + EXPIRE).
- Apply at the edge (gateway, CDN) for DDoS-adjacent traffic; at the service for business quotas.
- Always return structured 429s with `Retry-After` — clients can back off correctly.

See Stripe's post for multi-algorithm layering (request-rate, concurrency, load-shed) in production.

## Trade-offs

| Gain | Cost |
|------|------|
| Prevents one client from degrading others | Extra dependency on counter store (Redis) on the hot path |
| Enforces contractual quotas and tiering | Distributed counters drift under partition; exact limits are hard |
| Throws a shield in front of expensive endpoints | Mis-sized limits cause false positives and support load |
| Shifts retry burden onto the client (Retry-After) | Clients without backoff turn 429s into storms |
| Cheap compared to provisioning for attacker traffic | IP-based limits hurt NAT'd users and proxies |

## Implementation checklist

- [ ] Pick the identity key per endpoint class (API key > user > IP fallback).
- [ ] Choose algorithm (token bucket default) and configure rate + burst per tier.
- [ ] Use atomic operations (Redis Lua, `INCR` + `EXPIRE`) for correctness.
- [ ] Return `429` with `Retry-After` and `X-RateLimit-{Limit,Remaining,Reset}` headers.
- [ ] Decide fail-open vs fail-closed when counter store is unreachable; document it.
- [ ] Exempt health checks and internal service-to-service traffic.
- [ ] Emit metrics: accepted, rejected, per-key saturation.
- [ ] Alert on sustained 429 rates — may signal mis-sized limits or genuine abuse.
- [ ] Publish quotas in API docs; make tier upgrades self-serve.

## See also

- [[pattern-throttling]] — server-side load shedding; complements per-client quotas.
- [[pattern-queue-based-load-leveling]] — buffers accepted traffic that rate limiting lets through.
- [[pattern-circuit-breaker]] — pair for upstream failure isolation on top of quota enforcement.
