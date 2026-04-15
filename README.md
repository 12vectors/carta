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

Link fields (`applies_to`, `prerequisites`, `related`, `conflicts_with`, `contradicted_by`) use `[[wikilinks]]` so Obsidian's graph view and backlinks index pick them up automatically. The traversal skill strips the `[[ ]]` wrappers when resolving IDs programmatically.

The `sources` field grounds every pattern in evidence — books, papers, blog posts, incident reports, codebases. Patterns without sources are flagged during lint. This is what separates Carta from opinion-driven documentation: every claim has provenance.

The `contradicted_by` field and the optional `## Contradictions` section make conflicts navigable rather than hidden. When a new ADR or pattern contradicts an existing node, the contradiction is linked in both directions. Agents check this field during traversal; humans see it in Obsidian's backlinks panel.

The `tags` field enables Obsidian's tag pane for filtering by node type and maturity. The `type` field serves the same purpose for agents and the validator.

The schema is enforced by `tools/validate.py`. Broken frontmatter fails CI.

## Operations

Carta defines four operations that agents and humans perform on the wiki. These are documented in `00-meta/operations.md` and encoded in the traversal skill.

### Traverse

The primary operation. An agent with a task consults Carta to select the right patterns, check constraints, and compose a solution. The traversal algorithm:

1. Read the task or goal.
2. Consult `DECISION_TREE.md` to identify the context (from `10-contexts/`).
3. From the context, follow `recommended_patterns` links.
4. For each candidate pattern, check `When to use`, `When NOT to use`, and `conflicts_with`.
5. Resolve `prerequisites` recursively.
6. Check `contradicted_by` — if a contradiction exists, read the linked node to understand the conflict and whether it's been resolved by an ADR.
7. Cross-reference `40-standards/` for non-negotiables.
8. Cross-reference `50-antipatterns/` as a negative filter.
9. Prefer composed solutions from `30-solutions/` when available.
10. Check `90-decisions/` for ADRs that constrain or resolve the choice.
11. Log the chosen path as a new ADR if the decision is non-trivial.

### Ingest

When a new ADR is committed or an architectural decision is made, the agent propagates changes across the graph. A single decision might touch many nodes — updating `contradicted_by` fields, revising maturity statuses, adjusting solution compositions, adding notes to affected patterns.

The ingest operation is **agent-proposed, human-reviewed**. The agent identifies which nodes are affected, drafts the updates, and opens a PR. A human reviews and merges. This is the maintenance cycle that keeps Carta current without the bookkeeping burden that kills traditional wikis.

Each ingest is logged in `LOG.md` with the triggering event, affected nodes, and outcome.

### Lint

A periodic health check of the graph. The lint operation looks for:

- **Contradictions** — nodes whose claims conflict but aren't linked via `contradicted_by`.
- **Stale nodes** — patterns whose `sources` have been superseded by newer evidence.
- **Orphans** — nodes with no inbound links (nothing references them).
- **Broken prerequisites** — circular or dangling prerequisite chains.
- **Missing pages** — concepts mentioned in prose but lacking their own node.
- **Ungrounded patterns** — nodes with an empty `sources` field.
- **Phantom conflicts** — `conflicts_with` edges that no longer hold after a recent ADR.

Lint can be run manually (`python tools/lint.py`) or triggered by a coding agent as part of regular maintenance. The results are logged in `LOG.md`.

### Capture

When a traversal produces a novel composition — patterns combined in a way not yet recorded in `30-solutions/` — the agent proposes it as a new solution node. This is how explorations compound into the knowledge base rather than disappearing into chat history.

A typical capture: an agent traversing Carta to solve "add observability to our LLM pipeline" composes `pattern-structured-logging` + `pattern-distributed-tracing` + `pattern-llm-observability` with org-specific stack choices. If no matching solution exists, the agent drafts `solution-instrument-llm-pipeline.md` with the composition and its rationale, and proposes it via PR.

Captures are logged in `LOG.md` with the originating task and the composed pattern set.

## The log

`LOG.md` is an append-only chronological record of everything that happens to the wiki — traversals, ingests, lint passes, captures. Each entry starts with a consistent prefix for parseability:

```markdown
## [2026-04-15] traverse | Add auth to payment service
Traversed: context-web-application → pattern-oauth2-oidc, pattern-secrets-management
ADR created: adr-0003-oauth2-for-payments.md

## [2026-04-14] ingest | ADR-0002 committed
Trigger: adr-0002-fastapi-as-default.md
Updated: pattern-rest-api.override.md (added FastAPI reference)
Updated: stack/frameworks.md (added FastAPI as default)

## [2026-04-13] lint | Periodic health check
Orphans found: pattern-sharding (no inbound links)
Ungrounded: antipattern-prompt-spaghetti (no sources)
Missing page: "feature flags" mentioned in 3 nodes but no pattern exists

## [2026-04-12] capture | LLM observability solution
Origin: task "instrument our RAG pipeline"
Created: solution-instrument-llm-pipeline.md
Composed: pattern-structured-logging + pattern-distributed-tracing + pattern-llm-observability
```

The log gives both humans and agents a timeline of the wiki's evolution. `grep "^## \[" LOG.md | tail -10` shows the last 10 operations. Agents read the log to understand what's been done recently and avoid redundant work.

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

Carta's generic core is stewarded by maintainers and shaped by community contribution. See `CHARTER.md` for the admission criteria, change process, roles (including what agents can and cannot do), and how contradictions are handled.

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
