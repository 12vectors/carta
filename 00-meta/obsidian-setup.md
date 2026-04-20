# Obsidian Setup

Carta is plain markdown that works in any editor. Obsidian is optional but recommended for exploring the graph, reviewing relationships, and authoring new nodes.

This guide walks through setting up Carta as an Obsidian vault. It takes a few minutes.

---

## Open the vault

Open your Carta repository root as an Obsidian vault. This is the directory that contains `foundations/`, `org/`, `teams/`, `projects/`, etc. — not the `foundations/` subdirectory itself.

1. Open Obsidian.
2. **Open folder as vault** → select the repository root.
3. When prompted to trust plugins, accept.

Opening the root ensures Obsidian sees all four levels — foundations, organisation, teams, and projects — in a single graph. Wikilinks resolve across all of them.

## Install community plugins

Go to **Settings → Community plugins → Browse** and install:

1. **Dataview** — powers the live index queries in `INDEX.md`. After installing, enable it. Default settings work fine.
2. **Templater** — scaffolds new nodes with valid frontmatter. After installing:
   - Go to **Settings → Templater → Template folder location**.
   - Set it to `templates`.
   - Enable **Trigger Templater on new file creation** if you want templates applied automatically.

## Configure graph view colours

Open the graph view (**Ctrl/Cmd + G**) and expand the **Groups** section. Add these colour groups to distinguish node types at a glance:

| Query | Colour | Node type |
|-------|--------|-----------|
| `tag:#context` | Orange | Contexts |
| `tag:#pattern` | Blue | Patterns |
| `tag:#solution` | Purple | Solutions |
| `tag:#standard` | Green | Standards |
| `tag:#antipattern` | Red | Antipatterns |
| `tag:#adr` | Grey | ADRs |

Choose whatever colours you prefer — the queries are what matter. They match the `tags` field in each node's frontmatter.

Alternatively, copy this into `.obsidian/graph.json` (close Obsidian first, then reopen):

```json
{
  "collapse-filter": false,
  "search": "",
  "showTags": false,
  "showAttachments": false,
  "hideUnresolved": false,
  "showOrphans": true,
  "collapse-color": false,
  "colorGroups": [
    { "query": "tag:#context", "color": { "a": 1, "rgb": 15105570 } },
    { "query": "tag:#pattern", "color": { "a": 1, "rgb": 4886745 } },
    { "query": "tag:#solution", "color": { "a": 1, "rgb": 10181046 } },
    { "query": "tag:#standard", "color": { "a": 1, "rgb": 3066993 } },
    { "query": "tag:#antipattern", "color": { "a": 1, "rgb": 15158332 } },
    { "query": "tag:#adr", "color": { "a": 1, "rgb": 9807270 } }
  ],
  "collapse-display": false,
  "lineSizeMultiplier": 1,
  "nodeSizeMultiplier": 1,
  "collapse-forces": false,
  "centerStrength": 0.5,
  "repelStrength": 10,
  "linkStrength": 1,
  "linkDistance": 250,
  "scale": 1
}
```

## Recommended settings

In **Settings → Editor**:

- **Default editing mode** → Source mode or Live Preview (your preference).
- **Properties in document** → Visible. Frontmatter is the graph — you want to see it.

In **Settings → Files & Links**:

- **Use [[Wikilinks]]** → On (should be default).
- **New link format** → Shortest path when possible.

## Using templates

To create a new node:

1. Create a new file in the appropriate directory (e.g. `foundations/20-patterns/tactics/resilience/` for a foundation resilience pattern, or `org/extensions/` for an org-specific pattern).
2. Open the command palette (**Ctrl/Cmd + P**) → **Templater: Insert template**.
3. Select the template for the node type you're creating (e.g. `tpl-pattern`).
4. Fill in the frontmatter fields and body sections.
5. Rename the file to match the `id` field (e.g. `pattern-circuit-breaker.md`).

Templates are in `templates/`. They match the schema defined in `00-meta/node-schema.md`.

## What's in `.obsidian/`

The `.obsidian/` directory is gitignored. It contains Obsidian's local working state — your workspace layout, plugin installs, and settings. It's created automatically when you open the vault and belongs to your local environment, not the repo.

## All levels in one vault

Always open the repository root as the vault. This gives Obsidian visibility into all four levels:

- `foundations/` — the shared starter knowledge base
- `org/` — organisation-level overrides, extensions, standards, and decisions
- `teams/<team>/` — team-level overrides, extensions, standards, and decisions
- `projects/<project>/` — project-level overrides, extensions, standards, and decisions

The graph view will show connections across all levels. Wikilinks resolve across boundaries — a project decision can reference a foundation pattern, and Obsidian will render the link.
