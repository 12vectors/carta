---
id: stage-mvp
title: MVP (Minimum Viable Product)
type: stage
maturity: stable
tags: [stage, stable, mvp, alpha, beta]
next_stage: "[[stage-production]]"
typical_antipatterns: []
related:
  - "[[stage-prototype]]"
  - "[[stage-production]]"
sources:
  - "The Lean Startup (Ries, Crown Business, 2011)"
  - "https://martinfowler.com/bliki/MvpDefinition.html"
---

## Description

An MVP exposes the system to first real users — internal or external — to validate that the idea delivers value. A single team operates the system. The scale is tens to low thousands of users, not millions. Availability SLOs exist but are soft; a maintenance window is acceptable. The goal has shifted from learning whether it *could* work (prototype) to learning whether it *should* exist as a product. Real data enters the system; real incidents happen. The system is now a **first-class artefact**, not a spike.

## What relaxes

- **Multi-region and cross-region HA** — single region is fine; disaster recovery is a runbook, not automated failover.
- **Fine-grained per-tenant isolation** — multi-tenant at the row level is acceptable; full DB-per-tenant is usually premature.
- **Elaborate CI/CD pipelines** — a single pipeline with tests and a deploy step beats a multi-stage canary rig at this volume.
- **Progressive delivery** — blue-green or canary is optional if rollback is fast and traffic is low.
- **On-call rigour** — engineers on rotation get paged; a formal SRE playbook isn't yet required.
- **Deep cost-optimisation** — right-size once, revisit quarterly; per-request cost tracking is overkill.

## What stays baseline

- **Authentication on every endpoint.** No network-only trust. Even internal calls authenticate.
- **Authorization at the resource level.** Users cannot see or modify each other's data accidentally.
- **Secrets in a real store.** Env-at-runtime, a secret manager, or workload identity. Not files on disk, not committed.
- **Structured logging and error tracking.** Every request and every external call logs with correlation IDs. Errors go to Sentry or equivalent.
- **Health checks that reflect reality.** `/livez` + `/readyz` with real dependency checks. Orchestrator-driven restart works.
- **Automated backups of user data.** Restore tested at least once before first real user.
- **Tests on critical paths.** Unit for core logic, integration for the main request path, smoke for deploys.
- **CI on the main branch.** Nothing merges that fails tests.
- **Schema migrations are non-destructive.** Use [[pattern-expand-contract-migration]] for any structural change.

## Graduating

Moving to [[stage-production]] requires committing to operational rigour:

- Define explicit SLOs (availability, latency, error rate) and the error budget.
- Add on-call rotation, runbooks, and incident response process.
- Introduce circuit breakers on outbound dependencies ([[pattern-circuit-breaker]]).
- Adopt progressive delivery ([[pattern-canary-release]] or [[pattern-blue-green-deployment]]).
- Full observability: metrics, logs, traces, with dashboards team-owned.
- Rate-limiting on public surface to bound abuse.
- Load testing at expected peak × safety margin.

## Typical antipatterns

- **Frozen MVP** — the system stays at MVP for years; features accumulate without graduating operational maturity. Eventually a single failure takes it down and exposes the gap.
- **Invisible production** — what was an "MVP with a few pilot users" now has revenue and SLA commitments, but the operational stance is still MVP.

## See also

- [[stage-prototype]] — where most MVPs come from; the transition is the riskiest part.
- [[stage-production]] — the next stage; plan graduation deliberately, not emergently.
- [[pattern-oauth2-authorization]] — auth is MVP-mandatory.
- [[pattern-secrets-management]] — floor of MVP.
- [[pattern-structured-logging]] — you cannot debug MVP incidents without it.
