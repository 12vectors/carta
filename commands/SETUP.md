# Carta slash command setup

## 1. Set CARTA_PATH

Tell Claude Code where your Carta knowledge base lives. Add the `env` field to your user-level settings:

```bash
# Edit ~/.claude/settings.json
```

```json
{
  "env": {
    "CARTA_PATH": "/absolute/path/to/my-org-architecture"
  }
}
```

Point CARTA_PATH to your **repository root** — the directory containing `foundations/` and your organisation/team/project levels. The command handles the four-level resolution automatically:

```
my-org-architecture/            # CARTA_PATH points here
├── foundations/                 # Starter knowledge base
│   ├── 10-contexts/
│   ├── 20-patterns/
│   └── ...
├── org/                        # Organisation level
│   ├── overrides/
│   ├── extensions/
│   ├── standards/
│   └── decisions/
├── teams/                      # Team-specific levels
│   └── platform/
│       ├── overrides/
│       ├── extensions/
│       ├── standards/
│       └── decisions/
└── projects/                   # Project-specific levels
    └── payments-api/
        ├── overrides/
        ├── extensions/
        ├── standards/
        └── decisions/
```

## 2. Install the slash commands

Symlink the commands into your user-level Claude Code commands directory:

```bash
mkdir -p ~/.claude/commands
ln -sf /absolute/path/to/carta/commands/carta.md ~/.claude/commands/carta.md
ln -sf /absolute/path/to/carta/commands/carta-add.md ~/.claude/commands/carta-add.md
```

Use the same absolute path you cloned the Carta repo to. The symlinks mean updates to the Carta repo automatically update the commands.

## 3. Use it

From any project, in Claude Code:

```
# Traverse existing content to answer an architectural question
/carta add authentication to the payment service
/carta choose a caching strategy for our product catalog API
/carta should we use event sourcing for order processing

# Draft a new node (loads the writing rules first, then validates)
/carta-add pattern for idempotency keys on payment endpoints
/carta-add antipattern for sharing Postgres tables across services
```

`/carta-add` loads `00-meta/writing-rules.md` into the drafting context so the agent writes terse, directive nodes rather than textbook entries.

## 4. Optional: mention Carta in your project CLAUDE.md

Add a line to your project's CLAUDE.md so the agent knows Carta is available even without the slash command:

```markdown
## Architecture
For non-trivial architectural decisions, use `/carta <task>` to traverse the team's Carta knowledge base before choosing patterns.
```
