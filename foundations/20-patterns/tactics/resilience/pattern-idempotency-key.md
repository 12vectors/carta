---
id: pattern-idempotency-key
title: Idempotency Key
type: pattern
category: resilience
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, resilience, fault-tolerance, api]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-compensating-transaction]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Designing robust and predictable APIs with idempotency (Stripe Engineering, 2017) — https://stripe.com/blog/idempotency"
---

## When to use

- Non-idempotent write endpoints (POST create, payment, transfer, send).
- Any API whose clients will retry on network or 5xx errors.
- Message consumers with at-least-once delivery semantics.
- Mobile or flaky-network clients where double-submit is likely.
- Financial, inventory, or side-effecting operations where duplicates cost money.

## When NOT to use

- Naturally idempotent operations (PUT full replace, DELETE by id).
- Read-only endpoints.
- Operations where duplicates are harmless and storage of keys costs more.

## Decision inputs

- Key source — client-supplied header vs server-derived hash of payload.
- Retention window (typically 24h-7d) balancing safety vs storage.
- Scope of the key (per account, per endpoint, global).
- Storage backend latency — lookup is on the hot path of every write.
- Behaviour on payload mismatch for the same key (reject vs replay).

## Solution sketch

Client sends `Idempotency-Key: <uuid>` on each write. Server atomically records the key with the request fingerprint and response. Second request with the same key returns the stored response without re-executing. On in-flight duplicates, return 409 or block on the first. Store fingerprint (hash of method + path + body) to detect key reuse with a different payload — reject with 422.

```
POST /charges  Idempotency-Key: abc
  └─ first  → execute, store (abc, fingerprint, 200, body), return 200
  └─ retry  → lookup abc → return stored 200
  └─ reuse  → fingerprint differs → 422
```

See Stripe Engineering (linked in sources) for storage, locking, and edge cases.

## Trade-offs

| Gain | Cost |
|------|------|
| Safe retries for non-idempotent writes | Extra storage and an atomic lookup on every write |
| Enables at-least-once messaging without duplicate side effects | Clients must generate and persist keys correctly |
| Deterministic client behaviour under network faults | Retention window bounds replay safety |
| Decouples retry safety from endpoint design | Fingerprint mismatch handling adds API surface |

## Implementation checklist

- [ ] Define an `Idempotency-Key` header contract (format, length, scope).
- [ ] Store key, request fingerprint, response, and status atomically.
- [ ] Lock or reserve the key before executing to handle concurrent retries.
- [ ] Return the stored response byte-for-byte on replay.
- [ ] Reject payload mismatches on a reused key with 422.
- [ ] Set a retention TTL; document it to clients.
- [ ] Expose key handling in client SDKs so retries attach the same key.
- [ ] Test concurrent duplicates, payload mismatch, and expiry edges.

## See also

- [[pattern-retry-with-backoff]] — idempotency keys make retries safe.
- [[pattern-compensating-transaction]] — alternative when idempotency is impractical.
- [[pattern-rest-api]] — header-based contract fits REST semantics.
