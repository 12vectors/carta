---
id: pattern-grpc-api
title: gRPC API
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-performance]]"
tags: [pattern, stable, api, grpc, rpc, protobuf]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-rest-api]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://grpc.io/docs/"
  - "gRPC: Up and Running (Indrasiri & Kuruppu, O'Reilly, 2020) — https://www.oreilly.com/library/view/grpc-up-and/9781492058328/"
---

## When to use

- Internal service-to-service calls where latency and throughput matter.
- Strong schema contracts (protobuf) with generated clients in many languages.
- Streaming — server, client, or bidirectional — is a first-class need.
- Polyglot microservice estate wanting uniform RPC semantics.

## When NOT to use

- Browser clients without a gRPC-Web proxy or a gateway translating to REST.
- Public APIs where third parties expect JSON and HTTP tooling.
- Human-debuggable wire format needed without tooling (curl-friendly).
- Single-language monolith where in-process calls or REST are adequate.

## Decision inputs

- Client environments — browsers need gRPC-Web; mobile needs SDK support.
- Payload size and call rate — binary encoding wins grow with both.
- Streaming requirements (server push, client upload, chat-like duplex).
- Org tolerance for protobuf schema stewardship and code-gen pipelines.
- Observability — HTTP/2 framing and trailers need gRPC-aware tooling.

## Solution sketch

Services defined in `.proto` files; `protoc` generates client and server stubs. Transport is HTTP/2 with binary protobuf framing. Four call types: unary, server-streaming, client-streaming, bidirectional. Deadlines (timeouts) propagate across calls by convention. Errors use `google.rpc.Status` with canonical codes. Expose health-check and reflection services for tooling.

```
service.proto ── protoc ──> server stubs
                       └──> client stubs (Go, Java, Py, TS, ...)
```

See grpc.io docs for transport details and Indrasiri & Kuruppu for production patterns.

## Trade-offs

| Gain | Cost |
|------|------|
| Binary + HTTP/2 — smaller payloads, lower latency than JSON/HTTP/1.1 | Not browser-native; needs gRPC-Web or gateway |
| Generated clients in every major language | Protobuf schema lifecycle and breaking-change discipline |
| First-class streaming in all four directions | Harder to debug on the wire without reflection/tools |
| Deadline propagation and canonical status codes | Load balancers and proxies need HTTP/2 end-to-end |

## Implementation checklist

- [ ] Proto schemas in a shared repo or registry with CI linting (buf, protolock).
- [ ] Deadlines set on every client call and propagated through the chain.
- [ ] Retry/hedging policy declared via service config, not ad hoc.
- [ ] TLS between services; mTLS inside the mesh where required.
- [ ] Health-check service registered for load balancer probes.
- [ ] Server-side reflection enabled in non-prod for debugging.
- [ ] Observability — interceptors for tracing, metrics, and auth.
- [ ] Breaking-change CI check on proto files.

## See also

- [[pattern-rest-api]] — alternative; preferred for browsers and third parties.
- [[pattern-api-gateway]] — translate gRPC to REST/JSON at the edge.
- [[pattern-circuit-breaker]] — wrap outbound gRPC clients.
