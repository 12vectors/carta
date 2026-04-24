---
id: pattern-build-once-deploy-many
title: Build Once, Deploy Many
type: pattern
category: delivery
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, delivery, artefacts]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
prerequisites: []
related:
  - "[[pattern-deployment-pipeline]]"
  - "[[pattern-preview-environment]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Continuous Delivery (Humble & Farley, Addison-Wesley 2010) ch. 5 — 'Only Build Your Binaries Once'"
  - "Continuous Integration (Martin Fowler, 2024 rev): https://martinfowler.com/articles/continuousIntegration.html"
---

## When to use

- Deploying the same code to multiple environments (dev, staging, prod).
- Environments differ only in configuration, not in built artefact.
- Supply-chain provenance matters — the artefact deployed to prod must be the one tested.
- Rollback must produce the exact prior artefact, not a rebuild of old source.

## When NOT to use

- Truly environment-specific builds (e.g. native per-arch binaries) — but even then, build each arch once and deploy many.
- Static-site previews where rebuilding is cheaper than artefact management.

## Decision inputs

- Artefact registry availability (OCI registry, Maven, npm, internal store).
- Config separation — can all environment differences live in env vars / config files?
- Rollback SLO — how fast must you revert to a known-good artefact?
- Supply-chain requirements (SLSA, SBOM, signatures).

## Solution sketch

```
PR/main → build artefact → tag with commit SHA → push to registry
                              │
                              ├── deploy to staging (same image, staging config)
                              ├── deploy to canary   (same image, canary config)
                              └── deploy to prod     (same image, prod config)
```

Config is injected at deploy time (env vars, mounted config, secret store). The artefact is immutable and referenced by content-addressable ID across every environment.

## Trade-offs

| Gain | Cost |
|------|------|
| What you tested is what you deploy — no rebuild drift | Requires an artefact registry and artefact retention |
| Rollback is "redeploy tag X", not "revert + rebuild" | Config mistakes can't be caught at build time |
| Supply-chain provenance becomes tractable | Environment-specific assets must be handled separately or baked as side files |

## Implementation checklist

- [ ] Build the artefact once in the PR or main pipeline; tag with commit SHA.
- [ ] Push to a registry with retention covering at least your rollback window.
- [ ] Forbid per-environment rebuilds — deploy pulls by tag, never rebuilds from source.
- [ ] Externalise all environment differences into config/env/secret.
- [ ] Sign artefacts; verify signature on deploy.
- [ ] Keep a manifest linking commit SHA → artefact digest → deployed environments.

## See also

- [[pattern-deployment-pipeline]] — the pipeline this artefact flows through.
- [[pattern-preview-environment]] — reuses the same artefact per PR.
