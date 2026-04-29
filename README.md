# Carta

**Coding agents don't know how *your team* builds software. Carta gives them the map.**

Carta is plain markdown in a Git repo: an architectural knowledge graph — patterns, principles, decisions, antipatterns — curated by your team and read deterministically by your coding agents. Open it in any markdown reader (we like Obsidian); point Claude Code at the directory; humans and agents read the same files.

Your team curates the map. Your agents traverse it — spending tokens on the work, not redrawing what your team has already settled. The map gets sharper with every commit.

---

## Why Carta — and not a config file, a wiki, or RAG

Out of the box, your coding agent doesn't know how your team builds software. Teams patch the gap in a few ways. Each handles a slice of the problem; none handle all of it.

|                                                       | `agent.md` / `CLAUDE.md` | Wiki | RAG over docs | **Carta** |
|---|:-:|:-:|:-:|:-:|
| Scales past one file                                  | ✗ | ✓ | ✓ | ✓ |
| Compounds across the org with every commit           | ✗ | ~ | ✗ | ✓ |
| Token-efficient — loads only what the query needs    | ✗ | ✗ | ~ | ✓ |
| Cross-referenced, traversable graph                  | ✗ | ~ | ✗ | ✓ |
| Multi-level overrides (org / team / project)         | ✗ | ✗ | ✗ | ✓ |
| Sources cited per node                                | ✗ | ✗ | ~ | ✓ |
| Deterministic for agents                              | ✓ | ✗ | ✗ | ✓ |

Carta is the missing layer: a durable, versioned graph that compounds. Cross-references are already there. Contradictions have already been flagged. The synthesis already reflects every decision your team has made.

- **For developers.** A curated reference of architectural patterns with sources, trade-offs, and real "when NOT to use" guidance. Intermediate engineers learn from it. Senior engineers argue with it.
- **For agents.** A deterministic graph they traverse before making architectural choices. No more re-deriving the same answer from scratch.

## How it works

Carta is plain markdown organised on two axes. Each axis exists because of a real problem.

### Architectural truth is contextual → four-level overrides

A 5-second timeout is right for most services and wrong for a payments processor doing 3D Secure. A generic REST shape is right for most teams and wrong if your org has standardised on RFC 7807 and `/v1/` versioning. So Carta is layered by specificity:

- **Foundations** — generic, sourced content shipped with Carta. Framework- and library-agnostic.
- **Organisation** — your overrides, extensions, concrete standards, tech-stack ADRs.
- **Team** — team-specific customisation within the org.
- **Project** — project-specific choices for systems that need their own answers.

Each more local level can override or extend the level above, with an ADR explaining why. Your project's `pattern-circuit-breaker.payments-api` wins; the foundation stays generic. No forks of the foundation; no duplication.

**Tech stacks live at organisation level**, never in foundations. A stack commitment is captured as an ADR (the *why*) paired with overrides on the foundation patterns it touches (the *how*). Foundations age slowly so the shared layer compounds; concrete library choices accumulate as you descend the levels.

### Pattern matching without framing is shallow → foundation layers walked in fixed order

"Should we use CQRS?" depends on what you're optimising for, what kind of system you're building, and what stage you're at. Most agent-knowledge skips the framing and just lists patterns. Carta's foundation has explicit framing layers, walked in order on every traversal:

- `05-pillars/` — quality lenses (reliability, security, cost, operational-excellence, performance). What a task is *optimising for*.
- `10-contexts/` — system archetypes (web app, internal tool, agentic system, data pipeline, …). What the system *is*.
- `12-stages/` — operational ambition (prototype, mvp, production, critical). What the system is *aiming to be right now*.
- `15-principles/` — cross-cutting design heuristics. How to *approach* a problem.
- `20-patterns/` — reusable patterns: `styles/` (system shapes), `tactics/<concern>/` (communication, data, resilience, security, …), `integration/` (messaging, routing, transformation). What to *build*.
- `25-decision-trees/` — selection guides between alternative patterns.
- `30-solutions/` — pre-composed combinations of patterns for recurring problems.
- `40-standards/` — meta-standards and templates.
- `50-antipatterns/` — recurring failure modes with fixes.

Same reasoning shape every traversal: pillars frame the trade-off, contexts + stage scope the candidate set, principles back the patterns, decision-trees pick between alternatives, solutions offer pre-composed combinations.

### Unsourced best-practice is hearsay → every node carries verifiable sources

A pattern recommendation is only as good as its provenance. Without sources you can't check the reasoning, can't tell when something was canonical, and can't update when the source updates. Every Carta node cites at least one canonical source — book chapter, paper with DOI, or article by a recognised authority — with a `Currency` note when the source is older but the pattern is shape-level. The source list is the test for whether a node deserves to exist.

**Agents write, humans curate.** Nobody expects developers to write 500-word patterns from scratch. The workflow is: you direct an agent to draft a node, review what it produces, edit for accuracy and team fit, commit. The tedious writing is automated. The judgement stays with the team.

For the full technical picture — schema, traversal algorithm, operations — see [`00-meta/overview.md`](00-meta/overview.md).

## What's seeded today

A starter foundation that's already useful, ready for your overrides. **144 sourced nodes** across the graph — books, papers with DOIs, canonical articles. Patterns include Cache-Aside, Circuit Breaker, Idempotency Key, Retry with Backoff, Transactional Outbox, CQRS, Saga, and 90 more.

| Kind | Count |
|---|---|
| Patterns | 97 |
| Principles | 14 |
| Antipatterns | 10 |
| Contexts | 7 |
| Decision trees | 6 |
| Pillars | 5 |
| Stages | 4 |
| Solutions | 1 |

Coverage spans communication, data, resilience, scaling, security, observability, deployment, agentic systems, testing, delivery / CI, and frontend.

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
| `/carta-review <path>` | Auditing an existing codebase against Carta | Spawns a Claude Code subagent that iterates the traversal protocol across six passes (with up to four iterations of the candidate-stability loop), pairing every finding with a `file:line` citation from the actual code. Concise by default; ask `verbose` for the full scorecard. Read-only. |
| `/carta-project-setup <path>` | Seeding or refreshing a project's Carta scope | Reads the target project's README, docs, and manifests; proposes a profile (slug, context, stage, pillars, detected stack) with `file:line` citations; scaffolds `projects/<slug>/` with a charter ADR and a tech-stack ADR (`status: proposed`). Re-runnable — drifted `accepted` ADRs are superseded, never overwritten. |
| `/carta-add <node description>` | Authoring a new node | Loads writing rules and the matching template, drafts a terse markdown file (front-matter, decision inputs, when-to-use / when-NOT-to-use, sources), runs validator and linter. You review, edit, commit. |

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

Use this when `/carta`'s single response isn't enough to audit a real application. The report is concise by default; ask "show verbose" or "show every pattern" after the run to expand into the full scorecard with every Present pattern, the principles applied, and the decision trees consulted.

### First authored node

If the traversal surfaces a gap — a pattern your team uses but hasn't written down, a standard you've agreed but haven't captured — use `/carta-add` to author:

```
/carta-add pattern for idempotency keys on payment endpoints
```

The fuller walkthrough, including a worked example of adding your first org-level override, is in [`00-meta/quickstart.md`](00-meta/quickstart.md).

## What it costs to run this

Every knowledge base rots without a curator. Carta's authoring loop is in your normal review workflow — not a parallel system.

- **Who curates.** Whoever owns architectural decisions on your team — usually a tech lead or staff engineer, sometimes a small guild. The role is light: spot a recurring decision (in PR review, in an incident, in a `/carta` answer that didn't quite fit) and turn it into a node. Expect roughly 20 minutes per node, often less.
- **The authoring loop.** `/carta-add` → review → commit. The command loads the matching template, drafts a terse node, and runs the validator and linter. You read it, sharpen it, push it through normal code review. Every node has an author, a diff, and a commit message. No separate publishing step. No separate place to look.
- **Upstream foundations.** Foundations are MIT-licensed and shared. Your fork pulls them in; your `org/`, `teams/`, and `projects/` directories are yours alone. Upstream changes arrive via a regular `git pull`. Conflicts surface in your overrides — exactly where you want a human in the loop.

## Status

Pre-1.0. APIs, schemas, and directory conventions may change.

| Component | Status |
|---|---|
| Node schema and four-level model | Working |
| Operations model (traverse, ingest, lint, capture) | Working |
| Slash commands — `/carta`, `/carta-review`, `/carta-project-setup`, `/carta-add` | Working |
| Validator (`tools/validate.py`) and linter (`tools/lint.py`) | Working |
| Foundations — pillars (5), contexts (7), stages (4), principles (14), patterns (97), decision-trees (6), solutions (1), antipatterns (10) | Seeded — 144 nodes |
| Obsidian setup guide and templates (10 node types) | Done |
| Spec Kit integration example | Planned |

## Further reading

- [`00-meta/overview.md`](00-meta/overview.md) — the full technical picture: structure, schema, operations.
- [`00-meta/quickstart.md`](00-meta/quickstart.md) — hands-on guide, 10 minutes to first traversal.
- [`CHARTER.md`](CHARTER.md) — governance of the foundations: admission criteria, contradictions, promotion.
- [`00-meta/glossary.md`](00-meta/glossary.md) — canonical terminology. Use this when authoring.
- [`00-meta/node-schema.md`](00-meta/node-schema.md) — the normative frontmatter contract.
- [`00-meta/writing-rules.md`](00-meta/writing-rules.md) — voice, length, and bullet rules. Soft-enforced by `tools/lint.py`.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — what we accept upstream, how to propose nodes, the PR checklist.

## License

The Carta foundations are released under the MIT License ([LICENSE](LICENSE)). Your organisation, team, and project levels are yours; nothing in this license requires you to publish them.

## Credits

The name draws on the Latin *charta* — a written charter that constrains and enables, referred to and amended over time. The operations model (traverse, ingest, lint, capture) adapts ideas from Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. The ADR format follows Michael Nygard's [convention](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
