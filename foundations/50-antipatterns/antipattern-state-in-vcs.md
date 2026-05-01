---
id: antipattern-state-in-vcs
title: State in VCS
type: antipattern
category: security
maturity: experimental
tags: [antipattern, experimental, iac, state, vcs, git, secrets]
applies_to:
  - "[[context-infrastructure-as-code]]"
mitigated_by:
  - "[[pattern-state-isolation]]"
  - "[[pattern-secrets-management]]"
sources:
  - "HashiCorp — Terraform Backend Configuration: 'Don't commit state to source control' — https://developer.hashicorp.com/terraform/language/backend"
  - "Terraform: Up & Running (Brikman, O'Reilly, 2022 3rd ed.) ch. 3 'How to Manage Terraform State' — https://www.oreilly.com/library/view/terraform-up/9781098116736/"
  - "OWASP Secrets Management Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"
  - "GitHub — Removing sensitive data from a repository — https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository"
---

## How to recognise

- `terraform.tfstate` or `*.tfstate.backup` files committed to the repo, or present in the working tree without a `.gitignore` entry.
- Ad-hoc state files attached to issues, pull requests, chat threads, or shared drives.
- Git history showing a previously-committed state file even if it has since been removed.
- "Just check the state file in lib/" or "the state is in main" referenced in onboarding docs.
- State files attached to Terraform plan artefacts persisted in publicly-readable CI artefact stores.

## Why it happens

- Bootstrapping shortcut: the team starts with a local backend during exploration and never migrates.
- Onboarding friction: setting up a remote backend feels heavyweight for a first-day developer.
- Auditing pressure: a request to "send me the current state" gets answered with the file rather than read access to the backend.
- Tooling gap: CI uploads `plan.out` and `state` together as a single artefact for convenience.
- Misunderstanding: the team treats state as data they own and can share, not as a credential.

## Consequences

- Sensitive outputs (DB passwords, API keys, generated tokens) leak to anyone with repo read access.
- Resource IDs and topology are exposed to attackers planning lateral movement.
- Concurrent edits via VCS produce silent state corruption — no locking primitive exists in Git.
- Forks, mirrors, and stale clones retain the secret material indefinitely; rotation alone is insufficient remediation.
- Compliance posture (SOC2, PCI, HIPAA) is breached the moment a state file lands in a multi-reader VCS.

## How to fix

- Adopt `[[pattern-state-isolation]]`: provision a remote backend per stack with scoped IAM and encryption.
- `.gitignore` `*.tfstate`, `*.tfstate.backup`, and `.terraform/` immediately, then audit Git history for prior commits.
- Rotate every credential that appeared in a previously-committed state file — assume disclosure.
- Purge from history (`git filter-repo`, BFG) and force-rotate any deploy keys, CI tokens, or webhook secrets the repo could have authorised.
- Configure CI artefact stores with access control; if `plan.out` is shared, scrub state-derived outputs first.
- Document the remote-backend bootstrap path so the next contributor doesn't reinvent the local-backend shortcut.

## Stage-specific notes

- **At [[stage-prototype]]**: a local state file is acceptable, but never committed; `.gitignore` from day one.
- **At [[stage-mvp]] and beyond**: remote backend required; local state files are a regression.
- **At [[stage-critical]]**: VCS scanning (gitleaks, GitHub secret scanning) blocks merges that introduce committed state files.

## See also

- [[pattern-state-isolation]] — the primary mitigation; per-stack remote backends with scoped IAM.
- [[pattern-secrets-management]] — sensitive outputs in state are credentials and need vault-grade handling.
- [[antipattern-prototype-drift]] — committed state often co-occurs with broader prototype-stage debt.
