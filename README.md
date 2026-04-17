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

Carta is plain markdown in a git repository, structured as a four-level model:

- **Foundations** — a starter knowledge base of generic, sourced patterns. Ships with Carta.
- **Organisation** — your org's overrides, extensions, concrete standards, and decisions.
- **Team** — team-specific customisation within the org.
- **Project** — project-specific customisation, for when a particular system needs its own choices.

Each more specific level can override or extend the level above it. The only constraint is that overrides are accompanied by a decision record explaining why.

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

# 3. Install the /carta slash command for Claude Code
#    Set CARTA_PATH and symlink the command — see commands/SETUP.md

# 4. Try a traversal against a real architectural question
#    In Claude Code, from any project:
/carta choose a caching strategy for our product catalog API
```

If the traversal surfaces gaps in Carta — a pattern your team uses but hasn't written down, a standard you've agreed but haven't captured — that's your cue to author. Ask an agent:

```
Draft a pattern node for <X> following the schema in 00-meta/node-schema.md.
Place it in <the appropriate directory>. Cite verifiable sources.
```

Review, edit, commit. That's the loop.

The fuller walkthrough, including a worked example of adding your first org-level override, is in [`00-meta/quickstart.md`](00-meta/quickstart.md).

## Status

Pre-1.0. APIs, schemas, and directory conventions may change. The foundations are incomplete — we ship with a scenario covering one context (web application) and a handful of patterns to demonstrate the model. Expanding the foundations is ongoing work.

| Component | Status |
|---|---|
| Node schema and four-level model | Draft |
| Operations model (traverse, ingest, lint, capture) | Draft |
| Traversal slash command | Working |
| Validator (`tools/validate.py`) | Working |
| Linter (`tools/lint.py`) | Working |
| Foundations (patterns, contexts, antipatterns) | In progress — ~14 nodes |
| Obsidian setup guide and templates | Done |
| Spec Kit integration example | Planned |

## Further reading

- [`00-meta/overview.md`](00-meta/overview.md) — the full technical picture: structure, schema, operations.
- [`00-meta/quickstart.md`](00-meta/quickstart.md) — hands-on guide, 10 minutes to first traversal.
- [`CHARTER.md`](CHARTER.md) — governance of the foundations: admission criteria, contradictions, promotion.
- [`00-meta/glossary.md`](00-meta/glossary.md) — canonical terminology. Use this when authoring.
- [`00-meta/node-schema.md`](00-meta/node-schema.md) — the normative frontmatter contract.

## License

The Carta foundations are released under the MIT License. Your organisation, team, and project levels are yours; nothing in this license requires you to publish them.

## Credits

The name draws on the Latin *charta* — a written charter that constrains and enables, referred to and amended over time. The operations model (traverse, ingest, lint, capture) adapts ideas from Andrej Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern. The ADR format follows Michael Nygard's [convention](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
