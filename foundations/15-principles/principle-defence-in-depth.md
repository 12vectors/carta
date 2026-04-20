---
id: principle-defence-in-depth
title: Defence in Depth
type: principle
maturity: stable
pillar: "[[pillar-security]]"
related_patterns:
  - "[[pattern-input-validation]]"
  - "[[pattern-rbac]]"
  - "[[pattern-oauth2-authorization]]"
  - "[[pattern-secrets-management]]"
tags: [principle, stable, security]
---

## Statement

Never rely on a single control. Every security boundary must assume the outer layer has already been breached.

## Rationale

Perimeter defences fail — a stolen credential, a misconfigured firewall rule, a supply-chain compromise. A system that depends on any one control has a single point of compromise. Layered controls turn a single failure into a contained incident.

## How to apply

- Validate at every trust boundary, not only at the edge.
- Require authentication and authorisation on internal APIs, not only external.
- Encrypt data in transit and at rest, independently.
- Separate duties so no one credential grants end-to-end control.
- Assume the code on the other side is hostile until proven otherwise.

## Related patterns

- [[pattern-input-validation]] — each parser and boundary validates, not only the API gateway.
- [[pattern-rbac]] — narrow scopes at each layer.
- [[pattern-oauth2-authorization]] — short-lived tokens over long-lived secrets.
- [[pattern-secrets-management]] — centralise and rotate.
