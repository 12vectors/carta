---
id: pattern-valet-key
title: Valet Key
type: pattern
category: security
maturity: stable
pillars:
  - "[[pillar-security]]"
  - "[[pillar-performance]]"
tags: [pattern, stable, security, valet-key, presigned-url, delegated-access]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-oauth2-authorization]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/valet-key"
---

## When to use

- Large file upload/download where streaming through the app tier wastes CPU and bandwidth.
- Direct-to-storage flows: S3, GCS, Azure Blob via presigned URLs / SAS tokens.
- Short-lived, narrowly scoped access to a specific object or prefix.
- Mobile/SPA clients that should not hold long-lived storage credentials.
- Cost optimisation: bypass app egress by serving direct from object store or CDN.

## When NOT to use

- Small payloads where proxying through the app is negligible.
- When the app needs to inspect, transform, or audit the bytes in flight.
- Object stores or services that cannot scope tokens tightly (object, action, TTL).
- When revocation before expiry is required — presigned URLs are hard to revoke.
- Regulated flows requiring server-side DLP or virus scanning on the hot path.

## Decision inputs

- Storage capability: presigned URLs (S3, GCS), SAS (Azure), signed cookies (CloudFront).
- TTL: short enough to bound leak blast radius (minutes), long enough to complete the transfer.
- Scope: exact object, HTTP method, content-type, max size, optional IP/VPC constraint.
- Issuer identity: the app signs with a long-lived key — protect it aggressively.
- Audit: server must log every issued token with subject, object, method, TTL.
- Post-upload processing model (event-driven scan, trigger, CDN invalidation).

## Solution sketch

App authenticates and authorises the caller, then mints a **narrow, short-lived token** for a specific object. Client transfers bytes directly with storage.

```
Client --request access--> App --(authz check)--> App --signed URL (obj, method, exp)--> Client
Client --upload/download--> Object Store
Object Store --event (ObjectCreated)--> App (scan, index, notify)
```

- Pin method (`PUT` vs `GET`), content-type, and size where the provider allows.
- Short TTL: 5–15 min is typical; longer is a liability.
- Scope to **one object key** — never a whole bucket or prefix unless absolutely required.
- Pair with server-side event handler for post-upload validation (scan, index).
- Protect the signing key in a vault; rotate on schedule and on suspected leak.

See Azure valet-key pattern for SAS specifics and delegation.

## Trade-offs

| Gain | Cost |
|------|------|
| Massive bandwidth and CPU savings in the app tier | Presigned tokens are bearer tokens — a leaked URL equals access |
| Scales uploads/downloads with the object store, not the app | Revocation before expiry is hard; keep TTLs short |
| Client can resume/parallelise transfers natively | Cannot inspect bytes in flight (no sync DLP, no virus scan) |
| Works for mobile/SPA without shipping storage creds | Signing key compromise is catastrophic — vault it |
| Cost drop: direct-from-store or CDN egress | Post-upload validation is async; UX must reflect that |

## Implementation checklist

- [ ] Authorise the caller server-side before signing any token.
- [ ] Set TTL to the minimum that fits the transfer (often 5–15 min).
- [ ] Scope to a single object key, method, and (where supported) content-type and size.
- [ ] Store the signing key in a vault; rotate on schedule.
- [ ] Log every issued token: subject, object, method, TTL, IP.
- [ ] Wire object-created events for post-upload scan/index/notify.
- [ ] Use HTTPS only; reject unsigned or expired requests at the store.
- [ ] For sensitive data, layer server-side encryption (KMS-managed keys).
- [ ] Document client retry behaviour for expired URLs — re-request, do not cache.

## See also

- [[pattern-oauth2-authorization]] — authenticate the caller with OAuth2; then issue the valet key.
- [[pattern-secrets-management]] — signing keys are high-value secrets; vault them.
- [[pattern-input-validation]] — validate metadata at token-issue time; validate bytes on upload event.
