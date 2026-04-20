---
id: pattern-async-request-reply
title: Async Request-Reply
type: pattern
category: communication
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-reliability]]"
tags: [pattern, stable, api, async, http]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-competing-consumers]]"
  - "[[pattern-publish-subscribe]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply"
---

## When to use

- Operation takes longer than a reasonable HTTP timeout (seconds to minutes).
- Client is a browser or mobile app that cannot hold a long-lived connection.
- Workload benefits from queue-based load levelling and horizontal workers.
- Caller needs an acknowledgement now but can poll or receive a callback later.

## When NOT to use

- Operation completes in well under the client timeout — synchronous is simpler.
- True streaming required — use WebSockets, SSE, or gRPC streaming.
- Caller cannot handle polling or callback mechanics (strict legacy client).
- Fire-and-forget is acceptable — no reply needed, use plain messaging.

## Decision inputs

- Expected P95/P99 work duration vs client timeout budget.
- Client capability — can it poll, or does it need webhook/push?
- Idempotency model for retries and duplicate submissions.
- Status-endpoint retention — how long do results stay queryable?
- Failure semantics — surface partial progress or only terminal states?

## Solution sketch

Client POSTs the work; server returns `202 Accepted` with a `Location` header pointing to a status resource and a retry hint. Work runs asynchronously (often on a queue + workers). Client polls the status URL: `200` with result when done, `202` while running, `4xx/5xx` on failure. For push, register a webhook URL at submission; server POSTs the result when ready. Use an idempotency key on submission to make retries safe.

```
POST /jobs                      202 Accepted
                                Location: /jobs/{id}
                                Retry-After: 5

GET /jobs/{id}   ──> 202 (running) | 200 (done, result) | 4xx/5xx
```

See the Azure architecture centre article for polling-vs-callback trade-offs and status-shape examples.

## Trade-offs

| Gain | Cost |
|------|------|
| Client freed from long connections; browsers/mobile friendly | Two-step protocol — client must implement polling or webhooks |
| Backend can queue and scale workers independently | Status store needed; retention and cleanup policy required |
| Natural back-pressure and failure isolation | Result correlation via job ID adds bookkeeping |
| Retry-safe with idempotency keys | End-to-end latency visible as "time to done", not request RTT |

## Implementation checklist

- [ ] `202 Accepted` with `Location` and `Retry-After` on submission.
- [ ] Job status resource: running / succeeded / failed with structured error.
- [ ] Idempotency key on submit; duplicates return the existing job.
- [ ] Worker pool consumes from a durable queue with DLQ on repeated failure.
- [ ] Status retention policy (TTL) documented and enforced.
- [ ] Optional webhook callback with signed payload; retries with backoff.
- [ ] Correlation ID propagated from submit through worker through status.
- [ ] Client guidance: backoff schedule for polling; give up after N attempts.

## See also

- [[pattern-competing-consumers]] — worker pool that drains the job queue.
- [[pattern-publish-subscribe]] — fan out job completion to interested parties.
- [[pattern-idempotency-key]] — makes submit-retries safe.
- [[pattern-queue-based-load-leveling]] — the usual back-end for async jobs.
