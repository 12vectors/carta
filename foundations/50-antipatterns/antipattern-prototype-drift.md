---
id: antipattern-prototype-drift
title: Prototype Drift
type: antipattern
category: refactoring
maturity: stable
tags: [antipattern, stable, refactoring, lifecycle, operations]
applies_to:
  - "[[context-web-application]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-ml-system]]"
mitigated_by:
  - "[[pattern-oauth2-authorization]]"
  - "[[pattern-secrets-management]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-health-check-endpoint]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-strangler-fig]]"
sources:
  - "The Pragmatic Programmer, 20th Anniversary Edition (Hunt & Thomas, Addison-Wesley, 2019) — 'Broken Windows'"
  - "Site Reliability Engineering (Beyer et al., O'Reilly, 2016) ch. 27 'Reliable Product Launches at Scale' — https://sre.google/sre-book/reliable-product-launches/"
---

## How to recognise

- System is deployed at a reachable URL (not localhost) but was authored under [[stage-prototype]] assumptions.
- Production data is in play — real API keys, real user data, real billable LLM calls — without the MVP baselines in place.
- No authentication on a system accessed from outside the developer's machine.
- Secrets committed to the repo or stored in plaintext on disk.
- Background jobs crash silently; no on-call owner; no error tracking.
- README still says "prototype" or is silent on stage — and "we'll fix it after we ship" was said more than six months ago.

## Why it happens

- A demo was shown to a stakeholder, they asked "can we just use it?", and no one scheduled the hardening.
- Feature pressure outpaces graduation work; MVP baselines never land.
- The team that built the prototype is no longer the team operating it; institutional memory of the prototype label drains.
- The original author left; inheritors treat the system as it appears (production-shaped URL) rather than as it was authored.
- No explicit graduation criteria — the transition from prototype to MVP is vibes-based.

## Consequences

- A single security incident exposes the gap publicly; recovery is expensive and reputational.
- Incidents are undetected until users complain; mean-time-to-detection is open-ended.
- Costs spike silently — LLM budgets, cloud bills, storage — because nothing enforces ceilings.
- The system becomes unreplaceable because it accumulates users and data while the code decays.
- Every new engineer who touches it inherits the implicit "we'll fix this eventually" contract.

## How to fix

- Name the stage in the README. If the system is deployed to real users with real data, it's not a prototype anymore; it's an under-resourced MVP.
- Schedule graduation explicitly: block a sprint (or more) on landing the MVP baselines from [[stage-mvp]] — auth, secrets manager, structured logging, error tracking, health checks.
- Make graduation non-negotiable for any further feature work. An error-budget-style policy works here: no new features until the graduation baseline is met.
- If graduation is genuinely not worth the cost (the system shouldn't survive), retire it — don't leave a degraded prototype in production.
- Use [[pattern-strangler-fig]] if a clean replacement is more tractable than hardening the original.

## See also

- [[stage-prototype]] — the stage this antipattern ages out of.
- [[stage-mvp]] — the baselines that mark the graduation.
- [[principle-deploy-small-and-often]] — prototype-drift thrives in infrequent-deploy systems.
- [[antipattern-silent-failure]] — a frequent travelling companion of prototype-drift.
