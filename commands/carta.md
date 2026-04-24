Traverse the Carta architectural knowledge base for the task below.

## When to use this vs `/carta-review`

Use `/carta` when:
- You need a quick architectural recommendation on a task or question.
- No codebase read is required — or at most a handful of files the conversation will cite directly.
- A single-response traversal is enough.

Use `/carta-review` instead when:
- You are auditing an existing application (dozens to hundreds of files).
- Every finding must be backed by a `file:line` citation from the target codebase.
- The review benefits from iteration — a dedicated subagent running multiple passes with its own context budget.

## Find Carta

Resolve the CARTA_PATH environment variable (run: `echo $CARTA_PATH`). This is the root of the Carta knowledge base. If unset, tell the user to configure it and stop.

CARTA_PATH should point to the repository root — the directory containing `foundations/`, and optionally `org/`, `teams/`, and `projects/`.

Set working references:
- FOUNDATIONS = CARTA_PATH/foundations
- ORG = CARTA_PATH/org
- TEAM = CARTA_PATH/teams/<team> if a team scope is specified or can be inferred from the current working directory
- PROJECT = CARTA_PATH/projects/<project> if a project scope is specified or can be inferred from the current working directory

## Confirm the stage

Before traversing, confirm the system's operational stage. Values: `prototype`, `mvp`, `production`, `critical` (see FOUNDATIONS/12-stages/).

- If the user provided the stage in the task, use it.
- Otherwise check PROJECT for a stage declaration — read `entries[adr-0001-project-charter.<project>].stage` from `INDEX.yaml` (this is where `/carta-project-setup` records it). If the charter is still `status: proposed`, treat the stage as a suggestion rather than authoritative.
- Otherwise **ask the user**: *"Is this system at the prototype, MVP, production, or mission-critical stage?"* Do not infer from repo signals — a Dockerfile or CI config is not a reliable indicator.

Read the matching node in FOUNDATIONS/12-stages/ to understand what relaxes and what stays baseline at this stage. Every severity in the final report is relative to this stage.

## Discover available content

List what exists at each level. Carta may be partially built — work only with what is present.

| Path | Contains |
|------|----------|
| FOUNDATIONS/05-pillars/ | Quality lenses (reliability, security, cost, op-ex, performance) |
| FOUNDATIONS/10-contexts/ | System archetypes (web app, internal tool, agentic, pipeline, ...) |
| FOUNDATIONS/12-stages/ | Operational stages (prototype, mvp, production, critical) |
| FOUNDATIONS/15-principles/ | Cross-cutting design heuristics above patterns |
| FOUNDATIONS/20-patterns/ | Reusable patterns — styles/, tactics/<concern>/, integration/ |
| FOUNDATIONS/25-decision-trees/ | Selection guides between alternative patterns |
| FOUNDATIONS/30-solutions/ | Composed patterns for recurring problems |
| FOUNDATIONS/40-standards/ | Meta-standards and templates |
| FOUNDATIONS/50-antipatterns/ | What not to do and why |
| ORG/overrides/ | Org-specific pattern overrides (`.org.md` suffix) |
| ORG/extensions/ | Org-specific patterns not in foundations |
| ORG/standards/ | Org-level concrete standards |
| ORG/decisions/ | Org-level ADRs |
| TEAM/overrides/, extensions/, standards/, decisions/ | Team-level, `.<team>.md` suffix |
| PROJECT/overrides/, extensions/, standards/, decisions/ | Project-level, `.<project>.md` suffix |

Report briefly what directories exist so the user knows the scope of the traversal.

## Load the index

Read `CARTA_PATH/INDEX.yaml` once at the start (it's at the repository root — the index spans every level, not just foundations). It pre-computes the inverted lookups you'd otherwise get by scanning directories — `context_to_patterns`, `pillar_to_principles`, `pattern_to_dtrees`, `affects_to_adrs`, `context_to_standards`, `context_to_antipatterns`, `solution_composes`, `prerequisites_closure`, and the `overrides` resolution map. Structural queries below go through the index; body reads are reserved for judgement material (`When to use`, `Solution sketch`, stage descriptions, dtree recommendations).

## Traverse

See `00-meta/traversal-protocol.md` for the full normative algorithm. Summary below — every step names the index lookup that replaces a directory scan. Body reads stay reserved for judgement material (`When to use`, `Solution sketch`, stage descriptions, dtree recommendations).

1. **Contexts, pillars, stage.** Match the task against `DECISION_TREE.md`'s signal table to identify one or more contexts. Identify the 1–3 pillars the task is optimising for (`FOUNDATIONS/05-pillars/`). Re-read `FOUNDATIONS/12-stages/stage-<stage>.md` — every severity in the report is relative to this stage.

2. **Candidate set.** For each matched context, read `context_to_patterns[<ctx>]` from the index. This covers foundation patterns *and* any org/team/project extensions whose `applies_to` matches — no directory scan.

3. **Resolve overrides.** For each candidate, read `overrides[<id>]` — it names the entry key at each level. Pick most-specific-first: project → team → org → foundation. Resolve the winning entry via `entries[<key>].path`.

4. **Evaluate each candidate.** Read the node body for `When to use` / `When NOT to use` / `Decision inputs`. Read `pattern_to_principles[<id>]` and filter against `pillar_to_principles[<foregrounded-pillar>]` to cite the principles each pattern realises — a finding without a principle citation is weaker than one with. Apply `stage_floor`: patterns above the task stage are **demoted** to "defer to stage X", not dropped.

5. **Resolve prerequisites.** Use `prerequisites_closure[<id>]` for the transitive (cycle-safe) prerequisite set. Add missing ones to the candidate set and evaluate them.

6. **Conflicts.** Read each candidate's `conflicts_with` from its frontmatter (via `entries[<key>]`). Present any pair in the candidate set to the user; do not silently drop either.

7. **Alternatives via decision trees.** For each candidate, read `pattern_to_dtrees[<id>]`. If two or more candidates both appear in a dtree's `decides_between`, apply the dtree (FOUNDATIONS/25-decision-trees/) to pick one and mark the others considered-and-rejected.

8. **Contradictions.** Read each candidate's `contradicted_by`. Present substance, not just the link. Check ADRs for resolution.

9. **Standards.** Use `context_to_standards[<ctx>]` plus `context_to_standards.__universal`. Read the body of each applicable standard to check for violations; note any decision that relaxes them.

10. **Antipatterns.** Use `context_to_antipatterns[<ctx>]`. Antipatterns carry no stage floor — they apply at every stage. Flag risks in the candidate set, citing each antipattern's `How to recognise` and `How to fix`.

11. **Solutions.** Walk `solution_composes` — each entry is solution-id → composed-patterns. Prefer a pre-composed solution when its composes list is a subset or near-match of the candidate set.

12. **Decisions (ADRs).** For each candidate pattern id or matched context id, read `affects_to_adrs[<id>]`. Respect `accepted` ADRs; follow supersessions; note `proposed` ones as pending. More specific decisions take precedence (project > team > org).

## Report

Structure the output as:

**Stage**: the declared stage, and how it was determined (asked / declared / provided).

**Context(s)**: which matched and why.

**Pillars foregrounded**: the 1–3 quality lenses the task is optimising for. Rank any ordered findings (e.g. "top risks") by these pillars.

**Principles applied**: the principles (by ID) each recommended pattern realises. A finding without a principle citation is weaker than one with.

**Decision trees consulted**: any dtree used to pick between alternatives, and which options were kept vs rejected.

**Recommended patterns (current stage)**: each pattern with a one-line rationale and the level it comes from (foundation / org / team / project).

**When you graduate to stage X**: patterns demoted because their stage_floor is above the current stage. Visible, not urgent.

**Prerequisites**: patterns that must be in place first, in dependency order.

**Standards**: applicable constraints, noting their level and any relaxing decision.

**Avoid**: relevant antipatterns.

**Conflicts and contradictions**: any unresolved issues with both sides presented.

**Existing solutions**: matches from FOUNDATIONS/30-solutions/.

**Gaps**: content that would have been useful but doesn't exist in Carta yet — missing patterns, contexts, principles, dtrees, solutions, or stale edges. This helps the team know what to author next.

Do not invent patterns, standards, or decisions that are not in the knowledge base. If Carta has insufficient content for the task, say so plainly and note what's missing.

## Task

$ARGUMENTS
