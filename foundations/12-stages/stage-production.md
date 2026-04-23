---
id: stage-production
title: Production
type: stage
maturity: stable
tags: [stage, stable, production]
next_stage: "[[stage-critical]]"
typical_antipatterns: []
related:
  - "[[stage-mvp]]"
  - "[[stage-critical]]"
sources:
  - "Site Reliability Engineering (Beyer et al., O'Reilly, 2016) — https://sre.google/sre-book/table-of-contents/"
  - "The Site Reliability Workbook (Beyer et al., O'Reilly, 2018) — https://sre.google/workbook/table-of-contents/"
  - "https://learn.microsoft.com/en-us/azure/well-architected/"
---

## Description

The system serves real users with real money attached. Downtime costs revenue, trust, or both. The team operates the system with on-call rotation, explicit SLOs, and error budgets. Scale is thousands to millions of users; incidents happen and must be diagnosed and recovered from, not just restarted. Changes go through progressive delivery — canary or blue-green — because a bad deploy is visible to everyone. The system is expected to run unattended through weekends, holidays, and vacations.

## What relaxes

- **Multi-region active-active** — single-region with tested failover is acceptable for most production workloads; active-active is usually over-engineering here.
- **Compliance audits at the highest level** — SOC 2 Type II and HIPAA-scope work is common, but FedRAMP, PCI, or medical-device certification belongs to mission-critical systems.
- **Zero-downtime deploys as mandatory** — short (seconds) switchover blips during rollout are usually acceptable if rollback is instant.
- **Chaos engineering as a regular practice** — valuable but not yet required; game days around planned changes suffice.
- **Formal DR drills every quarter** — an annual drill is standard production practice.

## What stays baseline

- **Explicit SLOs and error budgets.** Availability, latency P95/P99, error rate — measured, dashboarded, alerted.
- **Full observability stack.** Metrics ([[pattern-red-metrics]]), structured logs, distributed tracing with correlation IDs.
- **Outbound resilience.** Every external call has a timeout, retry with backoff, and a circuit breaker.
- **Progressive delivery.** Canary or blue-green on every deploy of the main service; feature flags for risky surfaces.
- **Rate limiting and abuse prevention.** Public surface has per-client limits; paid or expensive calls have budget caps.
- **Secrets manager with rotation.** Short-lived tokens, rotated on a schedule, audited.
- **CI/CD with automated tests and staged deploys.** Nothing goes to production without green signal; rollback is a click.
- **Runbooks for the top ten failure modes.** Not prose — executable checklists with explicit commands.
- **Backups with tested restore.** Quarterly drill at minimum; RPO and RTO are documented numbers.
- **On-call rotation with escalation.** Primary + secondary + manager escalation path; every page is reviewed.
- **Post-incident review on every customer-impacting event.** Blameless format, actionable follow-ups tracked.

## Graduating

Moving to [[stage-critical]] requires taking the floor significantly higher:

- Multi-region active-active or active-passive with tested automatic failover.
- Chaos engineering as a scheduled program, not a one-off game day.
- Compliance certifications appropriate to domain (PCI, HIPAA, FedRAMP, SOC 2 Type II, ISO 27001).
- Formal disaster recovery drills multiple times per year with documented RTO/RPO.
- Dedicated SRE or platform team separate from feature-developing teams.
- Error budget policy that **actively stops feature work** when exhausted.
- Every dependency has a fallback or a documented "we accept this outage" decision.

## Typical antipatterns

- **MVP-cost production** — the system is in production but the operational spend is still MVP-level; the first serious incident reveals the gap.
- **Observability theatre** — dashboards exist but no one owns them; alerts fire but no one acts; logs are captured but never searched.
- **SLO without budget** — SLOs are published but error budget exhaustion never actually slows feature work, so the SLO stops being a guardrail.

## See also

- [[stage-mvp]] — the previous stage; graduation is often quieter than it should be.
- [[stage-critical]] — the next stage; not all production systems need it.
- [[pattern-canary-release]], [[pattern-blue-green-deployment]], [[pattern-feature-flag]] — the progressive-delivery trio that defines production-grade release.
- [[pattern-circuit-breaker]], [[pattern-retry-with-backoff]], [[pattern-bulkhead]] — the resilience floor.
- [[principle-observe-before-optimising]] — production decisions are measured, not guessed.
