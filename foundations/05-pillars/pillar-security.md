---
id: pillar-security
title: Security
type: pillar
maturity: stable
tags: [pillar, stable]
realised_by:
  - "[[principle-defence-in-depth]]"
  - "[[principle-least-privilege]]"
  - "[[principle-zero-trust]]"
tradeoffs_with:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-performance]]"
sources:
  - "https://learn.microsoft.com/en-us/azure/well-architected/security/"
  - "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/"
---

## Description

Security is the system's ability to protect confidentiality, integrity, and availability of data and function against adversaries. It covers authentication, authorisation, data protection in transit and at rest, input handling, secret management, and resilience to abuse.

## When this dominates

- Internet-facing services with untrusted inputs.
- Systems handling regulated data (PII, PHI, PCI, financial records).
- Multi-tenant platforms where one tenant's compromise must not propagate.
- Any system where unauthorised access carries outsized consequences.

## Trade-offs

| Gain | Cost |
|------|------|
| Reduced attack surface and blast radius | Extra validation, auth, and review loops slow delivery ([[pillar-operational-excellence]]) |
| Defence-in-depth catches failures at multiple layers | Each layer adds latency and compute ([[pillar-performance]]) |
| Strong audit and least-privilege boundaries | Developer friction; elevated-access workflows |

## Realised by

- [[principle-defence-in-depth]] — never rely on a single control.
- [[principle-least-privilege]] — grant the minimum access required.
- [[principle-zero-trust]] — verify every request, everywhere.
- [[pattern-input-validation]], [[pattern-oauth2-authorization]], [[pattern-rbac]], [[pattern-secrets-management]] — patterns that encode these principles.
