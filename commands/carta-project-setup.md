Seed or refresh a project's Carta scope from its own documentation and tech stack.

## When to use this

Use `/carta-project-setup` when:
- Starting a new project that should carry project-level overrides, extensions, standards, and decisions.
- Re-running against an existing `projects/<slug>/` to refresh the charter or tech-stack ADRs after the codebase has drifted.

Use `/carta-add` instead when you want to author one specific Carta node (a single pattern, ADR, standard, etc.) at any level — `/carta-project-setup` is the project-scoped scaffolder, `/carta-add` is the single-node author.

## Find Carta and the target codebase

1. Resolve CARTA_PATH (`echo $CARTA_PATH`). If unset, tell the user to configure it and stop.
2. Parse the target codebase path from the user's invocation. If not provided, default to the current working directory. Confirm with the user if ambiguous.
3. Propose a project **slug** from the target dir name (lowercase, hyphenated). Confirm with the user — the slug becomes the suffix on every project-level file (`.<slug>.md`) and the directory name under `projects/`.

## Check for prior setup

If `CARTA_PATH/projects/<slug>/` already exists, switch to **update flow** (see later section). Otherwise proceed with **fresh setup**.

## Gather evidence from the project

Read what the project has already written about itself and what its manifests reveal. Every later proposal must cite this evidence by `file:line` so the developer can push back against specific lines, not a vibe.

**Documentation to read (if present):**
- `README.md` / `README.rst` / `README.txt`
- `/docs/` recursively; `/architecture/`, `/documentation/` if present
- `CLAUDE.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `GOALS.md`

**Manifests for tech-stack detection:**
- JS/TS: `package.json`, `pnpm-lock.yaml`, `tsconfig.json`
- Python: `pyproject.toml`, `requirements*.txt`, `Pipfile`, `setup.py`
- Go: `go.mod`
- Rust: `Cargo.toml`
- Ruby: `Gemfile`
- Java/Kotlin: `pom.xml`, `build.gradle`, `build.gradle.kts`
- PHP: `composer.json`
- .NET: `*.csproj`, `*.sln`

**Runtime and infra signals:**
- `Dockerfile`, `docker-compose*.yml`
- `k8s/`, `manifests/`, `helm/`, `infra/`
- `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/`
- `.env.example`, top-level `config/` files

**Directory layout:** top-level directory names (is there a backend/frontend split? monorepo? separate services?).

## Propose a profile

Draft a profile based on evidence. Every field cites the line it came from.

- **Slug** — confirmed above.
- **One-liner** — from the README tagline or first paragraph.
- **Context(s)** — match evidence against `CARTA_PATH/DECISION_TREE.md`'s signal table. If a single context fits cleanly, propose it; if multiple overlap (e.g. web application + agentic system), propose all and explain what each covers.
- **Foregrounded pillars** — infer from README emphasis. Uptime/SLA language → reliability. PII/auth/compliance → security. Unit economics or LLM spend → cost. Dev velocity or on-call burden → operational-excellence. p95/throughput → performance.
- **Detected stack** — enumerate languages, frameworks, data stores, message systems, infra, CI — each row cited.
- **Suggested stage** — from operational signals (production docker-compose, multi-env config, on-call runbooks, SLA docs → production; single-file scripts or "experimental" language in the README → prototype). Propose, do **not** decide.

Present the profile to the user. Ask them to correct any line they disagree with.

## Confirm the stage explicitly

Per `00-meta/traversal-protocol.md`, stage is the one thing that must be asked, not inferred. Even after proposing a stage from signals, ask directly: *"Is this project at the prototype, MVP, production, or mission-critical stage?"*

Record both the answer and how it was reached (asked / accepted-proposal) — both go in the charter.

## Scaffold (fresh setup)

Create the project directory tree:

```
CARTA_PATH/projects/<slug>/
├── README.md                 # dev-facing orientation (what this dir is)
├── overrides/
│   └── .gitkeep              # populated when the project disagrees with a foundation pattern
├── extensions/
│   └── .gitkeep              # project-specific patterns not in foundations
├── standards/
│   └── .gitkeep              # project-level concrete standards
└── decisions/
    ├── adr-0001-project-charter.<slug>.md
    └── adr-0002-tech-stack.<slug>.md
```

The `README.md` at the top orients the developer in ~10 lines: what this directory is, how overrides and extensions work, and where to invoke `/carta` and `/carta-review` scoped to this project. Keep it terse — pointers, not documentation.

## Draft ADR-0001 — Project charter (status: proposed)

The charter captures the project's scope, matched contexts, declared stage, and foregrounded pillars in one place. Status is `proposed` — the developer reviews and flips to `accepted`, or edits and then flips.

File: `CARTA_PATH/projects/<slug>/decisions/adr-0001-project-charter.<slug>.md`

Frontmatter (the `stage:` and `pillars:` fields live here so the traversal reads them in one place — see **Stage storage** below). All cross-references use `[[...]]` wikilink syntax so `build_index.py` resolves them into the charter's entry in `INDEX.yaml`:

```yaml
---
id: adr-0001-project-charter
type: adr
level: project
status: proposed
date: <today, ISO>
affects:
  - "[[<each matched context id>]]"
stage: "[[stage-<confirmed>]]"
pillars:
  - "[[pillar-<foregrounded pillar 1>]]"
  - "[[pillar-<foregrounded pillar 2>]]"
---
```

The index picks up `stage` and `pillars` automatically once this command's schema changes are in place (both keys are registered in `WIKILINK_FIELDS` and `WIKILINK_SCALAR_FIELDS`). A traversal can therefore read a project's stage from `entries[adr-0001-project-charter.<slug>].stage` without opening the ADR body.

Body (the ADR schema requires `## Context`, `## Decision`, `## Consequences`):

- **## Context** — one paragraph, sourced from the README. What the project does, who uses it, what problem it solves. Cite the README line range.
- **## Decision** — the scope declaration: slug, contexts, stage (with how it was determined), pillars, one-line non-goals if extractable. Every anchor cites the README line that supports it. Contradictions with evidence are flagged, not hidden.
- **## Consequences** —
  - Traversals under this project auto-scope to `context_to_patterns[<matched-ctx>]` plus any project-level overrides/extensions.
  - Severity in reviews is calibrated to the declared stage.
  - Relaxations of foundation standards require a further ADR in this directory.

**Stage storage.** The stage lives in the charter ADR's `stage:` frontmatter field rather than a separate `stage.<slug>.md` file — one source of truth, read by the traversal alongside every other ADR frontmatter field. (This is the "equivalent convention" the traversal-protocol leaves open.)

## Draft ADR-0002 — Tech stack (status: proposed)

Records the languages, frameworks, data stores, and infra the project runs on today, with a citation against every claim. Status is `proposed` — the developer reviews and accepts, or edits where the scan got something wrong.

File: `CARTA_PATH/projects/<slug>/decisions/adr-0002-tech-stack.<slug>.md`

Frontmatter:

```yaml
---
id: adr-0002-tech-stack
type: adr
level: project
status: proposed
date: <today, ISO>
affects:
  - "[[<pattern implied by the stack, e.g. pattern-rest-api if a REST framework is detected>]]"
related:
  - "[[<any org or team ADR that binds this choice, e.g. adr-0001-fastapi-as-default>]]"
---
```

Body:

- **## Context** — one paragraph naming the source of every claim (detected from manifests + Dockerfile + compose + CI, etc.). Call out explicitly that this ADR documents *reality as found*, not a choice-after-debate — the developer accepts it (thereby blessing the stack), rewrites it, or ignores it.
- **## Decision** — a markdown table: `| Component | Choice | Evidence |`. Rows for language, framework, data store, cache, message broker, infra, CI, testing. Every row cites the manifest or config file:line that names it. Leave rows blank rather than guess.
- **## Consequences** —
  - **Org/team ADRs that bind** — read `affects_to_adrs` for each affected pattern; list any ADR whose constraints the detected stack must honour (e.g. if the org has `adr-fastapi-as-default` and the project uses FastAPI, note the conformance; if the project uses Flask instead, flag it as a deviation requiring a further ADR).
  - **Standards triggered** — from `context_to_standards[<matched-ctx>]`, any standard the detected stack immediately brings into scope.
  - **Antipattern risks** — from `context_to_antipatterns[<matched-ctx>]`, any antipattern the stack combination could trigger.
  - **Open questions** — items the scan couldn't resolve (e.g. "Redis detected in `docker-compose.yml:22` — used as cache, queue, or both?"). These are for the developer to answer before `accepted`.

## Update flow (project dir already exists)

If `CARTA_PATH/projects/<slug>/` exists, do not overwrite silently. Instead:

1. Read the existing `decisions/adr-0001-project-charter.<slug>.md` and `decisions/adr-0002-tech-stack.<slug>.md` (if present). Note each ADR's current `status:`.
2. Re-run the evidence pass on the current codebase.
3. Diff evidence-now against the ADR's recorded state:
   - **Charter**: has the context changed? Stage? Pillars? Have README signals shifted?
   - **Tech stack**: has the language, framework, data store, or infra changed? New dependencies in the manifests? Services added or removed from compose?
4. For each ADR, act based on status:
   - **`status: proposed`** — the ADR hasn't been blessed yet, so it's free to update in place. Produce a unified diff, show it to the developer, ask accept/reject/edit per change.
   - **`status: accepted`** — the ADR is immutable. Do not touch it. If the evidence has drifted materially, draft a *new* ADR (`adr-000N-tech-stack-update.<slug>.md` or `adr-000N-charter-revision.<slug>.md`) with `status: proposed`, `supersedes: [[adr-000M-...]]` in frontmatter, and a body explaining what changed. The previous ADR gets `superseded_by:` added (which the validator enforces bidirectionally).
5. Report drift explicitly: *"Charter says stage = mvp; codebase now shows production signals (SLA docs, on-call runbook, prod docker-compose). Propose a charter-revision ADR?"*
6. Never remove or silently overwrite `accepted` ADRs.

## Validate

From CARTA_PATH, run:

```bash
python tools/validate.py --root .
python tools/lint.py --root .
```

Fix validation errors and re-run until clean. For lint warnings, surface each to the developer — some will be intentional (the tech-stack ADR's Decision table is long because real stacks are long, and that may be worth keeping).

Re-regenerate `INDEX.yaml` if it's stale (the pre-commit hook normally handles this; if the validator complains, run `python tools/build_index.py`).

## Report

Summarise for the developer:

- **Files created / updated** — with paths. Distinguish new from modified.
- **Profile proposed** — slug, contexts, stage, pillars, stack.
- **Open questions** — things the scan couldn't resolve (e.g. "Redis: cache or queue?") that the developer should answer before flipping the ADRs to `accepted`.
- **Drift flagged** (update flow only) — each material change, with the ADR supersession it recommends.
- **Next steps**:
  1. Review both ADRs; edit where the scan got something wrong; flip to `status: accepted`.
  2. Run `/carta <task>` scoped to this project to get a starter pattern list for the declared context and stage.
  3. Run `/carta-review <target-path>` for a full multi-pass audit now that the project scope is declared.

Do not commit. The developer curates.

## Task

$ARGUMENTS
