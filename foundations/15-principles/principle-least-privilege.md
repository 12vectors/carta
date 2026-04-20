---
id: principle-least-privilege
title: Least Privilege
type: principle
maturity: stable
pillar: "[[pillar-security]]"
related_patterns:
  - "[[pattern-rbac]]"
  - "[[pattern-valet-key]]"
  - "[[pattern-secrets-management]]"
tags: [principle, stable, security, access-control]
---

## Statement

Grant the minimum access required for the job, for the minimum duration, at the narrowest scope.

## Rationale

Every permission granted is a permission that can be abused — by a compromised account, a misbehaving workload, or an insider. Tight scopes bound the blast radius of any single compromise. Broad defaults are convenient for developers and catastrophic for incident response.

## How to apply

- Default-deny; grant by explicit allowlist.
- Use short-lived, scoped tokens instead of long-lived secrets.
- Separate read from write; separate admin from operational.
- Revoke on role change; review access quarterly.
- Audit every privilege escalation.

## Related patterns

- [[pattern-rbac]] — role-scoped permissions.
- [[pattern-valet-key]] — short-lived, narrow-scope tokens for direct resource access.
- [[pattern-secrets-management]] — rotate, scope, and audit.
