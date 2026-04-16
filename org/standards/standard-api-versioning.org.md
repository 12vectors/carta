---
id: standard-api-versioning
title: "API Versioning (Org)"
type: standard
category: api
maturity: stable
tags: [standard, stable, api]
applies_to:
  - "[[context-web-application]]"
enforceability: automated
related:
  - "[[pattern-rest-api]]"
sources:
  - "https://stripe.com/docs/api/versioning"
---

## Requirement

All public and internal APIs MUST use URL-path versioning. Every API endpoint is served under a version prefix that forms part of the base path:

```
/v1/payments
/v1/payments/{id}
/v2/payments
/v2/payments/{id}
```

The version prefix follows the format `/vN/` where `N` is a positive integer. There is no `/v0/` -- the first released version is `/v1/`.

A new major version (`/v2/`, `/v3/`) is introduced only when a breaking change cannot be avoided. Non-breaking additions (new optional fields, new endpoints) are added to the current version without incrementing.

When a new major version is introduced, the previous version MUST remain available for a minimum deprecation period of six months. Deprecated versions return a `Deprecation` header with the sunset date.

## Rationale

URL-path versioning is the most visible and least error-prone approach to API versioning:

- **Visibility.** The version is part of the URL, which appears in logs, documentation, monitoring dashboards, and browser address bars. There is no ambiguity about which version a request targets.
- **Simplicity.** Clients specify the version by changing the URL path. No custom headers, no content negotiation, no query parameters. Any HTTP client -- including `curl` with no flags -- can target a specific version.
- **Routability.** Load balancers, API gateways, and reverse proxies can route by URL path without inspecting headers. This enables version-specific scaling, canary deployments, and gradual migration.
- **Avoids invisible breaking changes.** Header-based versioning (`Accept: application/vnd.api.v2+json`) or query-parameter versioning (`?version=2`) are easy to forget and hard to audit. When the version is in the path, omitting it results in a `404`, not a silent fallback to an unexpected version.

## Compliance

A service is compliant when:

- All API endpoints are served under a `/vN/` path prefix (e.g. `/v1/users`, `/v2/orders`).
- The OpenAPI spec includes the version prefix in every path definition.
- CI includes a lint check that verifies all route definitions start with a version prefix. FastAPI services can validate this by inspecting the generated OpenAPI schema in a test.
- Deprecated versions include a `Deprecation` response header with the sunset date.

## Non-compliance

The following are non-compliant and will be flagged by automated checks:

- API endpoints without a version prefix in the URL path (e.g. `/payments` instead of `/v1/payments`).
- Header-only versioning (e.g. `Accept: application/vnd.api.v2+json`) without a corresponding URL-path version.
- Query-parameter versioning (e.g. `/payments?version=2`).
- Removing a deprecated version before the six-month sunset period has elapsed.

## See also

- [[pattern-rest-api]] -- org-level REST API pattern that references this standard
- [[adr-0001-fastapi-as-default.org]] -- FastAPI is the default framework; its router must enforce versioned paths
