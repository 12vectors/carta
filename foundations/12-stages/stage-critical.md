---
id: stage-critical
title: Mission-Critical
type: stage
maturity: stable
tags: [stage, stable, critical, mission-critical]
typical_antipatterns: []
related:
  - "[[stage-production]]"
sources:
  - "https://learn.microsoft.com/en-us/azure/well-architected/mission-critical/"
  - "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/"
  - "Site Reliability Engineering (Beyer et al., O'Reilly, 2016) ch. 26 'Data Integrity' — https://sre.google/sre-book/data-integrity/"
---

## Description

Mission-critical systems carry consequences beyond revenue: patient safety, financial settlement, power-grid control, air-traffic, emergency services, large-scale consumer platforms where downtime means visible public impact. Downtime is measured in minutes per year, not per month. The team is a dedicated SRE or platform function separate from feature development. Compliance audits, disaster recovery drills, and chaos engineering are scheduled programs, not ad-hoc practices. Every change carries proof-of-safety, not just proof-of-value. This is not where you start; most systems never need this stage, and reaching for it prematurely burns money and velocity without buying proportional safety.

## What relaxes

Nothing relaxes relative to [[stage-production]]. The difference between production and critical is that everything is **harder**, **more frequent**, and **more formally owned**. A "we can't do that yet, we're at production stage" answer is no longer available.

The closest thing to a relaxation: **delivery velocity is explicitly deprioritised when it conflicts with safety**. Shipping a feature late to maintain change-freeze around a compliance window, a regulatory audit, or a DR drill is correct, not an operational failure.

## What stays baseline

Everything in [[stage-production]]'s baseline, plus:

- **Multi-region active-active or active-passive with automated failover.** Tested — not aspirational — with documented RTO and RPO.
- **Chaos engineering as a scheduled program.** Regular fault-injection exercises with documented results and action items.
- **Compliance certifications appropriate to domain.** SOC 2 Type II, HIPAA, PCI-DSS, FedRAMP, ISO 27001, HITRUST — whichever apply, fully maintained.
- **Formal disaster recovery drills** multiple times per year. RTO and RPO are hit or the drill counts as a failure requiring remediation.
- **Dedicated SRE or platform organisation** separate from feature teams.
- **Error budget policy with teeth.** Feature work actually stops when the budget is exhausted; leadership understands and enforces this.
- **Every dependency classified.** Tier-1 dependencies have fallbacks or explicit "we accept this outage" decisions signed by accountable leadership.
- **Change approval process** with explicit risk tiers and approval levels. Emergency change has its own codified path.
- **Blameless post-incident review on every event**, published within defined windows, with tracked action items.
- **Capacity and load testing at peak + headroom**, regularly re-run.
- **Data integrity monitoring and periodic reconciliation.** Not just "the DB is up" — "the data is still right".

## Typical antipatterns

- **Cargo-cult critical** — a team adopts mission-critical ceremony (error budgets, SRE rotation, chaos days) without the underlying SLOs or business need. Overhead dominates output without safety gain.
- **Compliance-as-theatre** — certifications are maintained formally but the practices are disconnected from the actual operational posture.
- **Hero operations** — the system looks mission-critical from the outside but survives on a small number of highly-tenured individuals whose departure would expose the gap.

## See also

- [[stage-production]] — the previous stage; most systems stop here appropriately.
- [[pattern-deployment-stamps]], [[pattern-geode]] — deployment shapes that mission-critical workloads commonly adopt.
- [[pattern-saga]], [[pattern-compensating-transaction]] — transactional integrity without distributed 2PC, which matters more here than anywhere else.
- [[principle-design-for-failure]] — the principle lived in full at this stage.
