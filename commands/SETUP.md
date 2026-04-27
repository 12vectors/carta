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

## 4. Install the git hooks (required for forks pulling upstream)

`INDEX.yaml` at the repo root is fully generated from the content tree. It must stay in sync — the validator fails on drift. Three hooks plus a merge configuration keep it correct without manual work:

| Hook / config | What it does |
|---|---|
| `pre-commit` | Regenerates and stages `INDEX.yaml` when content files are committed. |
| `post-merge` | After a merge from upstream (e.g. `git pull`), regenerates `INDEX.yaml` from the merged source tree and stages it. |
| `post-rewrite` | After a rebase, same regeneration. |
| `merge.ours.driver` git config | Pairs with `.gitattributes`'s `INDEX.yaml merge=ours` line so upstream pulls don't surface a conflict on the index file — the post-merge hook then rebuilds it correctly. |

**Why a fork specifically needs this:** an org's fork accumulates org/team/project content that changes its `INDEX.yaml`; upstream's foundation evolves and changes upstream's `INDEX.yaml`. Without these hooks, every `git pull` from upstream would surface an `INDEX.yaml` merge conflict. With them, the conflict is suppressed (`merge=ours`), the index is rebuilt from the now-merged source files (post-merge hook), and the result reflects both upstream's new foundation entries and the fork's local content.

Install all of the above with one script:

```bash
tools/hooks/install.sh
```

Symlinks the three hooks into `.git/hooks/` and registers `merge.ours.driver true` in this repo's git config. No Python packages beyond what the validator already uses. Idempotent — safe to re-run.

**Via the pre-commit framework:**

If you're already using [pre-commit.com](https://pre-commit.com) for other hooks, a `.pre-commit-config.yaml` ships at the repo root with the same pre-commit behaviour. The post-merge / post-rewrite hooks and the `merge.ours.driver` config still need `tools/hooks/install.sh` (or equivalent manual setup) — pre-commit.com only manages the pre-commit phase.

```bash
pip install pre-commit
pre-commit install
tools/hooks/install.sh   # still needed for post-merge, post-rewrite, merge driver
```

**CI freshness gate (required):** keep `python tools/build_index.py --check` in your CI pipeline. It's the safety net that catches a clone whose hooks didn't fire (GUI git clients can sometimes skip hooks; new contributors may forget to run the installer). The combination of installed hooks + CI check is what makes the merge=ours strategy safe — without the CI check, a hook-less clone could silently ship a stale index.

After a `git pull` that merged upstream changes, you may see `INDEX.yaml` staged in your working tree. Finalise with `git commit --amend --no-edit` (folds the regenerated index into the merge commit) or as a follow-up commit.

## 5. Optional: mention Carta in your project CLAUDE.md

Add a line to your project's CLAUDE.md so the agent knows Carta is available even without the slash command:

```markdown
## Architecture
For non-trivial architectural decisions, use `/carta <task>` to traverse the team's Carta knowledge base before choosing patterns.
```
