---
id: antipattern-snowflake-ci
title: Snowflake CI
type: antipattern
category: delivery
maturity: stable
tags: [antipattern, stable, delivery, ci]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-internal-tool]]"
mitigated_by:
  - "[[pattern-deployment-pipeline]]"
  - "[[pattern-build-once-deploy-many]]"
related:
  - "[[pattern-fast-feedback-pipeline]]"
sources:
  - "Continuous Delivery (Humble & Farley, Addison-Wesley 2010) ch. 11 — 'Principles of Infrastructure Management'"
  - "Continuous Integration (Martin Fowler, 2024 rev): https://martinfowler.com/articles/continuousIntegration.html"
---

## How to recognise

- Every service has a bespoke CI config nobody else understands.
- Onboarding a new repo requires a one-off meeting with the CI-whisperer.
- Pipeline behaviour depends on which host runs it (a runner "knows things").
- Rebuilding a runner from scratch is a multi-day project nobody wants.
- Debugging a failure means SSH to the build host.

## Why it happens

- CI configs evolved organically, never factored into shared templates.
- Runners were configured by hand, drift accumulated, nobody wrote it down.
- Secrets, caches, or global state lives on the runner rather than in the pipeline.
- Team lacks a platform engineer to own CI as a product.

## Consequences

- New services pick CI by cargo-cult — one misconfigured repo copies everywhere.
- Upgrade or migration is impossible without breaking something.
- Flaky builds blamed on "the runner" — genuine bugs hide.
- Supply-chain audits fail — nobody can attest what the artefact was built with.

## How to fix

- Move CI to ephemeral containers — each job runs on a clean base image.
- Factor shared CI into reusable workflows, actions, or templates.
- Encode the runner image in source; rebuild it in CI like any other artefact.
- Forbid SSH to runners — if you need that, you need better logs.
- Apply [[pattern-build-once-deploy-many]] so build reproducibility is a property of the artefact, not the runner.

## See also

- [[pattern-deployment-pipeline]] — the replacement structure.
- [[pattern-build-once-deploy-many]] — partner pattern for reproducibility.
