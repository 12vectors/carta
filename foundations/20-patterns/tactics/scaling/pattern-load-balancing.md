---
id: pattern-load-balancing
title: Load Balancing
type: pattern
category: scaling
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, scaling, load-balancing, horizontal-scaling]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-health-check-endpoint]]"
  - "[[pattern-microservices]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Designing Data-Intensive Applications (Kleppmann, O'Reilly, 2017) ch. 5 -- https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/"
---

## When to use

- Horizontally scaled stateless services fronting HTTP, gRPC, or TCP traffic.
- Rolling deploys, blue/green, or canary rollouts across multiple replicas.
- Availability-critical paths where a single instance failure must not take the service down.
- Regional failover across zones or regions.
- Offloading TLS termination, request logging, or WAF from app instances.

## When NOT to use

- Single-instance services where the LB only adds a hop.
- Strongly affinity-bound workloads (per-user sharded state with no rebalance plan).
- Tight intra-process calls — use in-process concurrency.
- When session stickiness defeats the point and a session store is cheaper.

## Decision inputs

- L4 (TCP) vs L7 (HTTP/gRPC) — header routing, retries, and mTLS need L7.
- Algorithm (round-robin, least-connections, consistent-hash, EWMA latency).
- Health check semantics and failure thresholds per backend.
- Session affinity requirements (stateless preferred; sticky only when state is local).
- Topology: client-side, server-side, service mesh, or managed (ALB, NLB, GCLB).

## Solution sketch

Place a distributor between clients and N backend replicas. The LB performs **health checks** (see related), removes unhealthy backends, and picks a target per request using a chosen algorithm.

- **L4**: fast, protocol-agnostic, no request-level retries.
- **L7**: header/path routing, retries, circuit breaking, per-route policies.
- **Client-side** (gRPC, Finagle): zero-hop, needs service discovery.
- **Mesh** (Envoy/Istio/Linkerd): sidecar does L7 LB + mTLS + telemetry.

Default to least-connections or EWMA over round-robin when backend latencies vary. Use consistent-hash only when cache affinity justifies uneven load. See Kleppmann ch. 5 for routing trade-offs.

## Trade-offs

| Gain | Cost |
|------|------|
| Horizontal scale without client changes | Extra hop adds latency and a failure mode |
| Removes dead instances automatically via health checks | Health-check tuning: too loose keeps bad nodes, too tight flaps |
| TLS, auth, and logging centralised | L7 LBs are expensive at high RPS; budget accordingly |
| Enables rolling deploys and canary | Sticky sessions undermine elasticity and complicate drains |
| Regional failover when paired with DNS/anycast | Cross-zone traffic can spike egress cost |

## Implementation checklist

- [ ] Pick L4 vs L7 per service based on routing needs.
- [ ] Wire `/healthz` and `/readyz` endpoints on every backend.
- [ ] Configure health-check interval, timeout, and unhealthy threshold.
- [ ] Set connection and request timeouts at the LB, not just the app.
- [ ] Enable graceful drain on shutdown (SIGTERM → fail readiness → wait).
- [ ] Emit per-backend request, error, and latency metrics.
- [ ] Load-test failover: kill a backend mid-traffic, verify no 5xx spike.
- [ ] Document algorithm and affinity choice in the runbook.

## See also

- [[pattern-health-check-endpoint]] — mandatory input to LB routing decisions.
- [[pattern-microservices]] — typical deployment topology requiring per-service LBs.
- [[pattern-circuit-breaker]] — pairs with L7 LB for fast failure at the hop above.
