# Contributing to Carta

Carta is a curated knowledge base. Contribution discipline is the product, not an obstacle to it. This document explains what we accept, how to propose changes, and what passing CI actually means.

## What kind of contribution

We accept three categories of change, in increasing order of effort to review.

### 1. Corrections — easy lane

Typos, broken links, source URL fixes, formatting issues, dead anchor links.

- Open a PR directly. No issue needed.
- One concern per PR. A typo fix and a content rewrite should not share a branch.

### 2. New foundation nodes — high bar

A new pattern, principle, antipattern, or decision-tree under `foundations/`.

The foundation layer is the shared starter set used by every fork. Additions raise the bar for everyone, so they need to clear it.

- **Open an issue first** using the "Propose a new foundation node" template. Wait for confirmation that the node is in scope before drafting.
- Each new node must:
  - Cite **at least one canonical source** (book, peer-reviewed paper with DOI, or article by a recognised authority on the topic). See [`foundations/40-standards/`](foundations/40-standards/) for the writing rules.
  - Include a "When NOT to use" section. Patterns without trade-offs are inadmissible.
  - Pass `python tools/validate.py` and `python tools/lint.py` locally before the PR opens.
  - Use the templates in [`templates/`](templates/) — they encode the schema.

If you are unsure whether a node belongs at foundation level or organisation level, propose at organisation level. The foundation is intentionally narrow.

### 3. Schema, tooling, and structural changes — discuss first

Changes to the four-level model, the foundation layer taxonomy, the validator/lint rules, the build pipeline, or the slash commands.

- Open an issue describing the change and the motivating problem. Do not open a PR before alignment.
- These changes ripple through every fork downstream. Reviews are slower and we will push back if the cost-benefit isn't clear.

## What does **not** belong upstream

Carta is designed to be forked. Most of what you'd want to add belongs in *your* fork, not upstream:

- Organisation-, team-, and project-level content (`org/`, `teams/`, `projects/`) — these layers exist precisely so each fork owns them. Do not PR organisation overrides upstream.
- Tech-stack ADRs — these live at organisation level by design (see CHARTER.md).
- Patterns specific to one company's tooling, vendors, or vocabulary.

If your change describes how *your* team does something, it almost certainly belongs in your fork's `org/` or `teams/` layer.

## How to author a node

The recommended path is the `/carta-add` slash command, which loads the writing rules, drafts a terse node from a chosen template, and runs the validator. You then review and edit.

If you prefer to write by hand: copy the matching template from [`templates/`](templates/), fill it in, and run the validators before opening the PR.

```bash
python tools/validate.py    # structural validation — must pass
python tools/lint.py        # graph health — must pass
python tools/build_index.py # regenerates INDEX.yaml
```

The pre-commit hook regenerates `INDEX.yaml` automatically on commit if you've installed it (`tools/hooks/install.sh`). If you haven't, regenerate it manually before pushing — CI will fail otherwise.

## Pull request checklist

The PR template encodes this; included here for reference.

- [ ] Single concern per PR.
- [ ] `python tools/validate.py` passes.
- [ ] `python tools/lint.py` passes.
- [ ] `python tools/build_index.py --check` passes (i.e. INDEX.yaml is fresh).
- [ ] All new claims cite sources. Currency notes added for sources older than five years.
- [ ] No forward references (a node cannot cite a node that doesn't exist yet).
- [ ] If overriding a foundation node at a more specific level, an ADR explains why.

## Review process

- One maintainer review for corrections; two for new foundation nodes.
- Reviews focus on: source admissibility, accuracy, fit with the rest of the graph, and prose clarity.
- We may ask you to split, narrow, or relocate the change. This is normal — keeping the foundation lean is the work.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating you agree to its terms.

## Licensing

By submitting a PR you agree that your contribution is licensed under the MIT licence — the same as the rest of the repository ([LICENSE](LICENSE)).
