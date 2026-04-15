# Glossary

Terms used in Carta with specific meaning.

---

**ADR (Architecture Decision Record)**
A node of type `adr` that records a non-trivial architectural decision — what was decided, why, what alternatives were considered, and what the consequences are. ADRs live in `90-decisions/` (core) or `decisions/` (overlay). See `adr-template-guide.md`.

**Antipattern**
A node of type `antipattern` describing a recurring architectural mistake — how to recognise it, why it happens, what goes wrong, and how to fix it. Antipatterns serve as a negative filter during traversal.

**Candidate set**
The set of patterns under consideration during a traversal, built from the matched context's `recommended_patterns` and refined by evaluation, prerequisite resolution, and conflict checking.

**Capture**
An operation that records a novel pattern composition discovered during traversal as a new solution node. See `operations.md`.

**Coherence**
An admission criterion assessing whether a node fits cleanly into the existing graph — no duplication, consistent vocabulary, honest edges, appropriate abstraction level. See `CHARTER.md`.

**Context**
A node of type `context` describing a category of system (e.g. web application, data pipeline, agentic system). Contexts are the entry point for traversal — agents match a task to a context, then follow its `recommended_patterns` links.

**Contradiction**
A relationship between two nodes whose claims conflict. Contradictions are explicit and bidirectional — both nodes link to each other via `contradicted_by`. Contradictions are not errors; they are navigable features of the graph.

**Core**
The generic, shared Carta knowledge base containing patterns, standards, antipatterns, contexts, and solutions that apply across organisations and stacks. Distinguished from organisation overlays.

**Currency**
An admission criterion requiring that nodes reflect current understanding. Sources older than five years require explicit justification. See `CHARTER.md`.

**Decidability**
An admission criterion requiring that every node gives an agent enough information to make a defensible yes-or-no decision about whether to apply it. See `CHARTER.md`.

**Decision tree**
`DECISION_TREE.md` — the top-level routing document that maps tasks to contexts via a signal table.

**Demotion**
The process of moving a node out of the core when it no longer meets admission criteria. Demotion paths vary by which criterion failed. See `CHARTER.md`.

**Extension**
A node in an organisation overlay that doesn't exist in the core — org-specific patterns, solutions, or standards. Extensions live in `extensions/` and are additive.

**Generality**
An admission criterion requiring that a node's principle applies across organisations and stacks. Stack-specific guidance belongs in overlays. See `CHARTER.md`.

**Ingest**
An operation that propagates the effects of a new decision or change across the graph — updating frontmatter links, maturity statuses, and affected nodes. See `operations.md`.

**Lint**
An operation that checks the health of the graph — detecting contradictions, orphans, stale nodes, missing pages, and other structural or semantic issues. See `operations.md`.

**Node**
Any file in Carta with valid frontmatter following the schema in `node-schema.md`. The six node types are: pattern, antipattern, standard, solution, context, adr.

**Overlay**
An organisation-specific extension of Carta containing overrides, extensions, stack choices, standards, and ADRs. Overlays include the generic core as a Git submodule and add org-specific knowledge on top.

**Override**
A file in an organisation overlay that replaces a core node for that organisation. Overrides live in `overrides/` with the suffix `.override.md`. During traversal, the override is read instead of the core node.

**Pattern**
A node of type `pattern` describing a reusable architectural approach — when to use it, when not to, what it trades off, and how to implement it.

**Promotion**
The process of moving a node from an overlay into the core when it meets all five admission criteria. See `CHARTER.md`.

**Provenance**
An admission criterion requiring that every pattern cite at least one verifiable source. See `CHARTER.md`.

**Signal**
An observable property of a task or system used to match it to a context. Signals appear in the `DECISION_TREE.md` signal table and in context nodes' `signals` field. Signals describe what a system *is*, not what technologies it uses.

**Solution**
A node of type `solution` describing a pre-composed combination of patterns for a common problem. Solutions include integration guidance that individual pattern nodes don't.

**Standard**
A node of type `standard` describing a non-negotiable practice. In the core, standards are limited to meta-standards, templates, and rare cross-cutting concerns. Concrete, opinionated standards live in overlays.

**Traverse**
The primary Carta operation — consulting the knowledge base to select patterns for a task. See `traversal-protocol.md` and `operations.md`.

**Wikilink**
An Obsidian-style link in the format `[[node-id]]` used in frontmatter fields to express relationships between nodes. Wikilinks are rendered as navigable links in Obsidian and parsed by agents and tooling.
