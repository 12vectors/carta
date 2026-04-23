---
id: stage-prototype
title: Prototype
type: stage
maturity: stable
tags: [stage, stable, prototype, spike]
next_stage: "[[stage-mvp]]"
typical_antipatterns:
  - "[[antipattern-prototype-drift]]"
related:
  - "[[stage-mvp]]"
sources:
  - "Extreme Programming Explained, 2nd ed (Beck & Andres, Addison-Wesley, 2004) — 'Spike Solution'"
  - "The Pragmatic Programmer (Hunt & Thomas, Addison-Wesley, 1999) — 'Tracer Bullets'"
---

## Description

A prototype explores feasibility. The audience is the team building it — a single developer, or a small working group — and the system runs on someone's laptop or a shared dev box. No external users. No revenue. The implicit assumption is that the code will either be rewritten, thrown away, or hardened substantially before reaching anyone else. The goal is to learn: does the idea work, does the API shape make sense, does the model choice hold up, is the integration tractable?

## What relaxes

- **Authentication and authorisation** — localhost or VPN is enough; no OAuth, no SSO.
- **Secrets management** — environment variables or a `.env` file (gitignored) are acceptable.
- **Observability** — console logs, not structured logging; no tracing, no metrics beyond "did it crash?".
- **High availability** — single instance, crash-and-restart is the recovery plan.
- **Deployment automation** — a README with `uvicorn app:main` is the deploy story.
- **Test coverage** — happy-path test for the core loop; full coverage is premature.
- **Schema stability** — breaking changes ship without migration; drop the data and reseed.

## What stays baseline

- **Real customer data stays out.** If it's personal, payment, health, or production-scoped, it doesn't enter the prototype.
- **Secrets never commit.** `.env` in `.gitignore`, even in prototypes. Once leaked, always leaked.
- **Code structure stays readable.** Prototypes become MVPs more often than they get thrown away; future-you has to read this.
- **External calls are bounded.** Paid APIs (LLMs, third-party) behind a cap — even a dumb per-run token ceiling — so a runaway loop doesn't burn through the company card.
- **The "prototype" label is explicit.** Calling something a prototype while deploying it to customers is how hardened-through-neglect systems are born.

## Graduating

Moving to [[stage-mvp]] requires tightening:

- Add authentication (even a single shared-secret header).
- Move secrets out of files and into env-at-runtime or a lightweight manager.
- Introduce structured logging on the main request path and on external calls.
- Add a health endpoint with real dependency checks.
- Stand up CI on the main branch.
- Write a minimal test suite for critical paths.
- Make schema changes backward-compatible or ship a migration script.

## Typical antipatterns

- **Prototype drift** — the prototype becomes the production system through accretion. No one ever schedules hardening; features land faster than the stage catches up.
- **Fake-prototype security** — "It's just a prototype" used to justify skipping auth on a system that has customer data.

## See also

- [[stage-mvp]] — the next stage on the ladder.
- [[pattern-feature-flag]] — even prototypes benefit; flags keep the risky new code out of the demo.
- [[antipattern-silent-failure]] — `except: pass` is seductive in prototypes; it costs more later than it saves now.
