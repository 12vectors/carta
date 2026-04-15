# Carta

**An architectural charter for teams and their coding agents. Patterns, standards, and decisions, written down.**

---

## What is Carta?

Carta is compiled architectural knowledge — a persistent, interlinked knowledge base of software architecture patterns, standards, anti-patterns, and decisions, structured so that both humans and coding agents can traverse it reliably.

Unlike documentation that's written once and abandoned, or context that's re-derived from scratch on every query, Carta is **compiled once and kept current**. Cross-references are already there. Contradictions have already been flagged. The synthesis already reflects every decision your team has made. It compounds over time.

It has two layers:

- **A generic core** — reusable patterns and practices that apply across organisations.
- **An organisation overlay** — your team's overrides, extensions, stack choices, and recorded decisions, layered on top of the core.

Coding agents consult Carta before making non-trivial architectural choices. Humans consult it during design reviews, onboarding, and whenever someone asks "how do we do X here?" Open it in Obsidian and the whole thing lights up as a navigable graph.

## Why Carta exists

Coding agents are increasingly capable but architecturally rootless. They produce locally-correct code that ignores your team's conventions, re-invents patterns you've already rejected, and makes silent choices where explicit ones are needed.

Existing approaches each miss something:

- **Wikis** are written for humans to browse, not for agents to traverse. They lack the structure agents need to make deterministic choices. And humans abandon them because the maintenance burden grows faster than the value.
- **Rules files and system prompts** are flat and don't scale. They describe preferences, not a reasoned graph of patterns and their relationships.
- **RAG over documents** re-derives knowledge from scratch on every query. There's no accumulation — ask a subtle question that requires synthesising five sources, and the system has to find and piece together fragments every time.
- **Spec-driven workflows** (like GitHub's Spec Kit) are excellent for per-feature delivery but presume the architectural knowledge already exists somewhere. Carta is where it lives.

Carta fills the gap: a durable, versioned, machine-traversable record of how your team builds software — and why. It does it without minimum bloat. Humans (and agents) author and curate the knowledge. Agents maintain the graph, propagate changes, flag contradictions, and traverse it at decision time. The tedious bookkeeping that typicall kills knowledge bases is handled by the agent; the thinking stays with the team.

## Design principles

1. **Compiled, not retrieved.** Carta is a persistent, compounding artefact. Knowledge is synthesised once and kept current — not re-derived on every query.
2. **Human/agent-authored, agent-maintained.** People write the patterns and make the decisions. Agents propagate changes across the graph, check consistency, and propose new compositions. Agents don't unilaterally add to the core.
3. **Decisions are first-class.** Patterns explain *what*; ADRs explain *why this one, here, now*.
4. **Grounded in evidence.** Patterns cite their sources — papers, incident reports, codebases, conversations. Assertions without provenance are flagged during lint.
5. **Contradictions are explicit.** When new decisions conflict with existing patterns, the conflict is flagged and linked — never silently overwritten.
6. **Generic and organisation-specific, cleanly separated.** The core is shared; overrides and extensions stay local.
7. **Traversal is deterministic.** Agents follow a documented algorithm, not vibes.
8. **Open by default.** The generic core is open source; organisation overlays stay private.
9. **Tool-agnostic, Obsidian-native.** Plain markdown that works anywhere; wikilinks and frontmatter that make Obsidian's graph view, backlinks, and Dataview queries work out of the box.

## Structure

```
carta/
├── README.md                          # This file
├── CHARTER.md                         # How Carta itself is governed
├── INDEX.md                           # Dynamic index (Dataview queries + static fallback)
├── DECISION_TREE.md                   # Top-level routing for agents
├── LOG.md                             # Append-only changelog of all wiki operations
│
├── 00-meta/
│   ├── traversal-protocol.md          # The algorithm agents follow
│   ├── operations.md                  # Traverse, ingest, lint, capture operations
│   ├── node-schema.md                 # Frontmatter contract
│   ├── adr-template.md
│   └── glossary.md
│
├── 10-contexts/                       # "What kind of system am I building?"
│   ├── context-web-application.md
│   ├── context-data-pipeline.md
│   ├── context-ml-system.md
│   ├── context-agentic-system.md
│   ├── context-event-driven-system.md
│   └── context-batch-processing.md
│
├── 20-patterns/                       # Reusable architectural patterns
│   ├── communication/
│   │   ├── pattern-rest-api.md
│   │   ├── pattern-graphql.md
│   │   ├── pattern-event-bus.md
│   │   ├── pattern-message-queue.md
│   │   └── pattern-webhooks.md
│   ├── data/
│   │   ├── pattern-cqrs.md
│   │   ├── pattern-event-sourcing.md
│   │   ├── pattern-repository.md
│   │   └── pattern-rag-pipeline.md
│   ├── resilience/
│   │   ├── pattern-circuit-breaker.md
│   │   ├── pattern-retry-with-backoff.md
│   │   ├── pattern-bulkhead.md
│   │   └── pattern-graceful-degradation.md
│   ├── scaling/
│   │   ├── pattern-horizontal-scaling.md
│   │   ├── pattern-caching-strategies.md
│   │   └── pattern-sharding.md
│   ├── security/
│   │   ├── pattern-oauth2-oidc.md
│   │   ├── pattern-secrets-management.md
│   │   └── pattern-input-validation.md
│   ├── agentic/
│   │   ├── pattern-tool-use.md
│   │   ├── pattern-orchestration.md
│   │   ├── pattern-guardrails.md
│   │   ├── pattern-memory-architectures.md
│   │   └── pattern-human-in-the-loop.md
│   └── observability/
│       ├── pattern-structured-logging.md
│       ├── pattern-distributed-tracing.md
│       └── pattern-llm-observability.md
│
├── 30-solutions/                      # Composed patterns for common problems
│   ├── solution-build-rag-system.md
│   ├── solution-add-auth.md
│   └── solution-build-conversational-agent.md
│
├── 40-standards/                      # Non-negotiable practices
│   ├── standard-api-design.md
│   ├── standard-testing-strategy.md
│   └── standard-naming-conventions.md
│
├── 50-antipatterns/                   # What not to do, and why
│   ├── antipattern-distributed-monolith.md
│   ├── antipattern-god-service.md
│   └── antipattern-prompt-spaghetti.md
│
├── 90-decisions/                      # ADRs
│
├── skills/
│   └── carta-traversal/
│       └── SKILL.md                   # Traversal skill for coding agents
│
├── tools/
│   ├── validate.py                    # Frontmatter and link validator (CI)
│   ├── lint.py                        # Semantic graph health checker
│   └── build-index.py                 # Generates static INDEX.md for non-Obsidian use
│
├── .obsidian/                         # Obsidian vault config (optional)
│   ├── plugins/
│   │   └── dataview/
│   ├── templates/
│   │   ├── tpl-pattern.md
│   │   ├── tpl-antipattern.md
│   │   ├── tpl-standard.md
│   │   ├── tpl-solution.md
│   │   └── tpl-adr.md
│   └── graph.json                     # Graph view colour and filter presets
│
└── .github/
    └── workflows/
        └── validate.yml               # CI: validate frontmatter on PR
```

Filenames are globally unique across the vault and prefixed by node type (`pattern-`, `context-`, `solution-`, `standard-`, `antipattern-`, `adr-`). This ensures Obsidian wikilinks resolve unambiguously and makes the node type visible at a glance in search results. Numeric folder prefixes enforce reading order: contexts before patterns, patterns before solutions, standards cross-cut everything.

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

The example above shows a `pattern` node. Each node type (pattern, antipattern, standard, solution, context, adr) has its own required fields and body sections. See `00-meta/node-schema.md` for the complete field reference, provenance rules, and validation requirements.

## Operations

Carta defines four operations that agents and humans perform on the wiki:

- **Traverse** — consult the knowledge base to select patterns for a task. This is the primary operation. See `00-meta/traversal-protocol.md` for the full algorithm.
- **Ingest** — propagate the effects of a new decision across the graph (agent-proposed, human-reviewed).
- **Lint** — periodic health check for contradictions, orphans, stale nodes, and broken links.
- **Capture** — record a novel pattern composition discovered during traversal as a new solution node.

Each operation has a defined trigger, procedure, actor, and logging format. See `00-meta/operations.md` for the complete reference.

Every operation is logged in `LOG.md` — an append-only chronological record of traversals, ingests, lint passes, and captures. The log format is defined in `00-meta/operations.md`.

## Organisation overlay

Teams don't fork Carta. They extend it.

```
your-org-carta/
├── README.md
├── ORG_CONTEXT.md                     # Stack, scale, constraints, team shape
├── LOG.md                             # Org-specific operation log
├── carta/                             # Git submodule → the generic core
│
├── overrides/                         # Override core nodes selectively
│   └── pattern-rest-api.override.md   # Org take: "we use FastAPI, OpenAPI-first"
│
├── extensions/                        # Org-specific nodes not in core
│   ├── pattern-multi-tenant-isolation.md
│   └── solution-onboard-new-tenant.md
│
├── stack/                             # Concrete tech choices
│   ├── languages.md
│   ├── frameworks.md
│   └── datastores.md
│
├── standards/                         # Org versions of standards
│   ├── standard-coding-python.md
│   └── standard-coding-typescript.md
│
└── decisions/                         # Real ADRs
    ├── adr-0001-postgres-over-mongodb.md
    └── adr-0002-fastapi-as-default.md
```

**Override resolution rule:** when looking up a node `X`, the agent checks for `X.override.md` in `overrides/` first, then falls back to `carta/X.md`. Extensions are additive — they introduce nodes that don't exist in the core. This rule is enforced by the traversal skill and documented in each overlay's README.

The `.override.md` suffix avoids filename collisions in Obsidian. When both are open in the same vault, wikilinks resolve unambiguously and the graph shows both the core node and the override as distinct, linked entries.

The organisation overlay has its own `LOG.md` tracking org-specific operations — ingests triggered by internal ADRs, lint results against the combined graph, captures from real project work.

## Viewing Carta in Obsidian

Carta is plain markdown that works in any editor and renders on GitHub. For the richest experience, open it as an Obsidian vault.

**What you get:**

- **Graph view** — the full pattern graph, colour-coded by node type. Orphan nodes (missing links) are immediately visible. Contradiction edges stand out.
- **Backlinks** — open any pattern and see every node that references it, including contradiction links.
- **Dataview indexes** — `INDEX.md` uses Dataview queries to generate live, filterable tables of all patterns, grouped by category, maturity, or context.
- **Canvas** — solutions in `30-solutions/` have optional `.canvas` files that show how patterns compose visually.
- **Templater** — run "New Pattern", "New ADR", or "New Anti-Pattern" commands to scaffold a valid node with correct frontmatter.
- **Tag pane** — filter instantly by `#pattern`, `#antipattern`, `#stable`, `#deprecated`, etc.

**Setup:**

```bash
git clone https://github.com/[org]/carta.git
# Open the carta/ directory as an Obsidian vault
# Obsidian will prompt to trust plugins — accept to enable Dataview and Templater
```

The `.obsidian/` folder ships recommended plugin configs, graph view presets, and templates. Everything works on first open.

**Obsidian is optional.** Agents don't need it (they read files directly). Contributors don't need it (any markdown editor works, and CI validates frontmatter). But it is the recommended way to explore the graph, review relationships, and author new nodes.

## Relationship to Spec Kit and similar tools

Carta is complementary to spec-driven development workflows like GitHub's Spec Kit.

- **Spec Kit** is a per-feature workflow: constitution → spec → plan → tasks → code.
- **Carta** is the durable knowledge the constitution and plan should draw from.

A typical integration: Spec Kit's `/plan` step invokes the Carta traversal skill to select patterns; new decisions produced during the run trigger an ingest operation, propagating changes back into the organisation overlay and becoming inputs to future runs.

Carta is also useful outside any structured workflow — during code review, refactoring, debugging, or when answering architectural questions directly. Every traversal, ingest, lint, and capture is logged, so the wiki's evolution is traceable regardless of which workflow triggered it.

## Getting started

> Carta is pre-1.0. APIs, schemas, and directory conventions may change.

**Use Carta with your agent:**

```bash
git clone https://github.com/[org]/carta.git
# Point your coding agent at the carta/ directory
# Load skills/carta-traversal/SKILL.md into the agent's context
```

**Start your organisation overlay:**

```bash
git clone https://github.com/[org]/carta-overlay-template.git your-org-carta
cd your-org-carta
git submodule add https://github.com/[org]/carta.git carta
# Fill in ORG_CONTEXT.md, stack/, and standards/
```

**Explore in Obsidian:**

```bash
# Open carta/ as a vault in Obsidian
# Or open your-org-carta/ to see both core and overlay together
```

**Validate and lint:**

```bash
python tools/validate.py    # Structural: frontmatter schema, link integrity
python tools/lint.py         # Semantic: contradictions, orphans, staleness, missing sources
```

## Governance

The generic core is governed by `CHARTER.md`. Organisation overlays are self-governed.

**Roles.** Maintainers steward the core. Contributors propose changes. Agents maintain the graph under human supervision — they may propose link updates, maturity changes, ingests, and captures, but may not merge their own proposals, author new core patterns, or resolve contradictions. The boundary: agents handle structure; humans handle judgement.

**Admission.** The core is a minimal, high-trust reference. Five criteria determine what enters, split into form (how a node is written) and fit (how it relates to the world and the graph):

1. **Decidability** — an agent can make a defensible yes/no decision from the node, and that decision is non-obvious.
2. **Provenance** — every claim cites a verifiable source.
3. **Generality** — the principle applies across stacks and organisations.
4. **Coherence** — the node strengthens the graph rather than fragmenting it.
5. **Currency** — the node reflects current understanding.

**Standards.** The core's `40-standards/` contains meta-standards and templates only. Concrete, opinionated standards live in organisation overlays.

**Demotion.** Nodes that no longer meet criteria are demoted, not silently removed. The demotion path depends on which criterion failed.

See `CHARTER.md` for the full admission criteria with tests, the change process, contradiction handling, and the reviewer checklist.

## Contributing

Contributions welcome. Before opening a PR:

1. Read `00-meta/node-schema.md` and make sure your frontmatter validates.
2. Use the Obsidian Templater templates (or copy `00-meta/node-schema.md` manually) to scaffold new nodes.
3. Run `python tools/validate.py` locally to catch structural issues before review.

See `CHARTER.md` for what the core accepts and `CONTRIBUTING.md` for the full process.

## Status

| Component | Status |
|---|---|
| Node schema (wikilinks, tags, sources, contradictions) | Draft |
| Operations model (traverse, ingest, lint, capture) | Draft |
| Traversal skill | Draft |
| Generic core (`10-contexts/`, `20-patterns/`) | In progress |
| Overlay template | Planned |
| Validator (`tools/validate.py`) | Planned |
| Linter (`tools/lint.py`) | Planned |
| Index builder (`tools/build-index.py`) | Planned |
| Obsidian vault config (`.obsidian/`) | Planned |
| Obsidian Templater templates | Planned |
| Canvas files for solutions | Planned |
| Spec Kit integration example | Planned |

## License

The Carta generic core is released under the MIT License. Organisation overlays are yours; nothing in this license requires you to publish them.

## Credits

Carta is developed in the open. The name draws on the Latin *charta* — a written charter that constrains and enables, referred to and amended over time.

The operations model (traverse, ingest, lint, capture) draws on ideas from Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern, adapted from personal knowledge management to organisational architecture.
