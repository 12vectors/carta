---
id: pattern-rbac
title: Role-Based Access Control
type: pattern
category: security
maturity: stable
pillars:
  - "[[pillar-security]]"
tags: [pattern, stable, security, rbac, authorization]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-oauth2-authorization]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Role-Based Access Control Models (Sandhu et al., IEEE Computer 1996) -- https://doi.org/10.1109/2.485845"
  - "NIST RBAC -- https://csrc.nist.gov/projects/role-based-access-control"
---

## When to use

- User populations group naturally into stable job functions (admin, editor, viewer, billing).
- Permissions are mostly resource-type scoped, not per-record.
- Audit requirements demand explainable access decisions.
- Mid-to-large org where per-user ACLs would explode combinatorially.
- Regulated environments (SOX, HIPAA) that require documented role definitions.

## When NOT to use

- Pure per-record ownership models ("only the author can edit") — use ReBAC or ownership checks.
- Highly dynamic or attribute-driven rules (time, location, risk) — use ABAC or policy engines.
- Tiny apps with two or three users — role overhead outweighs gain.
- When "role explosion" is already happening; reconsider with attributes or relationships.

## Decision inputs

- Number of distinct permissions and expected role count — above ~50 roles, reconsider ABAC/ReBAC.
- Role hierarchy needed? (RBAC1) vs flat roles (RBAC0).
- Static separation-of-duties constraints (RBAC2)?
- Scope of a role: global, per-tenant, per-resource-type, per-project.
- Assignment source: directory (SCIM/LDAP), IdP groups, or app-managed.
- Enforcement point: gateway, service middleware, DB row-level.

## Solution sketch

Core model: **users → roles → permissions**. Grant permissions to roles, assign roles to users.

```
User  ──(assigned)──▶ Role  ──(granted)──▶ Permission (resource, action)
```

- Start with **RBAC0** (flat roles). Add hierarchy (RBAC1) only when inheritance reduces duplication.
- Keep roles **business-named** (billing_admin), not permission-named (can_delete_invoice).
- Enforce at the service boundary — never trust client-side role data.
- Cache the user's role set in the session or token; invalidate on change.
- Combine with OAuth2 scopes: scopes limit the token's power; RBAC decides what the user can do.

See NIST RBAC spec for formal model (core, hierarchical, constrained, symmetric).

## Trade-offs

| Gain | Cost |
|------|------|
| Simple mental model; explainable to auditors | Role explosion if each edge case spawns a new role |
| Maps naturally to org structure and IdP groups | Poor fit for per-record or attribute-driven rules |
| Easy to grant/revoke at join/leave/role-change | Static — does not respond to context (time, risk, location) |
| Predictable performance — just a set lookup | Cross-tenant or cross-project scoping bolts on awkwardly |
| Wide library and framework support | Separation-of-duties rules add meaningful complexity |

## Implementation checklist

- [ ] Define roles from job functions, not from permissions.
- [ ] Enumerate permissions as (resource, action) pairs; avoid wildcards except for superuser.
- [ ] Enforce on the server; duplicate in UI only for UX.
- [ ] Sync role assignments from the IdP/directory — avoid app-local drift.
- [ ] Cache effective permissions per session; invalidate on role change.
- [ ] Log every authz denial and every privileged action with subject + role.
- [ ] Review roles quarterly; delete unused; split over-broad roles.
- [ ] Document separation-of-duties rules and enforce them at assignment time.
- [ ] Reach for ABAC/ReBAC when role count exceeds ~50 or per-record rules appear.

## See also

- [[pattern-oauth2-authorization]] — scopes constrain the token; RBAC constrains the user.
- [[pattern-input-validation]] — authorise only after validated, canonicalised input.
