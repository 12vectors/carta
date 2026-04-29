# Security policy

## Reporting a vulnerability

Carta is mostly markdown, but the repo ships a small Python toolchain (`tools/`) and pre-commit / post-merge hooks that execute on contributors' machines. If you find a vulnerability — code execution, hook injection, validator bypass, supply-chain risk, anything that affects users of this repo — please report it privately.

**Preferred channel: GitHub private security advisories.**

Open a private advisory at <https://github.com/12vectors/carta/security/advisories/new>. This routes the report directly to the maintainers without exposing details publicly.

Please do **not** open a public issue for security reports.

## What to include

- A description of the issue and its impact.
- A minimal reproduction (file paths, commands, expected vs actual behaviour).
- Affected versions or commit SHAs if known.
- Any suggested mitigation.

## What to expect

- We will acknowledge the report within **5 working days**.
- We will confirm or dispute the issue within **14 days** of acknowledgement.
- If confirmed, we will work on a fix and coordinate disclosure with you. Public disclosure happens after a patch is available.
- Reporters who follow this policy will be credited in the release notes (unless you prefer to remain anonymous).

## Scope

In scope:

- The Python tools under `tools/` (`build_index.py`, `validate.py`, `lint.py`, `carta_checks.py`).
- The git hooks under `tools/hooks/`.
- The slash command files under `commands/`.
- Build / CI configuration that executes on contributor machines or in this repo.

Out of scope:

- Forks of Carta. Each fork is responsible for its own security posture, including its `org/`, `teams/`, and `projects/` content.
- Content errors in foundation nodes (these are correctness issues — open a regular issue).
- Vulnerabilities in upstream dependencies of `pyyaml` or other transitive packages — please report those upstream.
