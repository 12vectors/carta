---
id: pattern-deployment-stamps
title: Deployment Stamps
type: pattern
category: deployment
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-cost]]"
tags: [pattern, stable, deployment, multi-tenancy, isolation]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-geode]]"
  - "[[pattern-microservices]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp"
---

## When to use

- Scaling beyond the limits of a single deployment (DB, quota, region).
- Tenant isolation for compliance, noisy-neighbour, or blast-radius reasons.
- Phased rollout where new versions hit one stamp before the rest.
- Regional data residency requirements per customer or market.

## When NOT to use

- Small systems well within single-deployment limits — complexity outweighs gain.
- Tightly coupled data requiring global consistency across all tenants.
- Teams without automation to provision and operate stamps identically.
- When a simple horizontal-scale tier already solves the problem.

## Decision inputs

- Stamp unit — region, tenant group, or scale bucket.
- Tenant-to-stamp routing — directory service, subdomain, or tenant-ID hash.
- Shared vs. stamp-local state (auth, billing, catalog).
- Cross-stamp operations — none, read-only aggregation, or full replication.
- Provisioning automation — IaC, GitOps, or platform service.

## Solution sketch

Package the full service stack — compute, data, cache, queues — as a repeatable **stamp**. Provision N stamps, each serving a disjoint subset of tenants. A thin routing layer (gateway, DNS, or directory lookup) maps each tenant to its stamp. Stamps are independent failure domains; a stamp outage affects only its tenants. Shared control-plane services (identity, billing) live outside the stamps.

```
[router] --tenant-A--> [stamp-1: app + db + cache]
         \--tenant-B--> [stamp-2: app + db + cache]
         \--tenant-C--> [stamp-3: app + db + cache]
```

See the Microsoft docs for reference architectures.

## Trade-offs

| Gain | Cost |
|------|------|
| Blast radius bounded by stamp | Provisioning, upgrade, and migration complexity |
| Horizontal scale past single-deployment limits | Cross-tenant features (shared state) are harder |
| Per-stamp rollout enables progressive deployment | Fleet-wide changes touch every stamp |
| Regional data residency supported directly | Higher baseline cost — fixed overhead per stamp |

## Implementation checklist

- [ ] Define the stamp unit and the tenant-to-stamp mapping.
- [ ] Automate stamp provisioning end-to-end (IaC).
- [ ] Build a routing layer with tenant lookup.
- [ ] Identify shared control-plane services and keep them outside stamps.
- [ ] Plan tenant-migration procedure between stamps.
- [ ] Apply schema and config changes via automated fleet rollout.
- [ ] Monitor per-stamp SLIs separately, not just in aggregate.
- [ ] Test a full stamp failure — including tenant-impact containment.
- [ ] Budget fixed per-stamp cost against expected tenant density.

## See also

- [[pattern-geode]] — geographic specialisation with active-active routing.
- [[pattern-microservices]] — stamps often package a microservices stack as a unit.
