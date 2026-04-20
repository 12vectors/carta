---
id: pattern-gateway-aggregation
title: Gateway Aggregation
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-performance]]"
tags: [pattern, stable, api, gateway, aggregation]
applies_to:
  - "[[context-web-application]]"
prerequisites:
  - "[[pattern-api-gateway]]"
related: []
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/gateway-aggregation"
---

## When to use

- One logical client action needs data from multiple backend services.
- Clients on slow or high-latency networks (mobile, partner WAN).
- Reducing chatty client-to-service round trips is the main perf lever.
- Each backend response is small but combined payload is useful.

## When NOT to use

- Backend calls have vastly different latencies — slowest dominates the response.
- One backend is the clear hot path — aggregate elsewhere or cache instead.
- Aggregation logic encodes business rules — put them in a domain service, not the gateway.
- Responses need independent caching or streaming to the client.

## Decision inputs

- Per-backend latency distribution — aggregate only when tail is manageable.
- Failure modes — all-or-nothing vs partial response acceptable.
- Payload size after aggregation vs client memory/bandwidth limits.
- Timeout budget — aggregate deadline = max(backends) + overhead.
- Caching opportunity per constituent vs the combined result.

## Solution sketch

Gateway receives one client request, fans out parallel calls to N backends, waits (up to a deadline) for responses, and returns a combined result. Use partial-success semantics: return what succeeded with per-section error markers rather than failing the whole request on one slow backend. Enforce per-backend timeout < aggregate timeout. No business logic in the aggregator — shape and merge only.

```
client ──> gateway ──┬──> service A ─┐
                     ├──> service B ─┼──> merge ──> client
                     └──> service C ─┘
```

See the Azure architecture centre article for variants and failure handling.

## Trade-offs

| Gain | Cost |
|------|------|
| Fewer client round trips — better mobile/WAN performance | Slowest backend drives response latency |
| Client code simpler — one call, one response | Partial-failure semantics must be designed explicitly |
| Central place to enforce deadlines and circuit breaking | Aggregator becomes a bottleneck if not horizontally scaled |
| Cross-cutting observability of the composite call | Hard to cache — combined shape rarely matches any one backend |

## Implementation checklist

- [ ] Issue backend calls in parallel, not serially.
- [ ] Per-backend timeout strictly less than the aggregate timeout.
- [ ] Partial-response contract with per-section status/error fields.
- [ ] Circuit breakers on each backend call; aggregation continues on trip.
- [ ] Correlation ID propagated to every downstream call.
- [ ] Response cached only where all constituents are cacheable.
- [ ] Keep aggregation stateless — no business rules in the gateway.

## See also

- [[pattern-api-gateway]] — parent pattern.
- [[pattern-gateway-routing]] — sibling; routes rather than aggregates.
- [[pattern-backend-for-frontend]] — BFFs aggregate per client type.
- [[pattern-scatter-gather]] — messaging-layer equivalent.
