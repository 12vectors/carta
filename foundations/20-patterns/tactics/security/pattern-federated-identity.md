---
id: pattern-federated-identity
title: Federated Identity
type: pattern
category: security
maturity: stable
pillars:
  - "[[pillar-security]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, security, identity, sso, federation]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-oauth2-authorization]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/federated-identity"
---

## When to use

- Enterprise B2B where customers bring their own IdP (Okta, Azure AD, Google Workspace).
- Consumer sign-in via social providers (Google, Apple, GitHub) to reduce signup friction.
- Internal SSO across multiple apps with one corporate identity.
- Regulated environments where the customer insists on controlling deprovisioning.
- Acquisitions / multi-brand setups consolidating onto one auth surface.

## When NOT to use

- Tiny consumer app with no SSO demand and low signup friction already.
- Air-gapped or offline-first systems where external IdP reachability is an operational risk.
- When the IdP cannot be trusted (low-assurance providers) for the sensitivity of the app.
- If every customer wants a distinct auth model — federation cannot paper over divergent requirements.

## Decision inputs

- Protocol: **OIDC** (modern, JWT-based) vs **SAML 2.0** (enterprise legacy, XML, still common).
- IdP trust: single social, multiple social, customer-brought enterprise IdP, or all.
- Provisioning: JIT on first login vs **SCIM** for full lifecycle (create, update, deprovision).
- Identity linking strategy: email-based merge vs strict-per-IdP accounts.
- Claims mapping: group → role, department → tenant, etc.
- Session model: local session after federation, or re-federate per request.

## Solution sketch

App delegates authentication to an external IdP; the IdP returns an assertion the app trusts.

```
User --> App --redirect--> IdP --(authn)--> IdP --assertion (JWT/SAML)--> App --local session--> App
```

- Use **OIDC** for new integrations; support **SAML** for enterprise buyers who require it.
- Validate signature, `iss`, `aud`, `exp`, and replay protection (`nonce`/`jti`).
- Map IdP groups/attributes to roles on ingest — never trust client-supplied role claims.
- **Provisioning**: JIT for low-assurance; **SCIM** for enterprise to enable deprovisioning.
- Handle identity linking explicitly — account takeover via email merge is a common attack.

See Azure architecture pattern for multi-IdP and claims-transformation patterns.

## Trade-offs

| Gain | Cost |
|------|------|
| Offload password storage, MFA, and account recovery | External dependency on every login path |
| Enterprise-ready; unblocks B2B sales | Protocol complexity (especially SAML) is a perennial footgun |
| Single sign-on across multiple apps | Identity linking and deprovisioning require deliberate design |
| Reduces signup friction (social login) | IdP outage = app outage unless session TTLs buffer it |
| Compliance-friendly (customer controls their identities) | Claims mapping drift between IdPs is an ongoing tax |

## Implementation checklist

- [ ] Pick OIDC as default; add SAML only when required by a buyer.
- [ ] Use a hardened broker or IdP (Auth0, Okta, Keycloak, Cognito) — do not roll your own.
- [ ] Validate all assertion claims: signature, `iss`, `aud`, `exp`, `nonce`.
- [ ] Define the account-linking policy (strict, verified-email merge) before launch.
- [ ] Map IdP groups to roles on ingest; reject unmapped groups.
- [ ] Implement SCIM for enterprise tenants to support deprovisioning SLAs.
- [ ] Log every federated login with subject, IdP, and claims snapshot.
- [ ] Handle IdP outage gracefully: cached sessions, clear error UX, break-glass for admins.
- [ ] Test logout: propagate to IdP (single logout) where required.

## See also

- [[pattern-oauth2-authorization]] — OIDC is OAuth2 + identity; federation reuses its flows.
- [[pattern-rbac]] — map IdP groups to roles; roles decide permissions.
- [[pattern-secrets-management]] — store IdP client secrets and signing keys in the vault.
