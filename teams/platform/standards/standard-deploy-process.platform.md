---
id: standard-deploy-process
title: Deployment Process (Platform Team)
type: standard
category: deployment
maturity: stable
tags: [standard, stable, deployment]
applies_to:
  - "[[context-web-application]]"
enforceability: automated
related: []
sources:
  - "Accelerate (Forsgren et al., 2018) ch. 4"
  - "Continuous Delivery (Humble & Farley, 2010) ch. 10"
---

## Requirement

All production deployments for services owned by the platform team must use blue-green deployment. The previous version must remain running and routable until the new version passes health checks and carries live traffic for a minimum observation period of 10 minutes.

Rollback must be achievable by switching traffic back to the previous version without redeployment.

## Rationale

Blue-green deployment minimises downtime and provides an instant rollback path. For platform services that underpin other teams' work, deployment risk must be as low as possible. A bad deploy to a platform service cascades to every consumer.

The 10-minute observation period catches issues that health checks miss — memory leaks, slow performance degradation, and errors that only appear under real traffic patterns.

## Compliance

- Deployment pipeline includes blue-green switch with automated health check gates.
- Previous version is retained and routable for at least 1 hour after cutover.
- Deployment runbook documents the rollback procedure (traffic switch, not redeployment).
- Deployment metrics (error rate, latency p99, CPU/memory) are automatically compared between old and new versions during the observation period.

## Non-compliance

- Direct in-place deployments (rolling update that destroys the previous version).
- Deployments without health check gates.
- Rollback requiring a full redeployment pipeline run.
- Observation period shorter than 10 minutes.

Remediation: configure the deployment pipeline to use the platform team's blue-green deployment template. Contact platform-infra for setup assistance.

## See also
