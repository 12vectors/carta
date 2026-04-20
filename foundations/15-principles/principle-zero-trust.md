---
id: principle-zero-trust
title: Zero Trust
type: principle
maturity: stable
pillar: "[[pillar-security]]"
related_patterns:
  - "[[pattern-oauth2-authorization]]"
  - "[[pattern-federated-identity]]"
  - "[[pattern-input-validation]]"
tags: [principle, stable, security, zero-trust]
---

## Statement

Verify every request, every time. Network location is not a trust signal.

## Rationale

The perimeter model assumes "inside" is safe and "outside" is hostile. Modern deployments — cloud, containers, service mesh, third-party SaaS — have no useful perimeter. A workload running inside the VPC is no more trustworthy than one on the public internet once an attacker has a foothold.

## How to apply

- Authenticate and authorise every request, including east-west traffic between services.
- Use cryptographic identity (mTLS, signed tokens), not IP allowlists, as the trust signal.
- Assume any service can be compromised; verify what callers claim about themselves.
- Log and audit cross-service calls as carefully as edge calls.

## Related patterns

- [[pattern-oauth2-authorization]] — token-based auth for service-to-service.
- [[pattern-federated-identity]] — single identity provider across domains.
- [[pattern-input-validation]] — trust nothing a caller provides without checking.
