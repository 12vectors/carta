---
id: antipattern-snapshot-overreliance
title: Snapshot Overreliance
type: antipattern
category: testing
maturity: stable
tags: [antipattern, stable, testing, frontend]
applies_to:
  - "[[context-web-application]]"
mitigated_by:
  - "[[pattern-test-pyramid]]"
related: []
sources:
  - "Effective Snapshot Testing (Kent C. Dodds, 2017): https://kentcdodds.com/blog/effective-snapshot-testing"
  - "Jest Snapshot Testing: https://jestjs.io/docs/snapshot-testing"
---

## How to recognise

- Tests are mostly `expect(x).toMatchSnapshot()` with thin or no other assertions.
- Snapshot updates are routine; reviewers rubber-stamp the diff.
- Snapshot files run hundreds of lines per component.
- Failures prompt "just update the snapshot" rather than diagnosis.
- Snapshots capture rendered HTML down to whitespace and class names.

## Why it happens

- Snapshots feel like free coverage — one line, huge captured output.
- Component-library churn (styles, hashed class names) produces constant diffs.
- No explicit acceptance criterion exists, so the snapshot *becomes* the spec.
- Reviewers lack time to read long snapshot diffs carefully.

## Consequences

- Signal lost — everyone updates without reading, missing real regressions.
- Cosmetic refactors turn the suite red for behaviour-preserving changes.
- Coverage metrics overstate confidence.
- Real bugs hide in snapshot-diff noise.

## How to fix

- Restrict snapshots to stable, user-visible output (serialised API responses, not rendered HTML).
- Pair every snapshot with at least one behavioural assertion stating intent.
- Prefer inline snapshots — the expected value sits in the test file where reviewers read it.
- Delete any snapshot nobody can explain; replace with an explicit assertion if still needed.
- For UI, use role- and text-based queries (Testing Library) with explicit expectations.

## See also

- [[pattern-test-pyramid]] — snapshot overuse concentrates at the top; rebalance.
