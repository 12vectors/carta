# Carta TODO

Things we want to add to Carta — content gaps, tooling, schema changes, integrations. This is a working list, not a roadmap. Items move to `LOG.md` (or just disappear) when they land.

Order within each section is rough priority, most useful first. Feel free to rearrange.

---

## Agent and review UX

### Verbose vs concise review reports
The `/carta-review` subagent produces a comprehensive structured report — pattern scorecard with file:line citations, deferred-to-stage groups, pillars and principles, decision trees consulted, "Gaps in Carta itself". It's thorough, and it can be overwhelming on first read. A real team wants two modes:

- **Concise** (default for casual review): two-sentence lead + top-5 current-stage findings with one-line rationales + the "Gaps in Carta itself" section. No full scorecard. Maybe 30–50 lines.
- **Verbose** (default for audit or when the concise run surfaces something worth drilling into): today's full report.

Open questions:
- Do we add a `--mode=concise|verbose` style argument to `/carta-review`, or is it a follow-up question the parent asks after the subagent returns?
- Does the subagent always produce the verbose report internally and the parent trims for display, or does the subagent change behaviour? The former is probably right — the subagent's cost doesn't change, and the user can always ask for the full report.
- Should the report structure itself be redesigned so "concise" is a natural subset (e.g. every section has a headline the concise mode quotes, and the rest is collapsible detail)?

### Follow-up offers after a review
The existing "Pick a, b, or c" footer works but could be smarter — e.g. pre-populate the top-5 action list, or offer to draft the Carta-gap fixes as a standalone command. Consider whether `/carta-review-followup <n>` makes sense, or whether it's just better conversation UX.

### Stream long reviews
A 7-minute subagent run with no visible progress is uncomfortable. Look into the Monitor tool or periodic pass-boundary markers the subagent emits (e.g. "Pass 2 complete — 23 candidates identified") that the parent relays while the subagent works.

---

## Foundation content gaps

Surfaced by earlier reviews and the vanilla-reviewer comparison. Ordered by how often they came up in practice.

### Frontend tactics
Zero foundation coverage today. Vanilla code reviewers find multiple issues per review that Carta can't speak to: component-size heuristics, state-management patterns, error boundaries, rendering strategies (SSR/SSG/CSR), form handling, accessibility floors, bundle size. Likely shape: a `tactics/frontend/` folder with ~10 patterns, sourced from MDN, Kent C. Dodds' Epic React, React Patterns, Vue composition-API docs, TanStack, etc.

### Testing tactics and standards
Also zero foundation coverage. Patterns worth authoring: test pyramid, contract testing, snapshot testing (and when not to), property-based testing, deterministic test environments, test-data management, flakiness-hunting. A likely `tactics/testing/` folder plus a meta-standard on test documentation. Sources: xUnit Test Patterns (Meszaros), Growing Object-Oriented Software Guided by Tests (Freeman & Pryce), Hillel Wayne on property-based testing.

### Bulk-classify `stage_floor` on remaining patterns
Only 8 of ~75 patterns have `stage_floor` set. The rest default to "applies at every stage" — conservative but not accurate. Work through the inventory and add floors where they matter. Priority list is anything that came up in a review as "Missing — deferred to MVP" or "deferred to production" without a stage_floor already.

### Extend context roster
Deferred from the "initially seed 6 contexts" decision. Candidates: `context-multi-tenant-saas` (per-tenant isolation, noisy-neighbour, per-tenant data sharding), `context-iot-platform` (device fleet + ingest + command). Only add if 6 contexts feel thin in real use.

### Two Fowler event-* patterns
`pattern-event-notification` and `pattern-event-carried-state-transfer` — already authored during the initial seeding but could be wired more tightly with `dtree-choose-event-style` and the new `context-event-driven-system` recommended_patterns.

---

## Tooling

### Pre-commit hook for index freshness
`python tools/build_index.py` runs at commit time so contributors don't have to remember. Validator already fails on stale index; the hook just removes the "commit → push → CI fails → amend" loop. Trivial to add to `.pre-commit-config.yaml` or as a raw `.git/hooks/pre-commit` script.

### Python / MCP tool layer for deterministic protocol steps
Today the subagent reads YAML for structural queries. With proper tools (`carta.match_context(task)`, `carta.resolve_prerequisites(id)`, `carta.apply_dtree(id, criteria)`, `carta.get_node(id)`), the deterministic steps become a single tool call each, freeing the subagent's context budget for judgement steps. Two shapes:
- **Python CLI** callable from Bash — simplest, works today.
- **MCP server** — long-running, holds the index in memory, supports filesystem watchers. Higher ceremony, better for stable teams.

Start with the CLI if/when the subagent starts hitting context pressure.

### Project-level stage declaration format
The traversal protocol says "a project that has declared its stage in `projects/<project>/stage.<project>.md` or an equivalent convention can be read without asking again" — but the exact format isn't specified. Define it: probably a minimal node with `stage:` frontmatter and a body explaining the declaration.

### LOG.md automation
`LOG.md` is meant to record traversals, ingests, lint passes, and captures (per `operations.md`). Today it's manual. Consider a `/carta` post-run hook that appends an entry automatically.

---

## Schema and design

### Stage-scoped solutions
Solutions today are stage-general in frontmatter; the `## Implementation sequence` names stages in prose. A `/carta-review` surfaced this: "A stage-scoped mechanism would let the traversal produce a stage-scoped pattern scorecard directly rather than filtering the stage-general list."

Options:
- Add an optional `stage_scope:` field to solution frontmatter (list of stages where the composition applies).
- Allow multiple solution nodes for the same problem, each scoped to a stage.
- Keep it in prose; add a convention for how the implementation sequence marks stage transitions.

Worth a design conversation before committing — not a quick edit.

### Multi-dimensional node keys
The index currently keys by filename-stem (`pattern-rest-api` vs `pattern-rest-api.org`). Works, but the "extensions that share an id with a foundation pattern" case (e.g. `teams/platform/extensions/pattern-rate-limiting.platform.md` alongside foundation `pattern-rate-limiting.md`) is awkward — is it an extension or a misplaced override? Review the shape and maybe clarify the naming convention.

---

## Integrations

### Spec Kit example
Called out as Planned in README's status table. Worked example of how a Carta traversal feeds into Spec Kit's flow — probably a `projects/spec-kit-example/` scenario.

### CLAUDE.md generator
Given a Carta scope, generate a `CLAUDE.md` for a target project that points agents at the relevant contexts, stage, and recommended patterns. Useful for teams that don't want to run `/carta` on every task.

### Obsidian Dataview example queries
A few saved Dataview queries for common views — "patterns by pillar", "patterns my org has overridden", "ADRs affecting this context". Lives in `00-meta/obsidian-setup.md` or a new `00-meta/dataview-queries.md`.

---

## Known debt

### Pre-existing worked-example lint warnings
Nine writing-rule lint warnings in `org/decisions/adr-0001-fastapi-as-default.org.md`, `projects/payments-api/decisions/adr-0001-relaxed-circuit-breaker-timeouts.payments-api.md`, and a couple of others. These are illustrative of realistic org content (real ADRs run long) — arguably correct to leave alone, but worth a deliberate trim pass for consistency with the writing rules we ask users to follow.

### Trim CHARTER.md
3322 words. Governance docs earn their length, but a pass to remove duplicated four-level-model explanation (it's in README, CHARTER, overview, node-schema, traversal-protocol) would help.
