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
│   ├── 05-pillars/              # Quality lenses (reliability, security, cost, op-ex, performance)
│   ├── 10-contexts/             # System archetypes
│   ├── 12-stages/               # Operational ambition (prototype, mvp, production, critical)
│   ├── 15-principles/           # Cross-cutting design heuristics
│   ├── 20-patterns/             # styles/, tactics/<concern>/, integration/
│   ├── 25-decision-trees/       # Selection guides between alternative patterns
│   ├── 30-solutions/            # Composed patterns
│   ├── 40-standards/            # Meta-standards and templates
│   └── 50-antipatterns/
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
ln -sf /absolute/path/to/carta/commands/carta-review.md ~/.claude/commands/carta-review.md
ln -sf /absolute/path/to/carta/commands/carta-project-setup.md ~/.claude/commands/carta-project-setup.md
```

Use the same absolute path you cloned the Carta repo to. The symlinks mean updates to the Carta repo automatically update the commands.

## 3. Use it

From any project, in Claude Code:

```
# Light traversal — single-response, no codebase audit required
/carta add authentication to the payment service
/carta choose a caching strategy for our product catalog API
/carta should we use event sourcing for order processing

# Deep review — multi-pass audit of an existing codebase (spawns a subagent)
/carta-review ./backend
/carta-review /path/to/my-service
/carta-review                      # defaults to current working directory

# Draft a new node (loads the writing rules first, then validates)
/carta-add pattern for idempotency keys on payment endpoints
/carta-add antipattern for sharing Postgres tables across services

# Seed (or refresh) a project's Carta scope from its docs and tech stack
/carta-project-setup ./backend
/carta-project-setup /path/to/new-service
```

`/carta` is for conversational architectural questions — one response, no file crawling of the target codebase. `/carta-review` is for auditing an existing application: it spawns a subagent that iterates (up to four passes) through the candidate set, reads code files to back every finding with `file:line` evidence, and terminates when the set is stable. Use `/carta-review` when you want every recommended pattern backed by code citations. The default report is concise (top issues + status-grouped findings, empty sections collapsed); ask `verbose` or "show every pattern" after the run to see the full scorecard. `/carta-add` loads `00-meta/writing-rules.md` into the drafting context so the agent writes terse, directive nodes rather than textbook entries. `/carta-project-setup` is the project-scoped scaffolder: it reads the target project's README, docs, and manifests, proposes a matching profile (slug, context, stage, pillars, detected stack) with `file:line` citations the developer can push back against, and writes a charter ADR and a tech-stack ADR under `projects/<slug>/decisions/` with `status: proposed` for review. Re-run it to refresh after the codebase drifts — `accepted` ADRs are never rewritten, only superseded.

## 4. Install the pre-commit hook (optional but recommended)

`INDEX.yaml` at the repo root must stay in sync with the content tree — the validator fails on drift. A pre-commit hook regenerates it automatically whenever you commit a change to content (under `foundations/`, `org/`, `teams/`, or `projects/`).

Two ways to install:

**Dependency-free (recommended):**

```bash
tools/hooks/install.sh
```

Symlinks `tools/hooks/pre-commit` into `.git/hooks/pre-commit`. No Python packages beyond what the validator already uses.

**Via the pre-commit framework:**

If you're already using [pre-commit.com](https://pre-commit.com) for other hooks, a `.pre-commit-config.yaml` ships at the repo root with the same behaviour:

```bash
pip install pre-commit
pre-commit install
```

Either approach regenerates and stages `INDEX.yaml` in the same commit as the content change. Skip this step entirely if you're comfortable running `python tools/build_index.py` by hand — the validator will tell you when you've forgotten.

## 5. Optional: mention Carta in your project CLAUDE.md

Add a line to your project's CLAUDE.md so the agent knows Carta is available even without the slash command:

```markdown
## Architecture
For non-trivial architectural decisions, use `/carta <task>` to traverse the team's Carta knowledge base before choosing patterns.
```
