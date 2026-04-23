# Node Schema

The frontmatter contract for every node in Carta. The frontmatter **is the graph** — agents traverse it without parsing prose, and Obsidian renders it as a navigable knowledge graph.

This document is normative. `tools/validate.py` enforces the rules below. Broken frontmatter fails CI.

**Before authoring**, read [`writing-rules.md`](writing-rules.md) for voice, length, and bullet-structure rules. The schema here defines *what* a node contains; the writing rules define *how much* and *in what voice*.

---

## Frontmatter fields

### Universal fields

These fields apply to every node type.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `id` | yes | string | Globally unique identifier. Must match the filename without `.md`. Prefixed by node type: `pattern-`, `context-`, `solution-`, `standard-`, `antipattern-`, `adr-`, `pillar-`, `principle-`, `dtree-`, `stage-`. |
| `title` | yes | string | Human-readable name. |
| `type` | yes | enum | One of: `pattern`, `antipattern`, `standard`, `solution`, `context`, `adr`, `pillar`, `principle`, `decision-tree`, `stage`. |
| `maturity` | yes | enum | One of: `experimental`, `stable`, `deprecated`. |
| `tags` | yes | list[string] | Must include the `type` value and the `maturity` value. Additional tags are encouraged for filtering. |
| `related` | no | list[wikilink] | Links to nodes that are relevant but not prerequisite or conflicting. |
| `pillars` | no | list[wikilink] | Well-Architected–style quality lenses this node serves. Wikilinks to `pillar` nodes in `foundations/05-pillars/` (e.g. `[[pillar-reliability]]`). Applies to `pattern`, `antipattern`, `solution`. |
| `sources` | see below | list[string] | Evidence grounding this node. Required for `pattern`, `antipattern`, `solution`. See **Provenance rules**. |

### Type-specific fields

#### pattern

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `category` | yes | string | Maps to the pattern's location under `foundations/20-patterns/`. Values: `style` (for `styles/<file>`), a tactic concern (for `tactics/<concern>/<file>`: `communication`, `data`, `resilience`, `scaling`, `security`, `agentic`, `observability`, `refactoring`, `deployment`), or `integration` (for `integration/<file>`). |
| `stage_floor` | no | enum | Minimum operational stage at which this pattern becomes recommended. One of `prototype`, `mvp`, `production`, `critical`. If absent, the pattern applies at every stage (defaults to `prototype`). Patterns whose `stage_floor` exceeds the task's declared stage are demoted to "defer to stage X" in the traversal report — they stay in view as "plan for later", not as current blockers. |
| `applies_to` | yes | list[wikilink] | Contexts where this pattern is relevant. At least one required. |
| `prerequisites` | no | list[wikilink] | Patterns that must be in place before this one can be applied. |
| `conflicts_with` | no | list[wikilink] | Patterns that cannot coexist with this one in the same system. |
| `contradicted_by` | no | list[wikilink] | Nodes whose claims conflict with this one. See **Contradictions**. |

#### antipattern

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `category` | yes | string | Same category values as patterns. |
| `applies_to` | yes | list[wikilink] | Contexts where this antipattern commonly appears. |
| `mitigated_by` | no | list[wikilink] | Patterns that address or prevent this antipattern. |

#### standard

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `category` | yes | string | Domain the standard covers (e.g. `api`, `testing`, `naming`, `security`). |
| `applies_to` | no | list[wikilink] | Contexts where this standard applies. Omit if it applies universally. |
| `enforceability` | yes | enum | One of: `automated` (CI can check it), `review` (requires human review), `advisory` (recommended but not enforced). |

#### solution

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `composes` | yes | list[wikilink] | The patterns this solution combines. Order reflects the recommended implementation sequence. |
| `applies_to` | yes | list[wikilink] | Contexts where this solution is relevant. |
| `prerequisites` | no | list[wikilink] | Patterns or solutions that must already be in place. |

#### context

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `signals` | yes | list[string] | Observable properties that indicate this context applies. Mirrors the signal table in `DECISION_TREE.md`. |
| `recommended_patterns` | yes | list[wikilink] | Patterns commonly needed in this context. The traversal uses these as the starting candidate set. |
| `recommended_standards` | no | list[wikilink] | Standards that typically apply in this context. |
| `common_antipatterns` | no | list[wikilink] | Antipatterns that frequently appear in this context. |

#### adr

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `status` | yes | enum | One of: `proposed`, `accepted`, `superseded`, `rejected`. |
| `date` | yes | string | ISO 8601 date (YYYY-MM-DD) when the decision was made or proposed. |
| `supersedes` | no | wikilink | The ADR this one replaces, if any. |
| `superseded_by` | no | wikilink | The ADR that replaced this one, if any. |
| `affects` | yes | list[wikilink] | Nodes whose frontmatter or guidance changed as a result of this decision. |

#### pillar

Pillars live in `foundations/05-pillars/`. They encode the quality lenses (Reliability, Security, Cost, Operational Excellence, Performance) every system is evaluated against.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `realised_by` | no | list[wikilink] | Principles that realise this pillar. |
| `tradeoffs_with` | no | list[wikilink] | Pillars that typically pull in the opposite direction. |

#### principle

Principles live in `foundations/15-principles/`. They are cross-cutting design heuristics — pre-pattern guidance that shapes decisions.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `pillar` | yes | wikilink | The pillar this principle primarily realises. |
| `related_patterns` | no | list[wikilink] | Patterns that embody this principle. |
| `related_antipatterns` | no | list[wikilink] | Antipatterns that violate this principle. |

#### decision-tree

Decision trees live in `foundations/25-decision-trees/`. They are selection guides that help an agent or engineer choose between options along defined criteria.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `decides_between` | yes | list[wikilink] | The options being selected among — typically pattern nodes. |
| `criteria` | yes | list[string] | The axes against which the options are compared. |
| `related_patterns` | no | list[wikilink] | Upstream patterns that this decision tree elaborates. |

#### stage

Stages live in `foundations/12-stages/`. They encode operational ambition — what the system is aiming to be *right now*. The four stages (`prototype`, `mvp`, `production`, `critical`) combine with a context during traversal to determine which patterns are currently required vs. deferred.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `next_stage` | no | wikilink | The stage that comes after this one in the usual progression. `stage-critical` has none. |
| `typical_antipatterns` | no | list[wikilink] | Failure modes specific to operating at this stage (e.g. "production at MVP cost"). |

---

## Wikilink format

Link fields (`applies_to`, `prerequisites`, `related`, `conflicts_with`, `contradicted_by`, `composes`, `mitigated_by`, `recommended_patterns`, `affects`, etc.) use Obsidian wikilinks:

```yaml
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
```

The `[[ ]]` wrappers allow Obsidian's graph view and backlinks panel to index the relationship automatically. Agents strip the wrappers when resolving IDs programmatically. The inner text must exactly match the target node's `id` field.

---

## Body sections by type

The body (everything after the frontmatter) follows a type-specific structure. Sections are H2 headings. Required sections are marked.

### pattern

| Section | Required | Purpose |
|---------|----------|---------|
| `## When to use` | yes | Symptoms or triggers an agent can match against. Concrete and specific. |
| `## When NOT to use` | yes | Counter-indications. At least one case required. |
| `## Decision inputs` | yes | Questions the agent must answer before choosing this pattern. |
| `## Solution sketch` | yes | Minimal description of the approach. May include a reference implementation pointer. |
| `## Trade-offs` | yes | Gain/cost table. |
| `## Implementation checklist` | no | Concrete, verifiable steps. |
| `## Contradictions` | no | Only present when `contradicted_by` is non-empty. Uses `> [!contradiction]` callout. |
| `## See also` | no | Links to related nodes with a reason for each link. |

### antipattern

| Section | Required | Purpose |
|---------|----------|---------|
| `## How to recognise` | yes | Observable symptoms that this antipattern is present. |
| `## Why it happens` | yes | Root causes and conditions that lead to this antipattern. |
| `## Consequences` | yes | What goes wrong if left unaddressed. |
| `## How to fix` | yes | Remediation steps, linking to patterns that address the problem. |
| `## See also` | no | Related nodes. |

### standard

| Section | Required | Purpose |
|---------|----------|---------|
| `## Requirement` | yes | What the standard requires, stated unambiguously. |
| `## Rationale` | yes | Why this standard exists. |
| `## Compliance` | yes | What compliance looks like — how to verify it. |
| `## Non-compliance` | yes | What failure to comply looks like and what the remediation is. |
| `## See also` | no | Related nodes. |

### solution

| Section | Required | Purpose |
|---------|----------|---------|
| `## Problem` | yes | The problem this solution addresses. |
| `## Composition` | yes | How the constituent patterns fit together. Order, data flow, integration points. |
| `## Decision inputs` | yes | Questions to answer before applying this solution. |
| `## Trade-offs` | yes | Gain/cost table for the composition as a whole. |
| `## Implementation sequence` | yes | Ordered steps referencing the composed patterns. |
| `## See also` | no | Related nodes. |

### context

| Section | Required | Purpose |
|---------|----------|---------|
| `## Description` | yes | What kind of system this context describes. |
| `## Key concerns` | yes | The architectural concerns that dominate in this context (e.g. latency, consistency, security). |
| `## Typical architecture` | no | Common high-level shapes systems in this context take. |
| `## See also` | no | Related contexts and cross-references. |

### adr

| Section | Required | Purpose |
|---------|----------|---------|
| `## Context` | yes | The situation and forces at play. |
| `## Decision` | yes | What was decided. |
| `## Consequences` | yes | What follows from the decision — both positive and negative. |
| `## Alternatives considered` | no | Other options and why they were rejected. |

### pillar

| Section | Required | Purpose |
|---------|----------|---------|
| `## Description` | yes | What this quality lens optimises for. |
| `## When this dominates` | no | Conditions under which this pillar outweighs the others. |
| `## Trade-offs` | yes | What gets sacrificed to maximise this pillar — usually references to other pillars. |
| `## Realised by` | no | Bulleted links to principles and patterns that serve this pillar. |

### principle

| Section | Required | Purpose |
|---------|----------|---------|
| `## Statement` | yes | A short, directive sentence capturing the principle. |
| `## Rationale` | yes | Why this principle matters and which pillar it realises. |
| `## How to apply` | yes | What applying this principle looks like in practice. |
| `## Related patterns` | no | Patterns that embody the principle. |

### decision-tree

| Section | Required | Purpose |
|---------|----------|---------|
| `## Problem` | yes | The choice this tree helps make. |
| `## Criteria` | yes | Axes along which the options are compared. |
| `## Recommendation` | yes | A table, list, or flowchart mapping criteria outcomes to options. |
| `## Fallback` | no | What to do when criteria are ambiguous. |

### stage

| Section | Required | Purpose |
|---------|----------|---------|
| `## Description` | yes | What this operational stage is — who's using the system, what failure modes are acceptable. |
| `## What relaxes` | yes | Concerns that can legitimately drop at this stage (auth? monitoring? HA?). |
| `## What stays baseline` | yes | Things that cannot be relaxed even here — the floor below which the system is not fit for purpose. |
| `## Graduating` | no | What must tighten to reach the next stage. Omit on `stage-critical` (no next stage). |
| `## Typical antipatterns` | no | Failure modes specific to operating at this stage (e.g. "prototype drift" — code never leaves prototype, never hardens). |

---

## Provenance rules

The `sources` field grounds nodes in evidence. The following rules apply:

1. **Required for**: `pattern`, `antipattern`, `solution`. Optional for `standard`, `context`, `adr`.
2. **Minimum**: at least one source per node where required.
3. **Verifiable**: every source must be checkable by someone outside the contributor's context. Acceptable forms:
   - Book: author, title, year, and optionally chapter. E.g. `"Release It! (Nygard, 2018) ch. 5"`
   - Paper: title, authors, year, DOI or stable URL.
   - Blog post: author, title, URL. E.g. `"https://martinfowler.com/bliki/CircuitBreaker.html"`
   - Incident report: public post-mortem with URL or reference.
   - Codebase: named project with URL. E.g. `"Netflix Hystrix — https://github.com/Netflix/Hystrix"`
4. **Not acceptable**: "industry practice", "team discussion", anonymous references, undated URLs without attribution.
5. **Currency**: sources older than five years require an explicit note in the node confirming continued relevance. See the Currency admission criterion in `CHARTER.md`.

Nodes with empty or missing `sources` where required are flagged by `tools/validate.py` and `tools/lint.py`.

---

## Contradictions

When a node's claims conflict with another node:

1. Both nodes add the other to their `contradicted_by` field.
2. Both nodes gain a `## Contradictions` section with a `> [!contradiction]` callout describing the conflict.
3. Contradiction links are always bidirectional.

Contradictions are not errors — they are navigable features of the graph. See `CHARTER.md` for the resolution process.

---

## Filename conventions

- Filenames are globally unique across the vault.
- Foundation files match the node's `id` field with a `.md` extension. Foundation files have no level suffix.
- Files outside foundations use a level suffix for Obsidian uniqueness: `.org.md` for organisation-level files, `.<team>.md` for team-level files (e.g. `.platform.md`), `.<project>.md` for project-level files (e.g. `.payments-api.md`). This applies to all files outside foundations, not just overrides.
- Type prefix is part of the filename: `pattern-circuit-breaker.md` (foundation), `pattern-rest-api.org.md` (org override), `pattern-rest-api.platform.md` (team override).
- ADR filenames use a zero-padded sequence number: `adr-NNNN-slug.md` (foundation-level standards only). At other levels, include the level suffix: `adr-0001-postgres-over-mongodb.org.md`.
- Any override must be accompanied by a decision record at the same level.

---

## Validation

`tools/validate.py` checks:

- All required frontmatter fields are present and correctly typed.
- `id` matches the filename.
- `type` is a valid enum value.
- `maturity` is a valid enum value.
- `tags` includes the `type` and `maturity` values.
- All wikilink targets resolve to existing files (or are declared as known external references).
- Required body sections are present for the node's type.
- `sources` is non-empty where required.
- `contradicted_by` links are bidirectional.

`tools/lint.py` goes further with semantic checks — see `operations.md`.
