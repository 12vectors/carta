# Carta

**An architectural charter for teams and their coding agents. Patterns, standards, and decisions, written down.**

---

## What is Carta?

Carta is a system for managing architecture knowledge — a persistent, interlinked knowledge base of software architecture patterns, standards, anti-patterns, and decisions, structured so that both humans and coding agents can traverse it reliably.

Unlike documentation that's written once and abandoned, or context that's re-derived from scratch on every query, Carta is **compiled once and kept current**. Cross-references are already there. Contradictions have already been flagged. The synthesis already reflects every decision your team has made. It compounds over time.

Carta operates across three levels:

- **Foundations** — a starter knowledge base of reusable patterns and practices that apply across organisations. This is what Carta ships out of the box.
- **Organisation** — your team's overrides, extensions, concrete standards, and recorded decisions, layered on top of the foundations.
- **Project** — project-specific customisations within your organisation, for when a particular system needs its own architectural choices.

Coding agents consult Carta before making non-trivial architectural choices. Humans consult it during design reviews, onboarding, and whenever someone asks "how do we do X here?" Open it in Obsidian and the whole thing lights up as a navigable graph.

## Why Carta exists

Coding agents are increasingly capable but architecturally rootless. They produce locally-correct code that ignores your team's conventions, re-invents patterns you've already rejected, and makes silent choices where explicit ones are needed.

Existing approaches each miss something:

- **Wikis** are written for humans to browse, not for agents to traverse. They lack the structure agents need to make deterministic choices. And humans abandon them because the maintenance burden grows faster than the value.
- **Rules files and system prompts** are flat and don't scale. They describe preferences, not a reasoned graph of patterns and their relationships.
- **RAG over documents** re-derives knowledge from scratch on every query. There's no accumulation — ask a subtle question that requires synthesising five sources, and the system has to find and piece together fragments every time.
- **Spec-driven workflows** (like GitHub's Spec Kit) are excellent for per-feature delivery but presume the architectural knowledge already exists somewhere. Carta is where it lives.

Carta fills the gap: a durable, versioned, machine-traversable record of how your team builds software — and why. Humans (and agents) author and curate the knowledge. Agents maintain the graph, propagate changes, flag contradictions, and traverse it at decision time. The tedious bookkeeping that typically kills knowledge bases is handled by the agent; the thinking stays with the team.

## Design principles

1. **Compiled, not retrieved.** Carta is a persistent, compounding artefact. Knowledge is synthesised once and kept current — not re-derived on every query.
2. **Human/agent-authored, agent-maintained.** People write the patterns and make the decisions. Agents propagate changes across the graph, check consistency, and propose new compositions. Agents don't unilaterally add to the foundations.
3. **Decisions are first-class.** Patterns explain *what*; ADRs explain *why this one, here, now*.
4. **Grounded in evidence.** Patterns cite their sources — papers, incident reports, codebases, conversations. Assertions without provenance are flagged during lint.
5. **Contradictions are explicit.** When new decisions conflict with existing patterns, the conflict is flagged and linked — never silently overwritten.
6. **Three levels, cleanly separated.** Foundations are shared; organisation and project layers are yours.
7. **Transparency over rigidity.** Any level can override any other level — the constraint is that overrides are documented, not that they're forbidden.
8. **Traversal is deterministic.** Agents follow a documented algorithm, not vibes.
9. **Open by default.** The foundations are open source; organisation and project layers stay private.
10. **Tool-agnostic, Obsidian-native.** Plain markdown that works anywhere; wikilinks and frontmatter that make Obsidian's graph view, backlinks, and Dataview queries work out of the box.

## Structure

```
carta/                                 # Repository root = Obsidian vault
├── README.md                          # This file
├── CHARTER.md                         # How the foundations are governed
├── DECISION_TREE.md                   # Top-level routing for agents
├── LOG.md                             # Append-only changelog of all operations
│
├── foundations/                        # Starter knowledge base (shared, generic)
│   ├── 00-meta/
│   │   ├── traversal-protocol.md      # The algorithm agents follow
│   │   ├── operations.md              # Traverse, ingest, lint, capture operations
│   │   ├── node-schema.md             # Frontmatter contract
│   │   ├── obsidian-setup.md          # Obsidian vault setup guide
│   │   ├── adr-template-guide.md      # How to write ADRs
│   │   └── glossary.md
│   │
│   ├── 10-contexts/                   # "What kind of system am I building?"
│   │   ├── context-web-application.md
│   │   ├── context-data-pipeline.md
│   │   ├── context-ml-system.md
│   │   ├── context-agentic-system.md
│   │   ├── context-event-driven-system.md
│   │   └── context-batch-processing.md
│   │
│   ├── 20-patterns/                   # Reusable architectural patterns
│   │   ├── communication/
│   │   ├── data/
│   │   ├── resilience/
│   │   ├── scaling/
│   │   ├── security/
│   │   ├── agentic/
│   │   └── observability/
│   │
│   ├── 30-solutions/                  # Composed patterns for common problems
│   ├── 40-standards/                  # Meta-standards and templates only
│   └── 50-antipatterns/               # What not to do, and why
│
├── templates/                         # Node scaffolding templates (used at all levels)
│   ├── tpl-pattern.md
│   ├── tpl-antipattern.md
│   ├── tpl-standard.md
│   ├── tpl-solution.md
│   ├── tpl-context.md
│   └── tpl-adr.md
│
├── overrides/                         # Org-level overrides of foundation nodes
├── extensions/                        # Org-specific patterns, contexts, etc.
├── standards/                         # Org-level concrete standards
├── decisions/                         # Org-level ADRs
│
├── projects/                          # Project-specific layers
│   └── <project-name>/
│       ├── overrides/
│       ├── extensions/
│       ├── standards/
│       └── decisions/
│
├── commands/
│   └── carta.md                       # Slash command for coding agents
│
└── tools/
    ├── validate.py                    # Frontmatter and link validator (CI)
    ├── lint.py                        # Semantic graph health checker
    └── build-index.py                 # Generates static INDEX.md
```

Filenames are globally unique across the vault and prefixed by node type (`pattern-`, `context-`, `solution-`, `standard-`, `antipattern-`, `adr-`). This ensures Obsidian wikilinks resolve unambiguously. Numeric folder prefixes in foundations enforce reading order: contexts before patterns, patterns before solutions.

## Three-level model

Carta resolves knowledge across three levels. Each more specific level can override or extend the one above it:

| Level | Location | Contains | Who owns it |
|-------|----------|----------|-------------|
| **Foundations** | `foundations/` | Generic patterns, contexts, antipatterns, solutions, meta-standards | Carta maintainers |
| **Organisation** | Root-level `overrides/`, `extensions/`, `standards/`, `decisions/` | Org-specific overrides, standards, and decisions | Your team |
| **Project** | `projects/<name>/` | Project-specific overrides, standards, and decisions | Project team |

**Override resolution:** for patterns, the most specific level wins (project → org → foundations). For standards, decisions, and extensions, all levels accumulate.

**Any level can override any other level.** The constraint is not hierarchy but transparency — any override must be accompanied by a decision record explaining why. A project that needs to relax an org standard to ship can do so, as long as the reasoning is documented.

Decisions (ADRs) do not live in the foundations. The foundations describe patterns and trade-offs; decisions are choices made by organisations and projects.

## The node schema

Every node follows a single schema. The frontmatter **is the graph** — agents traverse it without parsing prose, and Obsidian renders it as a navigable knowledge graph.

```markdown
---
id: pattern-circuit-breaker
title: Circuit Breaker
type: pattern                 # pattern | antipattern | standard | solution | context | adr
category: resilience
maturity: stable              # experimental | stable | deprecated
tags: [pattern, resilience, stable]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-retry-with-backoff]]"
related:
  - "[[pattern-bulkhead]]"
  - "[[pattern-graceful-degradation]]"
conflicts_with: []
contradicted_by: []           # Nodes whose claims conflict with this one
sources:                      # Evidence grounding this pattern
  - "Release It! (Nygard, 2018) ch. 5"
  - "https://martinfowler.com/bliki/CircuitBreaker.html"
---

## When to use
Symptoms or triggers an agent can pattern-match against.

## When NOT to use
Counter-indications.

## Decision inputs
Questions the agent must answer before choosing this pattern.

## Solution sketch
Minimal description + reference implementation pointer.

## Trade-offs
| Gain | Cost |
|------|------|
|      |      |

## Implementation checklist
- [ ] Concrete, verifiable steps.

## Contradictions
> [!contradiction]
> ADR-0012 recommends timeout-based fallback instead of circuit breaking
> for internal services. See [[adr-0012-timeout-over-circuit-breaker]].

If no contradictions exist, omit this section.

## See also
Links to related nodes, with the reason for each link:
- [[pattern-bulkhead]] — often combined for defence-in-depth
- [[pattern-graceful-degradation]] — the fallback strategy when the circuit opens
```

Each node type (pattern, antipattern, standard, solution, context, adr) has its own required fields and body sections. See `foundations/00-meta/node-schema.md` for the complete field reference, provenance rules, and validation requirements.

## Operations

Carta defines four operations that agents and humans perform on the knowledge base:

- **Traverse** — consult the knowledge base to select patterns for a task. This is the primary operation. See `foundations/00-meta/traversal-protocol.md` for the full algorithm.
- **Ingest** — propagate the effects of a new decision across the graph (agent-proposed, human-reviewed).
- **Lint** — periodic health check for contradictions, orphans, stale nodes, and broken links.
- **Capture** — record a novel pattern composition discovered during traversal as a new solution node.

Each operation has a defined trigger, procedure, actor, and logging format. See `foundations/00-meta/operations.md` for the complete reference.

Every operation is logged in `LOG.md` — an append-only chronological record of traversals, ingests, lint passes, and captures.

## Viewing Carta in Obsidian

Carta is plain markdown that works in any editor and renders on GitHub. For the richest experience, open the **repository root** as an Obsidian vault — you get a colour-coded graph view, backlinks across all nodes and layers, Dataview-powered indexes, Templater scaffolding for new nodes, and tag-based filtering.

**Obsidian is optional.** Agents don't need it (they read files directly). Contributors don't need it (any markdown editor works, and CI validates frontmatter). But it is the recommended way to explore the graph, review relationships, and author new nodes.

See `foundations/00-meta/obsidian-setup.md` for the full setup guide.

## Relationship to Spec Kit and similar tools

Carta is complementary to spec-driven development workflows like GitHub's Spec Kit.

- **Spec Kit** is a per-feature workflow: constitution → spec → plan → tasks → code.
- **Carta** is the durable knowledge the constitution and plan should draw from.

A typical integration: Spec Kit's `/plan` step invokes the Carta traversal skill to select patterns; new decisions produced during the run trigger an ingest operation, propagating changes back into the knowledge base and becoming inputs to future runs.

Carta is also useful outside any structured workflow — during code review, refactoring, debugging, or when answering architectural questions directly. Every traversal, ingest, lint, and capture is logged, so the knowledge base's evolution is traceable regardless of which workflow triggered it.

## Getting started

> Carta is pre-1.0. APIs, schemas, and directory conventions may change.

**Fork this repo** to start your organisation's Carta setup:

```bash
# Fork or clone carta
git clone https://github.com/[org]/carta.git my-org-architecture
cd my-org-architecture

# The structure is ready — foundations/ contains the starter knowledge base
# overrides/, extensions/, standards/, decisions/ are yours to fill
# projects/ is where project-specific layers go
```

**Open in Obsidian:**

```bash
# Open the repository root as a vault
# See foundations/00-meta/obsidian-setup.md for detailed setup
```

**Use the slash command:**

```bash
# From any project, in Claude Code:
/carta add authentication to the payment service
/carta choose a caching strategy for our product catalog API
```

See `commands/SETUP.md` for slash command installation.

## Governance

The foundations are governed by `CHARTER.md`. Organisation and project layers are self-governed.

**Roles.** Maintainers steward the foundations. Contributors propose changes. Agents maintain the graph under human supervision — they may propose link updates, maturity changes, ingests, and captures, but may not merge their own proposals, author new foundation patterns, or resolve contradictions. The boundary: agents handle structure; humans handle judgement.

**Admission.** The foundations are a minimal, high-trust reference. Five criteria determine what enters, split into form (how a node is written) and fit (how it relates to the world and the graph):

1. **Decidability** — an agent can make a defensible yes/no decision from the node, and that decision is non-obvious.
2. **Provenance** — every claim cites a verifiable source.
3. **Generality** — the principle applies across stacks and organisations.
4. **Coherence** — the node strengthens the graph rather than fragmenting it.
5. **Currency** — the node reflects current understanding.

**Standards.** The foundations' `40-standards/` contains meta-standards and templates only. Concrete, opinionated standards live in organisation and project layers.

**Decisions.** ADRs do not live in the foundations. They live in `decisions/` (org) or `projects/<name>/decisions/` (project).

**Demotion.** Nodes that no longer meet criteria are demoted, not silently removed. The demotion path depends on which criterion failed.

See `CHARTER.md` for the full admission criteria with tests, the change process, contradiction handling, and the reviewer checklist.

## Contributing

Contributions welcome. Before opening a PR:

1. Read `foundations/00-meta/node-schema.md` and make sure your frontmatter validates.
2. Use the templates in `templates/` to scaffold new nodes.
3. Run `python tools/validate.py` locally to catch structural issues before review.

See `CHARTER.md` for what the foundations accept and `CONTRIBUTING.md` for the full process.

## Status

| Component | Status |
|---|---|
| Node schema (wikilinks, tags, sources, contradictions) | Draft |
| Operations model (traverse, ingest, lint, capture) | Draft |
| Traversal skill | Draft |
| Foundations (`10-contexts/`, `20-patterns/`) | In progress |
| Three-level model (foundations, org, project) | Draft |
| Validator (`tools/validate.py`) | Planned |
| Linter (`tools/lint.py`) | Planned |
| Index builder (`tools/build-index.py`) | Planned |
| Obsidian setup guide | Done |
| Node templates (`templates/`) | Done |
| Canvas files for solutions | Planned |
| Spec Kit integration example | Planned |

## License

The Carta foundations are released under the MIT License. Organisation and project layers are yours; nothing in this license requires you to publish them.

## Credits

Carta is developed in the open. The name draws on the Latin *charta* — a written charter that constrains and enables, referred to and amended over time.

The operations model (traverse, ingest, lint, capture) draws on ideas from Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern, adapted from personal knowledge management to organisational architecture.
