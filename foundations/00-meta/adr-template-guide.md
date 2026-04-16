# ADR Template

Use this template when recording an Architecture Decision Record in `decisions/` (organisation level) or `projects/<name>/decisions/` (project level).

**Filename:** `adr-NNNN-slug.md` where NNNN is the next available zero-padded sequence number and slug is a short kebab-case description of the decision.

---

```markdown
---
id: adr-NNNN-slug
title: <Short title of the decision>
type: adr
maturity: stable
tags: [adr, <additional tags>]
status: proposed              # proposed | accepted | superseded | rejected
date: YYYY-MM-DD
supersedes: ""                # "[[adr-NNNN-old]]" if this replaces a prior ADR, omit otherwise
superseded_by: ""             # filled in later if this ADR is itself superseded, omit otherwise
affects:                      # nodes whose frontmatter or guidance changes as a result
  - "[[pattern-example]]"
related: []
sources: []
---

## Context

What situation or forces prompted this decision? What problem needed solving?
State the facts, constraints, and requirements — not the conclusion.

## Decision

What was decided. Be specific: name the pattern chosen, the trade-off accepted,
the constraint imposed.

## Consequences

What follows from this decision — both positive and negative.

- **Positive:** what improves or becomes possible.
- **Negative:** what gets harder, what's ruled out, what new constraints exist.
- **Neutral:** side effects that are neither good nor bad but worth noting.

## Alternatives considered

What other options were evaluated and why they were rejected.
For each alternative, state the option and the reason it was not chosen.
This section helps future readers understand the decision space,
not just the outcome.
```

---

## Guidance

- **Status lifecycle:** ADRs start as `proposed`. After review and merge, they move to `accepted`. If a later ADR replaces this one, it moves to `superseded` and gains a `superseded_by` link. Rejected proposals stay as `rejected` for the record.

- **The `affects` field is critical.** It drives the ingest operation. When an ADR is merged, an agent reads `affects` to determine which nodes need their frontmatter updated (e.g. adding `contradicted_by` links, adjusting maturity). An ADR with an empty `affects` field either doesn't change anything (and may not need to be an ADR) or has an incomplete analysis.

- **Keep the Context section factual.** Describe the situation, not the solution. A reader should understand why a decision was needed before learning what was decided.

- **Consequences are honest.** Every decision has costs. An ADR that lists only positive consequences is incomplete. Name what gets harder.

- **One decision per ADR.** If a situation requires multiple decisions, write multiple ADRs and link them via `related`.
