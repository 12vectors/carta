# Obsidian Setup

Carta is plain markdown that works in any editor. Obsidian is optional but recommended for exploring the graph, reviewing relationships, and authoring new nodes.

This guide walks through setting up Carta as an Obsidian vault. It takes a few minutes.

---

## Open the vault

Open the Carta directory (or your organisation overlay root) as an Obsidian vault:

1. Open Obsidian.
2. **Open folder as vault** → select the Carta root directory.
3. When prompted to trust plugins, accept.

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

1. Create a new file in the appropriate directory (e.g. `20-patterns/resilience/`).
2. Open the command palette (**Ctrl/Cmd + P**) → **Templater: Insert template**.
3. Select the template for the node type you're creating (e.g. `tpl-pattern`).
4. Fill in the frontmatter fields and body sections.
5. Rename the file to match the `id` field (e.g. `pattern-circuit-breaker.md`).

Templates are in the `templates/` directory at the repo root. They match the schema defined in `00-meta/node-schema.md`.

## What's in `.obsidian/`

The `.obsidian/` directory is gitignored. It contains Obsidian's local working state — your workspace layout, plugin installs, and settings. It's created automatically when you open the vault and belongs to your local environment, not the repo.

## Organisation overlays

If your overlay includes the Carta core as a submodule (`carta/`), open the **overlay root** as the vault, not the `carta/` subdirectory. This way Obsidian sees both core and overlay nodes in the same graph, and wikilinks resolve across both.
