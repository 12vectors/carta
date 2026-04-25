# Carta

**A shared architectural knowledge base for teams building software with coding agents.**

Carta ships with a starter set of patterns, contexts, and antipatterns curated from established sources. Your team extends it with your own standards, decisions, and overrides. Agents do the writing under your direction; you curate. Everyone — humans and agents — reads from the same graph.

---

## Why Carta

Coding agents are capable but architecturally rootless. They produce locally-correct code that ignores team conventions, re-invents patterns you've already rejected, and makes silent choices where explicit ones are needed. Teams solve this with CLAUDE.md files, prompts, wikis, or RAG over docs — but none of these compound. Each answer is re-derived. Cross-references aren't kept. Decisions quietly drift.

Carta is the missing piece: a durable, versioned knowledge base your team (and your agents) share.

- **For developers.** A curated reference of architectural patterns with sources, trade-offs, and real "when NOT to use" guidance. Intermediate engineers learn from it. Senior engineers argue with it. It's the team's accumulated wisdom, browsable in Obsidian.
- **For agents.** A deterministic graph they can traverse before making architectural choices. No more re-deriving the same answer from scratch.

It compounds. Cross-references are already there. Contradictions have already been flagged. The synthesis already reflects every decision your team has made.

## How it works

Carta is plain markdown in a git repository. Two axes structure it:

**The four-level model** — specificity:

- **Foundations** — a starter knowledge base of generic, sourced content. Ships with Carta.
- **Organisation** — your org's overrides, extensions, concrete standards, and decisions.
- **Team** — team-specific customisation within the org.
- **Project** — project-specific customisation, for when a particular system needs its own choices.

Each more specific level can override or extend the level above it. The only constraint is that overrides are accompanied by a decision record explaining why.

**Tech stacks live at organisation level**, never in foundations. A stack commitment is captured as an ADR (the *why*) paired with overrides on the foundation patterns it touches (the *how*) — the seeded `adr-0001-fastapi-as-default.org` + `pattern-rest-api.org` shows the shape. Foundations stay framework- and library-agnostic so the shared layer ages slowly while concrete library choices accumulate as you descend the levels.

**The foundation layers** — what the shared knowledge base contains:

- `05-pillars/` — quality lenses (reliability, security, cost, operational-excellence, performance). What a task is *optimising for*.
- `10-contexts/` — system archetypes (web app, internal tool, agentic system, data pipeline, …). What the system *is*.
- `12-stages/` — operational ambition (prototype, mvp, production, critical). What the system is *aiming to be right now*.
- `15-principles/` — cross-cutting design heuristics (design-for-failure, minimize-coordination, observe-before-optimising, …). How to *approach* a problem.
- `20-patterns/` — reusable patterns, split into `styles/` (system shapes), `tactics/<concern>/` (communication, data, resilience, security, etc.), and `integration/` (messaging, routing, transformation). What to *build*.
- `25-decision-trees/` — selection guides between alternative patterns (REST vs GraphQL, saga vs 2PC, monolith vs microservices, …).
- `30-solutions/` — pre-composed combinations of patterns for recurring problems.
- `40-standards/` — meta-standards and templates (opinionated standards live at org level, not here).
- `50-antipatterns/` — recurring failure modes with fixes.

A traversal consults these layers in order: pillars frame the trade-offs, contexts + stage scope the candidate set, principles provide the heuristics, patterns are the buildings blocks, decision-trees pick between alternatives, solutions offer pre-composed combinations.

**Agents write, humans curate.** Nobody expects developers to write 500-word architectural patterns from scratch. The workflow is: you direct an agent to draft a node, review what it produces, edit for accuracy and team fit, commit. The tedious writing is automated. The judgement stays with the team.

For the full technical picture — schema, traversal algorithm, operations — see [`00-meta/overview.md`](00-meta/overview.md).

## Design principles

1. **Curated, not retrieved.** Carta is a persistent, compounding artefact. Knowledge is synthesised once and kept current — not re-derived on every query.
2. **For humans and agents both.** Carta is as much a team reference as an agent input. Intermediate engineers learn from it; senior engineers refine it; agents traverse it.
3. **Human-curated, agent-authored.** People make the judgements and decisions. Agents draft the prose, propagate changes across the graph, and check consistency. Neither does the other's work.
4. **Decisions are first-class.** Patterns explain *what*; ADRs explain *why this one, here, now*.
5. **Grounded in evidence.** Patterns cite their sources. Assertions without provenance are flagged during lint.
6. **Contradictions are explicit.** When new decisions conflict with existing patterns, the conflict is flagged and linked — never silently overwritten.
7. **Four-level model, cleanly separated.** Foundations are shared; organisation, team, and project levels are yours.
8. **Transparency over rigidity.** Any level can override any other level — the constraint is that overrides are documented, not that they're forbidden.
9. **Traversal is deterministic.** Agents follow a documented algorithm, not vibes.
10. **Obsidian-native, works as plain markdown elsewhere.** The graph view, backlinks, and wikilinks make Obsidian the recommended way to explore Carta. The files themselves are plain markdown that renders on GitHub and parses in any editor.

## Quickstart

From zero to a first traversal in about 10 minutes:

```bash
# 1. Fork this repo, then clone your fork
git clone https://github.com/<your-org>/carta.git my-org-architecture
cd my-org-architecture

# 2. Open the repository root as an Obsidian vault
#    Obsidian → Open folder as vault → select my-org-architecture/
#    (See 00-meta/obsidian-setup.md for plugin configuration)

# 3. Point Claude Code at Carta and install the slash commands
#    - Set CARTA_PATH in ~/.claude/settings.json → env
#    - Symlink the four commands into ~/.claude/commands/
#    Full instructions: commands/SETUP.md
```

### The four Claude Code slash commands

| Command | When to use | What it does |
|---|---|---|
| `/carta <question>` | Quick architectural question, no codebase read required | Single-response traversal: matches contexts, pillars, stage; returns recommended patterns with rationale and citations. |
| `/carta-review <path>` | Auditing an existing codebase against Carta | Spawns a Claude Code subagent that iterates through the 13-step protocol in passes (up to four), reads code files to back every finding with `file:line` evidence, returns a structured scorecard. Read-only. |
| `/carta-project-setup <path>` | Seeding or refreshing a project's Carta scope | Reads the target project's README, docs, and manifests; proposes a profile (slug, context, stage, pillars, detected stack) with `file:line` citations; scaffolds `projects/<slug>/` with a charter ADR and a tech-stack ADR (`status: proposed`). Re-runnable — drifted `accepted` ADRs are superseded, never overwritten. |
| `/carta-add <node description>` | Authoring a new node | Loads writing rules and the matching template, drafts a terse node, runs validator and linter. Review, edit, commit. |

### First traversal

```
# In Claude Code, from any project:
/carta choose a caching strategy for our product catalog API
```

On the first run the agent will ask for the system's operational **stage** — `prototype`, `mvp`, `production`, or `critical`. Answer honestly; severity in the report is relative to that stage.

### First review

```
/carta-review ./backend
```

`/carta-review` is the deeper counterpart. It spawns a general-purpose subagent — with its own context budget — to multi-pass through your codebase, pairing every pattern-level finding with a `file:line` citation from the actual code. Use this when `/carta`'s single response isn't enough to audit a real application.

### First authored node

If the traversal surfaces a gap — a pattern your team uses but hasn't written down, a standard you've agreed but haven't captured — use `/carta-add` to author:

```
/carta-add pattern for idempotency keys on payment endpoints
```

`/carta-add` loads the writing rules and the matching template (one for each of the ten node types: pattern, antipattern, standard, solution, context, adr, pillar, principle, decision-tree, stage), drafts a terse, directive node, and runs the validator and linter before handing off for review. Edit, commit. That's the loop.

The fuller walkthrough, including a worked example of adding your first org-level override, is in [`00-meta/quickstart.md`](00-meta/quickstart.md).

## Status

Pre-1.0. APIs, schemas, and directory conventions may change.

| Component | Status |
|---|---|
| Node schema and four-level model | Working |
| Operations model (traverse, ingest, lint, capture) | Working |
| Slash commands — `/carta` (traverse), `/carta-review` (deep codebase audit via subagent), `/carta-project-setup` (scaffold a project's Carta scope), `/carta-add` (author one node) | Working |
| Validator (`tools/validate.py`) and linter (`tools/lint.py`) | Working |
| Foundations — pillars (5), contexts (7), stages (4), principles (14), patterns (97), decision-trees (6), solutions (1), antipatterns (10) | Seeded — 152 nodes |
| Obsidian setup guide and templates (10 node types) | Done |
| Spec Kit integration example | Planned |

## Further reading

- [`00-meta/overview.md`](00-meta/overview.md) — the full technical picture: structure, schema, operations.
- [`00-meta/quickstart.md`](00-meta/quickstart.md) — hands-on guide, 10 minutes to first traversal.
- [`CHARTER.md`](CHARTER.md) — governance of the foundations: admission criteria, contradictions, promotion.
- [`00-meta/glossary.md`](00-meta/glossary.md) — canonical terminology. Use this when authoring.
- [`00-meta/node-schema.md`](00-meta/node-schema.md) — the normative frontmatter contract.
- [`00-meta/writing-rules.md`](00-meta/writing-rules.md) — voice, length, and bullet rules. Soft-enforced by `tools/lint.py`.

## License

The Carta foundations are released under the MIT License. Your organisation, team, and project levels are yours; nothing in this license requires you to publish them.

## Credits

The name draws on the Latin *charta* — a written charter that constrains and enables, referred to and amended over time. The operations model (traverse, ingest, lint, capture) adapts ideas from Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. The ADR format follows Michael Nygard's [convention](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
