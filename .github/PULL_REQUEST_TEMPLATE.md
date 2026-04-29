<!--
Thanks for contributing to Carta. Please read CONTRIBUTING.md if you haven't already.
Keep PRs to a single concern. CI will run validate.py, lint.py, and an INDEX.yaml freshness check.
-->

## What this changes

<!-- One paragraph: what the change is and why. -->

## Type of change

- [ ] Correction (typo, broken link, source fix, formatting)
- [ ] New foundation node (pattern / principle / antipattern / decision-tree)
- [ ] Schema, tooling, or structural change
- [ ] Docs (README, CHARTER, meta)

## Checklist

- [ ] PR addresses a single concern.
- [ ] `python tools/validate.py` passes locally.
- [ ] `python tools/lint.py` passes locally.
- [ ] `python tools/build_index.py --check` passes (INDEX.yaml is fresh).
- [ ] All new claims cite sources. Currency notes added for sources older than five years where applicable.
- [ ] No forward references (any `[[wikilink]]` resolves to an existing node).
- [ ] If overriding a foundation node at a more specific level, an ADR explains why.
- [ ] For new foundation nodes: an issue was opened first and the node was confirmed in scope.

## Linked issues

<!-- Closes #N, refs #M, etc. -->
