# Charter

How Carta's foundations are governed. Organisation, team, and project levels are self-governed; this document applies only to `foundations/` itself.

---

## On this charter

This is a **governance document**, not a knowledge node. It prescribes rules for the foundations; it does not itself claim to meet the admission criteria it describes. The Provenance rule below applies to content nodes in the foundations, not to the charter.

That said, the charter's rules are not invented from scratch. The lineage:

- **ADR format.** Follows Michael Nygard's 2011 post, [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — context, decision, consequences.
- **Admission criteria.** Echo the review norms of IETF RFCs (specificity, decidability, clear rejection reasons) and the provenance standards of academic publishing (verifiable sources, named evidence).
- **Contradictions as first-class.** Draws on the "make implicit disagreements explicit" practice from design-by-argument traditions (Rittel, 1973; Kunz & Rittel's IBIS).
- **Five-year currency threshold.** A convention, not a derived number. Five years is long enough that field practice can shift meaningfully; short enough that cited sources are still verifiable. Adjust as needed.
- **Seven-question reviewer checklist.** An editorial compression of the five admission criteria, not an independent claim.

The charter is itself amendable via ADR (see **Amending this charter** at the end).

## Scope

This charter governs the **foundations** — the reusable patterns, standards, antipatterns, contexts, and solutions that ship as the starter knowledge base. It does not govern organisation, team, or project levels, which are owned by their respective groups and may adopt whatever process they see fit.

The foundations are the part of Carta that claims to be true across organisations and stacks. That claim demands a higher bar for admission and a clear process for change.

## Four-level model

Carta operates across four levels, each more specific than the last:

1. **Foundations** (`foundations/`) — the shared, generic knowledge base. Patterns, contexts, antipatterns, solutions, and meta-standards that apply across organisations and stacks. This is what Carta ships out of the box.

2. **Organisation** (`org/`) — an organisation's overrides, extensions, standards, and decisions.

3. **Team** (`teams/<team-name>/`) — team-specific overrides, extensions, standards, and decisions. A platform team and a product team may have different architectural needs.

4. **Project** (`projects/<project-name>/`) — project-specific overrides, extensions, standards, and decisions. The most specific level, scoped to a single system or service.

Each level can override the one above it. The constraint is not hierarchy but **transparency**: any override must be accompanied by a decision record explaining why. The knowledge base is most useful when you can see not just what was decided, but why — including when a project chose to relax an org standard to ship.

Not every level is required. Many setups will use only foundations + org. Teams and projects are available when needed but add no overhead if unused.

### Override resolution

When looking up a node during traversal:

1. Check `projects/<project>/overrides/<node-id>.<project>.md`
2. If not found, check `teams/<team>/overrides/<node-id>.<team>.md`
3. If not found, check `org/overrides/<node-id>.org.md`
4. If not found, use `foundations/<node-id>.md`

Most specific wins. Standards, decisions, and extensions are additive — all levels accumulate. But any level can relax or override any other level, provided the reasoning is documented in a decision record at the appropriate level.

### Filename suffix convention

To ensure global filename uniqueness across the Obsidian vault, files outside the foundations use a level suffix:

- Organisation: `<node-id>.org.md` — e.g. `pattern-rest-api.org.md`
- Team: `<node-id>.<team-name>.md` — e.g. `pattern-rest-api.platform.md`
- Project: `<node-id>.<project-name>.md` — e.g. `pattern-rest-api.payments-api.md`

Foundation files use no suffix — they are the base. The suffix makes every filename globally unique, so Obsidian wikilinks resolve unambiguously and you can tell at a glance in search results or graph view which level a file belongs to.

## Roles

**Maintainers** steward the foundations. They review contributions, enforce admission criteria, resolve disputes, and decide what enters or leaves the foundations. Maintainers are listed in `MAINTAINERS.md`.

**Contributors** propose changes — new nodes, edits to existing nodes, new ADRs. Anyone can contribute. Contributions are reviewed against the admission criteria below.

**Agents** maintain the graph under human supervision. They may:

- Propose updates to frontmatter links (related, conflicts_with, contradicted_by, prerequisites) when a new node changes the graph topology.
- Propose maturity changes (experimental → stable, stable → deprecated) based on evidence.
- Run lint and report issues.
- Draft new solution nodes when a traversal produces a novel composition (capture operation).
- Propagate the effects of a new ADR across affected nodes (ingest operation).

Agents may **not**:

- Merge their own proposals. Every agent-proposed change requires human review and approval.
- Add new patterns, standards, or antipatterns to the foundations. These require human authorship.
- Remove nodes. Deprecation and removal are human decisions.
- Resolve contradictions. Agents flag contradictions; humans resolve them via ADR.

The boundary is: agents handle structure and bookkeeping; humans handle judgement and knowledge.

## Admission criteria

The Carta foundations are a **minimal, high-trust reference**. Few patterns enter; those that do are durable, well-grounded, and reusable across organisations. Most working knowledge lives in organisation, team, and project levels — that's by design. The foundations' value is its quality, not its size.

Five criteria determine what enters. They divide into two groups: **form** criteria, about how a node is written, and **fit** criteria, about how a node relates to the world and to the existing graph. Every node must satisfy all five.

A separate section below addresses standards, which sit in the foundations only as templates and meta-guidance, not as opinionated content.

### Form criteria

These criteria assess the node on its own terms. They can be checked without looking at anything else in the wiki.

#### 1. Decidability

A node must give an agent enough information to make a defensible yes-or-no decision about whether to apply it to a given task. Patterns must have concrete `When to use` and `When NOT to use` sections. Standards must state what they require unambiguously. Anti-patterns must describe the conditions under which the failure mode appears. Vague, aspirational, or purely philosophical content is not admitted.

The implicit corollary: a pattern that's true but trivial — guidance that any practitioner would follow by default — fails decidability not because it's undecidable but because the decision is empty. "Use HTTPS for inter-service communication" passes the formal test and fails the spirit. Reviewers should reject patterns that codify universal practice unless the codification itself adds value (compliance checkbox, onboarding aid).

**Test:** could an agent reading this node make a defensible yes-or-no decision about whether to apply it? And: would that decision be non-obvious to someone with relevant experience? If either answer is no, the node isn't ready.

#### 2. Provenance

Every pattern must cite at least one source in its `sources` field. Sources must be **verifiable** — a book with an author and year, a paper with a DOI or stable URL, a blog post with an author, a public incident report, a named codebase, or a documented conversation with attribution. Anonymous claims, undocumented "team discussions," and vague references like "industry practice" do not count.

The source doesn't need to be academic; it needs to be checkable by someone outside the contributor's immediate context. Provenance protects against opinion masquerading as established practice.

**Test:** if someone asked "says who?", could you point them somewhere a stranger could verify? If not, the node isn't ready for the foundations. It may still be valid — capture it in an organisation, team, or project level and promote it when evidence accumulates.

### Fit criteria

These criteria assess the node in relation to its context — the broader landscape of architecture practice, the existing Carta graph, and the passage of time. They cannot be checked in isolation.

#### 3. Generality

A node belongs in the foundations only if it generalises across organisations and technology stacks. Stack-specific guidance (a particular cloud provider, language, framework, or vendor) belongs in organisation, team, or project levels.

The relevant test is whether the **principle** generalises, not whether every instantiation is universal. "Use a secrets manager rather than environment variables" generalises across stacks even though every implementation will be AWS Secrets Manager, HashiCorp Vault, or similar. The pattern is stack-general; the implementation is stack-specific. The pattern belongs in the foundations; implementation guidance belongs in organisation levels.

Patterns may be domain-specific without being stack-specific. Event sourcing applies to a subset of systems but generalises across stacks within that subset; it belongs in the foundations, scoped to the relevant `applies_to` contexts.

**Test:** could a reasonable team building any system in this category (web application, data pipeline, agentic system) apply this pattern, regardless of their stack choices? If applicability requires committing to a specific vendor, framework, or language, it belongs in an organisation, team, or project level.

#### 4. Coherence

A node must fit cleanly into the existing graph. This means:

- It does not duplicate an existing node under different framing. If similar guidance exists, the contribution either extends the existing node or replaces it; it does not create a parallel one.
- It uses established vocabulary. Introducing a new term requires justification — the existing vocabulary genuinely doesn't cover the concept, not stylistic preference.
- Its edges are honestly declared. `prerequisites`, `conflicts_with`, and `contradicted_by` reflect actual relationships, not aspirational ones. If the contributor isn't sure whether a conflict exists, they investigate before submitting.
- It sits at a useful level of abstraction. Too granular and it can't compose; too broad and it can't be acted on. Reviewers should ask whether the node would naturally combine with two or three others to form a solution, or whether it spans concerns that should be separate nodes.

**Test:** does this node strengthen the graph or fragment it? If accepting it would create duplication, vocabulary drift, or false edges, the contribution needs revision.

#### 5. Currency

A node must reflect current understanding. Patterns that the field has moved on from are not admitted, even if they were once standard practice. Sources older than five years require an explicit note in the node confirming the pattern still holds — either evidence of continued relevance or a statement of why the older source remains authoritative.

This criterion exists because Provenance alone is insufficient. A pattern can cite a real, verifiable 2009 source and be substantively wrong by current standards. Currency closes that gap.

Currency is reassessed periodically by the lint operation. Nodes that fall out of currency are marked deprecated rather than silently retained.

**Test:** does this pattern reflect what a thoughtful practitioner would recommend today? If newer sources contradict the cited evidence, or if the pattern's underlying assumptions no longer hold, the node needs revision before admission.

### Standards in the foundations

The `foundations/40-standards/` folder contains **meta-standards and templates only** — guidance on how teams should write standards, with templates and examples. It does not contain opinionated standards that prescribe specific practices.

This is because most concrete standards (API design conventions, naming rules, testing requirements) are organisational choices rather than universal truths. They fail Generality almost by definition. A standard like "all APIs use OpenAPI specs" is a defensible org choice but not a universal architectural truth, and its presence in the foundations would impose preferences inappropriately.

What the foundations' `40-standards/` does contain:

- **Templates** — the structural form a standard should take (frontmatter schema, required sections, levels of enforceability).
- **Meta-standards** — guidance on how to write standards well (e.g. "every standard must specify what failure to comply looks like and what the remediation is").
- **Cross-cutting concerns** — practices so universally agreed that they meet all five admission criteria, e.g. "secrets must not be committed to version control." These are rare. When in doubt, the standard belongs in an organisation level.

Concrete, opinionated standards live in `org/standards/`, `teams/<team>/standards/`, or `projects/<project>/standards/`. The traversal reads foundation meta-standards (for how to interpret a standard) and org/team/project standards (for what to actually do).

### Decisions

Decision records (ADRs) do not live in the foundations. ADRs record choices made in a specific context — they are inherently organisational, team, or project-specific. The foundations haven't made any choices; they describe patterns and trade-offs for others to choose from.

ADRs live in:

- `org/decisions/` — organisation-wide decisions
- `teams/<team>/decisions/` — team-specific decisions
- `projects/<project>/decisions/` — project-specific decisions

### Promotion and demotion

The foundations are not static. Nodes move in and out as evidence accumulates and understanding shifts.

**Promotion.** A node at any level may be promoted to the foundations when it meets all five admission criteria. Promotion happens by PR to the foundations. Evidence of use across multiple organisations strengthens the case but is not strictly required — a single organisation's experience is enough if the pattern itself generalises.

**Demotion.** A node in the foundations that no longer meets admission criteria is demoted, not silently removed. Demotion paths:

- **Failing Currency** — the node is marked `maturity: deprecated` and remains in the foundations for one minor version, with a note pointing to the superseding pattern (if any). It is then moved to an `archive/` folder, retained for historical reference but excluded from traversal.
- **Failing Generality** (a pattern previously thought general turns out to be stack-specific) — the node is moved to an `archive/` folder alongside the foundations, so existing setups that reference it continue to resolve.
- **Failing Coherence** (a node duplicates or fragments existing guidance) — the node is merged into the more authoritative existing node, with a redirect from the old ID.
- **Failing Provenance or Decidability** (rare for admitted nodes; usually surfaces during lint) — the node is held for revision; if it cannot be repaired within a release cycle, it is demoted as if failing Currency.

All demotions are logged in `LOG.md` with the triggering reason and the destination.

### Reviewer checklist

For PR reviewers, the criteria reduce to seven questions. A "no" to any of them is grounds for requesting changes:

1. Could an agent make a defensible decision from this node? *(Decidability)*
2. Is the decision non-obvious — does this earn its place? *(Decidability)*
3. Can a stranger verify the cited sources? *(Provenance)*
4. Does the principle generalise across stacks within its applicable contexts? *(Generality)*
5. Does the node strengthen the graph rather than fragment it? *(Coherence)*
6. Does it reflect current understanding, with sources younger than five years (or older sources explicitly justified)? *(Currency)*
7. If this is a standard, does it belong in the foundations or an organisation level? *(Standards clause)*

A node that passes all seven enters the foundations. A node that fails one or two can usually be revised. A node that fails three or more probably belongs in an organisation, team, or project level.

## Change process

### Adding a new node

1. **Author the node** using the schema in `00-meta/node-schema.md` and the relevant template. Ensure all five admission criteria are met.
2. **Open a PR** with the new node. The PR description must state why this node belongs in the foundations (generality), what decision it enables (decidability), and what evidence supports it (provenance).
3. **Review**. A maintainer reviews against the admission criteria. Common reasons for rejection: too stack-specific, "When NOT to use" section is missing or empty, no sources cited.
4. **Merge**. On approval, the node enters the foundations. An agent may then propose follow-up PRs to update related nodes' frontmatter links (ingest operation).

### Editing an existing node

- **Minor edits** (typos, link fixes, clarifications that don't change meaning) can be merged by any maintainer without ceremony.
- **Substantive edits** (changing when-to-use guidance, adding or removing trade-offs, revising the solution sketch) require a PR with rationale. If the edit changes the node's recommendations, it should be accompanied by an ADR explaining why.
- **Maturity changes** (experimental → stable, stable → deprecated) require a PR with evidence. Promotion to stable requires demonstrated use across multiple contexts. Deprecation requires an explanation of what supersedes the pattern and why.

### Recording a decision (ADR)

ADRs record non-trivial choices that affect the knowledge base. An ADR is required when:

- A new node contradicts or constrains an existing one.
- A pattern is deprecated in favour of an alternative.
- A substantive edit changes the recommendations of an existing node.
- A dispute between contributors is resolved.
- A team or project overrides a higher-level node.

ADRs follow the template in `00-meta/adr-template-guide.md`. Once merged, an agent propagates the ADR's effects across the graph — updating `contradicted_by` fields, adjusting maturity statuses, adding notes to affected nodes. These propagation changes are proposed as a separate PR (ingest operation) and reviewed before merge.

ADRs live at the level where the decision was made:

- `org/decisions/` for organisation-wide decisions
- `teams/<team>/decisions/` for team-specific decisions
- `projects/<project>/decisions/` for project-specific decisions

### Removing a node

Nodes are not deleted outright; they follow the demotion process described under **Admission criteria > Promotion and demotion**. The demotion path depends on which criterion the node no longer meets. All demotions require a PR and are logged.

If a node was added in error (wrong scope, factually incorrect, duplicate), it may be removed directly with a PR and an ADR explaining the removal.

## Contradictions

Contradictions are a feature, not a bug. When two nodes make conflicting claims, the conflict is made explicit:

1. Both nodes gain `contradicted_by` entries pointing to each other.
2. A `## Contradictions` section is added to each with a description of the conflict.
3. An ADR is opened to resolve the contradiction. The ADR may side with one node, deprecate the other, narrow the scope of each, or document the contradiction as a legitimate context-dependent trade-off.

Unresolved contradictions are valid — some trade-offs are genuinely context-dependent. The requirement is that they are **visible**, not that they are eliminated.

Agents flag potential contradictions during lint. Humans write the ADR.

## Layers and the foundations

The boundary between foundations and other levels is enforced by the generality criterion. When in doubt:

- If the guidance names a specific technology, it belongs in an organisation, team, or project level.
- If the guidance describes a pattern that could be implemented in multiple stacks, it belongs in the foundations.

Nodes may be promoted from any level to the foundations — see **Admission criteria > Promotion and demotion**.

Each level (org, team, project) has the same internal structure:

- `overrides/` — override foundation or higher-level nodes. Files use the level suffix for uniqueness.
- `extensions/` — new nodes that don't exist in the foundations. Files use the level suffix.
- `standards/` — concrete standards. Files use the level suffix.
- `decisions/` — ADRs recording choices at this level. Files use the level suffix.

Any level can override any other level. The constraint is documentation: overrides must be accompanied by a decision record explaining the reasoning. This applies whether the override tightens or relaxes the higher-level guidance. The goal is transparency, not rigidity — a project that needs to relax a standard to ship can do so, as long as the reasoning is visible.

## Versioning

Carta is pre-1.0. The node schema, directory conventions, and frontmatter fields may change. Breaking changes are documented in ADRs and announced in the changelog.

Post-1.0, the node schema is the stability contract. Fields may be added but not removed or renamed without a major version bump. This matters because agents and tooling parse frontmatter programmatically — breaking the schema breaks the traversal.

## Amending this charter

This charter is itself subject to change via ADR. Propose a change by opening a PR that modifies this file and includes an ADR explaining the rationale. Charter changes require approval from at least two maintainers.
