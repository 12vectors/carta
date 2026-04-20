# Carta Overview

A single entry point to the technical picture of Carta — structure, four-level model, node schema, and operations. Each section links out to the normative reference for the detail.

For the short pitch, see [`README.md`](../README.md). For governance of the foundations, see [`CHARTER.md`](../CHARTER.md).

---

## Repository structure

```
carta/                                  # Repository root = Obsidian vault
├── README.md                           # Pitch and quickstart
├── CHARTER.md                          # How the foundations are governed
├── DECISION_TREE.md                    # Top-level routing for traversal
├── LOG.md                              # Append-only record of operations
│
├── 00-meta/                            # How Carta works (system docs)
│   ├── overview.md                     # This file
│   ├── quickstart.md                   # 10-minute hands-on guide
│   ├── traversal-protocol.md           # Algorithm agents follow
│   ├── operations.md                   # Traverse, ingest, lint, capture
│   ├── node-schema.md                  # Frontmatter contract
│   ├── obsidian-setup.md               # Obsidian vault setup
│   ├── adr-template-guide.md           # How to write ADRs
│   └── glossary.md                     # Canonical terminology
│
├── foundations/                        # Starter knowledge base
│   ├── 05-pillars/                     # Well-Architected quality lenses (reliability, security, cost, op-ex, performance)
│   ├── 10-contexts/                    # System archetypes
│   ├── 15-principles/                  # Cross-cutting design heuristics above patterns
│   ├── 20-patterns/                    # Reusable patterns — styles/, tactics/<concern>/, integration/
│   ├── 25-decision-trees/              # Selection guides between alternative patterns
│   ├── 30-solutions/                   # Composed patterns
│   ├── 40-standards/                   # Meta-standards and templates only
│   └── 50-antipatterns/                # What not to do
│
├── templates/                          # Node scaffolding (tpl-*.md)
│
├── org/                                # Organisation-wide level
│   ├── overrides/                      # e.g. pattern-rest-api.org.md
│   ├── extensions/
│   ├── standards/
│   └── decisions/
│
├── teams/<team-name>/                  # Team-specific level
│   ├── overrides/                      # e.g. pattern-rest-api.platform.md
│   ├── extensions/
│   ├── standards/
│   └── decisions/
│
├── projects/<project-name>/            # Project-specific level
│   ├── overrides/                      # e.g. pattern-rest-api.payments-api.md
│   ├── extensions/
│   ├── standards/
│   └── decisions/
│
├── commands/
│   ├── carta.md                        # Slash command for coding agents
│   └── SETUP.md                        # Slash command installation
│
└── tools/
    ├── validate.py                     # Frontmatter and link validator (CI)
    └── lint.py                         # Semantic graph health checker
```

Filenames are globally unique across the vault. Foundation files use the node type prefix (`pattern-`, `context-`, etc.). Files outside the foundations add a level suffix for uniqueness: `.org.md`, `.<team-name>.md`, `.<project-name>.md`. This ensures Obsidian wikilinks resolve unambiguously.

## Four-level model

Carta resolves knowledge across four levels. Each more specific level can override or extend the level above it:

| Level | Location | Contains | Who owns it |
|-------|----------|----------|-------------|
| **Foundations** | `foundations/` | Generic patterns, contexts, antipatterns, solutions, meta-standards | Carta maintainers |
| **Organisation** | `org/` | Org-wide overrides, extensions, standards, decisions | Your org |
| **Team** | `teams/<team>/` | Team-specific overrides, extensions, standards, decisions | The team |
| **Project** | `projects/<project>/` | Project-specific overrides, extensions, standards, decisions | The project team |

**Override resolution** for patterns is most-specific-wins: project → team → org → foundations. For standards, decisions, and extensions, all levels accumulate.

**Any level can override any other level.** The constraint is transparency — any override must be accompanied by a decision record explaining why. A project that needs to relax an org standard to ship can do so, as long as the reasoning is documented.

Not every level is required. Many setups will use only foundations + org. Teams and projects are available when needed but add no overhead if unused.

Decisions (ADRs) do not live in the foundations. The foundations describe patterns and trade-offs; decisions are choices made by organisations, teams, and projects.

## The node schema

Every node follows a single schema. The frontmatter **is the graph** — agents traverse it without parsing prose, and Obsidian renders it as a navigable knowledge graph.

```markdown
---
id: pattern-circuit-breaker
title: Circuit Breaker
type: pattern                 # pattern | antipattern | standard | solution | context | adr
category: resilience          # style | <concern> | integration
maturity: stable              # experimental | stable | deprecated
pillars: [reliability]        # reliability | security | cost | operational-excellence | performance
tags: [pattern, resilience, stable]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-retry-with-backoff]]"
related:
  - "[[pattern-bulkhead]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Release It! (Nygard, 2018) ch. 5"
  - "https://martinfowler.com/bliki/CircuitBreaker.html"
---

## When to use
## When NOT to use
## Decision inputs
## Solution sketch
## Trade-offs
## See also
```

Each node type (pattern, antipattern, standard, solution, context, adr) has its own required fields and body sections. See [`node-schema.md`](node-schema.md) for the complete field reference, provenance rules, and validation requirements.

## Operations

Carta defines four operations that agents and humans perform on the knowledge base:

- **Traverse** — consult the knowledge base to select patterns for a task. The primary operation. See [`traversal-protocol.md`](traversal-protocol.md) for the full algorithm.
- **Ingest** — propagate the effects of a new decision across the graph (agent-proposed, human-reviewed).
- **Lint** — periodic health check for contradictions, orphans, stale nodes, and broken links.
- **Capture** — record a novel pattern composition discovered during traversal as a new solution node.

Each operation has a defined trigger, procedure, actor, and logging format. See [`operations.md`](operations.md) for the complete reference.

Every operation is logged in `LOG.md` — an append-only chronological record of traversals, ingests, lint passes, and captures.

## How authoring works

The maintenance burden that typically kills knowledge bases — "I don't have time to write this up" — doesn't apply to Carta. Agents draft nodes under developer direction; developers review, edit, and commit. The tedious writing is automated; the judgement stays with the team.

A typical authoring flow:

1. A developer runs `/carta` on a real task and sees that a relevant pattern is missing.
2. They ask an agent to draft the pattern node, citing sources and following the schema in [`node-schema.md`](node-schema.md).
3. The developer reviews the draft, edits for accuracy and team fit, and commits.
4. An agent follow-up proposes frontmatter updates to related nodes (the ingest operation).

See [`quickstart.md`](quickstart.md) for a hands-on walkthrough.

## Further reading

- [`CHARTER.md`](../CHARTER.md) — governance of the foundations: admission criteria, contradictions, promotion and demotion.
- [`node-schema.md`](node-schema.md) — the normative frontmatter contract.
- [`traversal-protocol.md`](traversal-protocol.md) — the algorithm agents follow at decision time.
- [`operations.md`](operations.md) — the four operations in detail.
- [`glossary.md`](glossary.md) — canonical terminology.
- [`obsidian-setup.md`](obsidian-setup.md) — setting up the Obsidian vault.
