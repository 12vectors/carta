---
id: pattern-sidecar
title: Sidecar
type: pattern
category: deployment
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, deployment, kubernetes, service-mesh]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-ambassador]]"
  - "[[pattern-microservices]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar"
---

## When to use

- Cross-cutting concerns (TLS, auth, logging, metrics, config) needed across many services in different languages.
- Augmenting a legacy app that cannot be modified.
- Offloading protocol translation or telemetry from the main process.
- Service-mesh data plane (Envoy, Linkerd) alongside each workload.

## When NOT to use

- Single-language stacks where a shared library is simpler and cheaper.
- Latency-sensitive paths where the extra localhost hop matters.
- Resource-constrained environments (edge, embedded) — doubling container count doubles overhead.
- When the concern is not truly cross-cutting — build it into the service.

## Decision inputs

- Co-location unit — pod, VM, or process group sharing lifecycle and network.
- Interface — localhost HTTP/gRPC, Unix socket, or shared volume.
- Resource budget — sidecar CPU/memory per instance, multiplied by fleet size.
- Lifecycle — start/stop ordering and health-check coupling with the main container.
- Update cadence independent of the application.

## Solution sketch

Deploy a secondary container alongside the main application container in the same pod/unit. They share network namespace and can share volumes. The sidecar handles a cross-cutting concern — for example, a proxy intercepting traffic, a log shipper reading shared files, or a config agent refreshing secrets. The main app stays focused on domain logic and is language-agnostic about the sidecar's implementation.

```
[pod]
  [app container] <-- localhost --> [sidecar container]
        \-- shared volume --/
```

See the Microsoft docs for variants and anti-patterns.

## Trade-offs

| Gain | Cost |
|------|------|
| Polyglot-friendly — one sidecar serves all languages | Doubles container count; resource and ops overhead |
| Independent release cadence from the app | Lifecycle and ordering bugs (startup, shutdown) |
| Clean separation of concerns per process | Localhost hop adds latency and failure mode |
| Retrofits onto legacy apps without code change | Debugging spans two processes |

## Implementation checklist

- [ ] Confirm the concern is cross-cutting across multiple services.
- [ ] Define the app↔sidecar interface (HTTP, gRPC, socket, file).
- [ ] Configure shared pod/unit with correct start/stop ordering.
- [ ] Set explicit CPU and memory limits for the sidecar.
- [ ] Wire health checks so sidecar failure reflects in readiness.
- [ ] Align log and metric pipelines to ingest from the sidecar.
- [ ] Budget fleet-wide resource impact before rollout.
- [ ] Document upgrade procedure independent of the app.

## See also

- [[pattern-ambassador]] — an outbound-proxy specialisation of the sidecar idea.
- [[pattern-microservices]] — sidecars are most common in fine-grained service fleets.
