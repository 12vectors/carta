---
id: pattern-preview-environment
title: Preview Environment
type: pattern
category: delivery
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, delivery, review]
applies_to:
  - "[[context-web-application]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
prerequisites:
  - "[[pattern-build-once-deploy-many]]"
related:
  - "[[pattern-deployment-pipeline]]"
  - "[[pattern-trunk-based-development]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Vercel Preview Deployments: https://vercel.com/docs/deployments/preview-deployments"
  - "Continuous Delivery (Humble & Farley, Addison-Wesley 2010) ch. 5 — on per-change deployable environments"
---

## When to use

- Review cycles where "does it work?" is a meaningful question a reviewer should answer without local setup.
- Frontend and full-stack apps where behaviour is hard to assess from a diff.
- Demo or stakeholder review of in-flight work.
- Testing integrations against real downstream services before merge.

## When NOT to use

- Backend services where contract tests already cover the review surface.
- Stateful systems where spinning up a fresh copy is prohibitively expensive.
- Environments requiring production-equivalent data that can't be safely cloned.

## Decision inputs

- Per-environment spin-up cost (compute, data provisioning).
- Secret and data isolation requirements.
- External integrations — do you need sandbox accounts for downstreams?
- Auto-teardown policy (on merge, on stale, on close).
- Cost budget — one env per open PR adds up fast.

## Solution sketch

```
PR opened     → pipeline builds artefact → deploys to preview-<PR-number>.<domain>
PR push       → redeploys preview
PR merged/closed → preview torn down
```

Each PR gets an isolated URL. The same artefact deployed to prod (via [[pattern-build-once-deploy-many]]) is deployed to preview with a per-preview config. Reviewers click the link to test behaviour, not just read code.

## Trade-offs

| Gain | Cost |
|------|------|
| Reviewers assess behaviour, not diffs | Infra cost per open PR; TTL hygiene matters |
| Stakeholders preview without local setup | Data isolation and secret scoping must be deliberate |
| Catches integration issues before merge | External-service sandboxes may not reflect prod |

## Implementation checklist

- [ ] Automate spin-up on PR open and teardown on close/merge.
- [ ] Use the same artefact as prod ([[pattern-build-once-deploy-many]]); differ only in config.
- [ ] Isolate data — per-preview schema, ephemeral seed, no prod data.
- [ ] Scope secrets to preview; never grant prod credentials.
- [ ] Enforce a TTL — tear down stale previews after N days regardless.
- [ ] Post the preview URL to the PR for one-click reviewer access.

## See also

- [[pattern-build-once-deploy-many]] — prerequisite; preview uses the same artefact.
- [[pattern-deployment-pipeline]] — preview is one of its targets.
