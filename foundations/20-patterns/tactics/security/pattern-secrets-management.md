---
id: pattern-secrets-management
title: Secrets Management
type: pattern
category: security
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-security]]"
tags: [pattern, stable, security, secrets, credentials]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related: []
conflicts_with: []
contradicted_by: []
sources:
  - "OWASP Secrets Management Cheat Sheet -- https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"
---

## When to use

- Any service holding API keys, DB credentials, signing keys, TLS certs, or tokens.
- CI/CD pipelines that deploy with credentials.
- Multi-environment setups (dev/stage/prod) needing distinct secrets per env.
- Compliance-driven environments (SOC2, PCI, HIPAA) requiring rotation and audit.
- Machine-to-machine auth where static long-lived keys need replacement.

## When NOT to use

Never skip. Choose mechanism instead:

- Workload identity (IRSA, GCP WI, Azure MI) over static keys wherever the platform supports it.
- Local dev: `.env` excluded from git is acceptable if paired with a bootstrap from the vault.
- Truly public config (feature flags, public URLs) — not a secret, do not store in the vault.

## Decision inputs

- Secret types: static API keys, dynamic DB creds, certs, signing keys, SSH, session cookies.
- Rotation cadence and whether rotation is automatic or ticket-driven.
- Audience: humans, CI, runtime workloads — each needs a different retrieval path.
- Platform capability: KMS, Vault, AWS Secrets Manager, GCP Secret Manager, sealed-secrets.
- Blast-radius budget: how quickly must a leaked secret be revoked?
- Compliance mandates for audit, MFA, and separation of duties.

## Solution sketch

One source of truth, fetched at runtime, never baked into code or images.

```
[Vault / Secrets Manager]
       │
       ├── CI: OIDC-exchanged short-lived token, not a static key
       ├── Workload: pod identity / IRSA / WI fetches on boot + on rotation
       └── Human: SSO + MFA + just-in-time grant, audit logged
```

- Prefer **dynamic secrets** (short-lived DB creds) over static; eliminate rotation entirely when possible.
- Prefer **workload identity** over any stored credential for cloud APIs.
- Encrypt at rest (KMS-backed) and in transit (TLS to the vault).
- Inject via file or env at process start; refresh on rotation without redeploy.
- Never log secrets; scrub error handlers and crash reports.

See OWASP Secrets Management Cheat Sheet for the canonical checklist.

## Trade-offs

| Gain | Cost |
|------|------|
| Central revocation and audit of every secret | Vault itself is a critical dependency and SPOF |
| Rotation without redeploy — dynamic creds eliminate rotation pain | Clients must handle credential refresh mid-process |
| Removes secrets from git, images, and env files | Local dev and emergency break-glass flows need explicit design |
| Fine-grained access per workload | Workload identity requires platform support and setup effort |
| Enables compliance (SOC2, PCI) | Poor access policies recreate the problem inside the vault |

## Implementation checklist

- [ ] Ban committed secrets; enforce with pre-commit hooks and repo scanning (gitleaks, trufflehog).
- [ ] Store every secret in a central vault; remove env-file secrets from images and artefacts.
- [ ] Use workload identity for cloud-provider APIs; avoid long-lived access keys.
- [ ] Use dynamic DB credentials where the vault supports it.
- [ ] Rotate static secrets on a schedule; rotate immediately on suspected compromise.
- [ ] Inject secrets at process start via file or env; support live reload on rotation.
- [ ] Scrub secrets from logs, traces, error reporters, and crash dumps.
- [ ] Restrict vault access per workload/role; log every read.
- [ ] Document break-glass procedure (who, how, audited).
- [ ] Periodic audit: find unused secrets, overbroad policies, stale accounts.

## See also

- [[pattern-oauth2-authorization]] — client secrets and signing keys belong in the vault.
- [[pattern-federated-identity]] — reduces the number of secrets by federating auth.
