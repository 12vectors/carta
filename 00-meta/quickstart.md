# Quickstart

From zero to a working Carta traversal in roughly 10 minutes. This guide assumes you have Claude Code installed and a GitHub account.

---

## Step 1 — Fork and clone (2 min)

Fork the Carta repository on GitHub, then clone your fork:

```bash
git clone https://github.com/<your-org>/carta.git my-org-architecture
cd my-org-architecture
```

Rename the directory to whatever reflects your organisation — this repo *is* your organisation's architectural knowledge base. You'll extend `org/`, `teams/`, and `projects/` over time.

## Step 2 — Open in Obsidian (2 min)

Obsidian is optional but recommended. It renders the graph, resolves wikilinks across all four levels, and gives you a proper authoring environment.

1. Open Obsidian.
2. **Open folder as vault** → select the repository root (not a subdirectory).
3. When prompted to trust plugins, accept.
4. Install the **Dataview** and **Templater** community plugins. See [`obsidian-setup.md`](obsidian-setup.md) for graph colours and other recommended settings.

Opening the root gives Obsidian visibility into all levels at once — foundations, org, teams, projects. Wikilinks resolve across boundaries.

## Step 3 — Install the slash command (2 min)

The `/carta` slash command runs a traversal from any project in Claude Code.

Edit `~/.claude/settings.json` to point at your Carta repo:

```json
{
  "env": {
    "CARTA_PATH": "/absolute/path/to/my-org-architecture"
  }
}
```

Symlink the command into your user-level Claude Code commands directory:

```bash
mkdir -p ~/.claude/commands
ln -sf /absolute/path/to/my-org-architecture/commands/carta.md ~/.claude/commands/carta.md
```

Full slash command setup is in [`commands/SETUP.md`](../commands/SETUP.md).

## Step 4 — Run your first traversal (2 min)

From any project in Claude Code:

```
/carta choose a caching strategy for our product catalog API
```

On the first run the agent will **ask you what operational stage the system is at** — `prototype`, `mvp`, `production`, or `critical`. That answer determines severity in the report: "no auth" is an urgent finding for a production API and an acceptable compromise for a localhost prototype. Do not guess on the agent's behalf; reply honestly. See `foundations/12-stages/` for what each stage means.

The agent will then:

1. Match your task against `DECISION_TREE.md` to find the relevant context(s) and identify the pillars the task is optimising for.
2. Read `foundations/10-contexts/` to get recommended patterns; confirm the stage's baselines.
3. Walk the four-level model — checking `projects/`, `teams/`, `org/`, `foundations/` — to resolve overrides.
4. Filter and demote patterns by `stage_floor` relative to your stage.
5. Consult decision trees when candidate patterns overlap, cross-reference standards and antipatterns, check ADRs.
6. Report what matches the current stage, what's deferred to later stages, and what's missing.

Carta ships with a worked example covering the `context-web-application` context and a payments-api project. See `foundations/10-contexts/context-web-application.md` and `projects/payments-api/` for the full scenario.

## Step 5 — Author your first node (a few minutes)

The traversal will often surface gaps — patterns your team uses but hasn't written down, standards you've agreed but haven't captured. This is the authoring loop.

Suppose the traversal reported that `pattern-rate-limiting` doesn't exist at the org level. Ask an agent:

```
Draft an org-level pattern node for rate limiting, following the schema
in 00-meta/node-schema.md. Place it at org/extensions/pattern-rate-limiting.org.md.
Cite verifiable sources. Use the tpl-pattern.md template.
```

The agent produces a draft with frontmatter, "When to use" / "When NOT to use" sections, and real sources (a blog post, a chapter from Release It!, etc.).

Your job now:

- **Review** — does the content match how your team actually does rate limiting?
- **Edit** — change anything that's wrong or off-tone for your team.
- **Verify sources** — the agent will cite real references, but check they say what the draft claims.
- **Commit** — `git add` and commit the reviewed node.

Run `python tools/validate.py` to check schema compliance. If it passes, you're done.

## Step 6 — What to do next

- **Browse the foundations.** Open `foundations/` in Obsidian and look at what's there. The graph view shows connections.
- **Read [`CHARTER.md`](../CHARTER.md)** if you're going to contribute to the foundations themselves (not just extend them for your org).
- **Plan your org level.** Identify 3–5 patterns or standards your team has strong opinions on and direct an agent to draft nodes for them.
- **Set up CI.** Add `tools/validate.py` to your CI pipeline to block PRs with broken frontmatter or wikilinks.
- **Run [`tools/lint.py`](../tools/lint.py)** periodically to catch orphan nodes, missing pages, and stale sources.

## The authoring loop in summary

1. Run `/carta` on a real task.
2. If it finds gaps, ask an agent to draft the missing nodes.
3. Review, edit, verify sources.
4. Commit.

Repeat. The knowledge base compounds. Every traversal makes it better.

## Troubleshooting

**"No context matches my task."** The signal table in `DECISION_TREE.md` may not cover your system type. Run the traversal anyway — the agent will proceed pattern-by-pattern — and consider adding a new context.

**"Wikilinks don't resolve in Obsidian."** You probably opened a subdirectory as the vault instead of the repository root. Close the vault and reopen the root.

**"The foundations are too thin."** They are, intentionally — the foundations ship minimal by design and grow through promotion from organisation, team, and project levels. Expanding them is ongoing work; contributions welcome.

**"Agent drafts are generic."** Give the agent more context. Point it at existing nodes as style references (`Use foundations/20-patterns/tactics/resilience/pattern-circuit-breaker.md as a template`). Tell it your stack.
