---
id: pattern-claim-check
title: Claim Check
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-cost]]"
tags: [pattern, stable, messaging, large-payload, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-message-translator]]"
  - "[[pattern-publish-subscribe]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/claim-check"
  - "EIP (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/StoreInLibrary.html"
---

## When to use

- Payloads exceed broker limits (SQS 256KB, SNS 256KB, Kafka message size cap).
- Large binary attachments (images, PDFs, ML models) must flow through the pipeline.
- Most intermediate stages do not need the full payload — only identity or metadata.
- Fan-out to many subscribers; replicating the blob is expensive.
- Compliance requires the payload be stored once, in a controlled bucket.

## When NOT to use

- Payloads comfortably fit in the broker — extra hop is pure cost.
- End-to-end latency is tight and the blob fetch round-trip breaks the budget.
- Every consumer always needs the full payload — replication cost may still win.
- No shared, durable object store is available with matching access control.

## Decision inputs

- Payload size distribution vs broker limits.
- Object-store latency and cost per GET/PUT at expected volume.
- Retention: when is the blob safe to delete?
- Access control — who can read the claim?
- Encryption at rest; key management for the blob store.
- Who owns lifecycle (TTL, cleanup) for orphaned blobs?

## Solution sketch

Producer uploads the large payload to an object store and sends a small reference ("claim check") on the queue. Consumers fetch the payload on demand using the reference.

```
[Producer] --PUT blob--> [Object Store]
     \--send(ref)--> [Queue] --> [Consumer] --GET blob--> [Object Store]
```

- Reference should be immutable (content-addressed ID or versioned key).
- Include enough metadata inline for routing decisions — avoid a blob fetch just to route.
- Enforce short-lived signed URLs or IAM-scoped access, not public reads.
- Define a cleanup policy: TTL, lifecycle rule, or consumer-ack-triggered delete.
- Do not leak blob keys into logs — they are access tokens.

## Trade-offs

| Gain | Cost |
|------|------|
| Messages stay small — fits broker limits and cheap to fan out | Extra round-trip to the object store per consumer |
| Payload stored once regardless of subscriber count | Two systems to operate and secure (broker + store) |
| Orthogonal lifecycle: broker retention independent of blob retention | Orphan blobs if cleanup is not wired |
| Routing metadata stays lightweight and scannable | Access-control surface widens — claims become credentials |

## Implementation checklist

- [ ] Set a size threshold above which producers use claim check automatically.
- [ ] Use content-addressed or versioned keys — never mutable paths.
- [ ] Sign URLs or scope IAM per-consumer; no anonymous access.
- [ ] Encrypt blobs at rest; rotate keys per policy.
- [ ] Wire a cleanup path — TTL, lifecycle rule, or explicit delete.
- [ ] Include enough inline metadata to route without fetching.
- [ ] Monitor orphan-blob count and age.
- [ ] Test consumer behaviour when the blob is missing or expired.

## See also

- [[pattern-publish-subscribe]] — claim check scales fan-out by not replicating payload.
- [[pattern-message-translator]] — often inserted to swap inline payload for a claim.
- [[pattern-dead-letter-channel]] — DLQ messages must still resolve or expire their claims.
