---
id: pattern-oauth2-authorization
title: OAuth 2.0 Authorization
type: pattern
category: security
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-security]]"
tags: [pattern, stable, security, oauth2, authorization, delegated-access]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-federated-identity]]"
  - "[[pattern-rbac]]"
conflicts_with: []
contradicted_by: []
sources:
  - "RFC 6749 -- https://datatracker.ietf.org/doc/html/rfc6749"
  - "OAuth 2 in Action (Richer & Sanso, Manning, 2017) -- https://www.manning.com/books/oauth-2-in-action"
---

## When to use

- Third-party apps need delegated access to a user's resources without the password.
- Public APIs exposing per-user data to first- and third-party clients.
- Mobile and SPA clients requiring short-lived tokens and refresh flows.
- Machine-to-machine auth between services (client-credentials grant).
- Single provider issuing tokens consumed by many resource servers.

## When NOT to use

- Pure first-party session auth with no third-party clients — a session cookie is simpler.
- Internal service mesh with mTLS and SPIFFE identities already solving the problem.
- When user identity is the goal, not delegated authorisation — use OIDC on top, not raw OAuth2.
- Legacy endpoints unable to validate JWTs or introspect opaque tokens.

## Decision inputs

- Grant type: **authorization_code + PKCE** (interactive), **client_credentials** (M2M), avoid implicit and ROPC.
- Token format: JWT (self-contained, offline validation) vs opaque (introspection endpoint, revocable).
- Token TTLs: access short (5–60 min), refresh long but rotated.
- Scopes: granular enough to enforce least privilege; small enough to audit.
- Client confidentiality: confidential (server) vs public (SPA, mobile) — PKCE is mandatory for public.
- Use off-the-shelf IdP (Auth0, Okta, Keycloak, Cognito) vs build — almost always buy.

## Solution sketch

Four roles: **resource owner**, **client**, **authorisation server (AS)**, **resource server (RS)**.

```
Client --authz code + PKCE--> AS --code--> Client --code--> AS --access+refresh token--> Client
Client --access token--> RS --validate (JWKS or introspect)--> response
```

- Use **authorization_code + PKCE** for all user-facing flows (web, SPA, mobile).
- Use **client_credentials** for service-to-service.
- Validate JWTs with the IdP's JWKS; cache keys, respect `kid` rotation.
- Enforce `aud`, `iss`, `exp`, and required scopes on every request.
- Rotate refresh tokens on each use; detect reuse as theft.

Deprecated: implicit grant, resource-owner password credentials. See RFC 6749 and OAuth 2 in Action for full flows.

## Trade-offs

| Gain | Cost |
|------|------|
| Standard, interoperable, library-rich | Spec is broad; misconfiguration is the #1 failure mode |
| Short-lived tokens limit compromise blast radius | Token lifecycle (refresh, rotation, revocation) adds client complexity |
| Delegated access without sharing passwords | Scope design is hard; overbroad scopes defeat least privilege |
| Decouples authN from authZ and from each RS | JWTs are hard to revoke before expiry without introspection |
| M2M and user flows under one framework | Implementing AS yourself is a security footgun — use an IdP |

## Implementation checklist

- [ ] Use a hardened IdP; do not build the AS yourself.
- [ ] Enforce PKCE on every public client; reject flows without it.
- [ ] Validate `iss`, `aud`, `exp`, `nbf`, and `scope` on every token.
- [ ] Short access-token TTL; rotate refresh tokens and detect reuse.
- [ ] Define scopes aligned with resources, not roles — pair with RBAC for roles.
- [ ] Use HTTPS everywhere; reject `http://` redirect URIs.
- [ ] Pin allowed redirect URIs exactly; no wildcards on host or path.
- [ ] Log token issuance, refresh, and revocation with client + subject IDs.
- [ ] Support token revocation and logout; propagate to RS via introspection or short TTL.

## See also

- [[pattern-federated-identity]] — layer OIDC on top of OAuth2 when user identity is needed.
- [[pattern-rbac]] — scopes grant delegated access; RBAC decides what the subject can do.
- [[pattern-secrets-management]] — client secrets and signing keys belong in a vault, not env files.
