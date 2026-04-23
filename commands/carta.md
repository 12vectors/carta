Traverse the Carta architectural knowledge base for the task below.

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
- Otherwise check PROJECT for a stage declaration (`PROJECT/stage.<project>.md` or equivalent).
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

## Traverse

See `00-meta/traversal-protocol.md` for the full normative algorithm. Summary:

1. **Context(s) and pillars.** Match the task against `DECISION_TREE.md`'s signal table to identify one or more contexts. Identify the 1–3 pillars the task is optimising for (from FOUNDATIONS/05-pillars/).

2. **Candidate set.** From each matched context, collect `recommended_patterns`. Add relevant extensions at org/team/project levels whose `applies_to` matches.

3. **Resolve overrides.** Most-specific wins: PROJECT → TEAM → ORG → foundation. Override files use level suffixes (`.org.md`, `.<team>.md`, `.<project>.md`).

4. **Evaluate each candidate.** Check `When to use` / `When NOT to use` / `Decision inputs`. Note which principles (FOUNDATIONS/15-principles/) each pattern realises — cite principles alongside patterns for durable backing. For review-shaped traversals (auditing existing code), pair pattern status with specific file:line evidence; absence-of-imports alone is not sufficient.

5. **Apply stage floor.** Compare each candidate's `stage_floor` against the task stage. Patterns above the floor are **demoted** — listed under "When you graduate to stage X", not as current findings. Patterns at or below the floor are evaluated normally.

6. **Resolve prerequisites.** Recursively include patterns named in `prerequisites`.

7. **Conflicts.** Present any `conflicts_with` between candidates to the user; do not silently drop either.

8. **Alternatives via decision trees.** If the candidate set contains two or more patterns a dtree's `decides_between` includes, apply the dtree (FOUNDATIONS/25-decision-trees/) to pick one and mark the others as considered-and-rejected.

9. **Contradictions.** Read `contradicted_by`. Present substance, not just the link.

10. **Standards.** Read FOUNDATIONS/40-standards/, ORG/standards/, TEAM/standards/, PROJECT/standards/. Flag violations. Check whether any decision relaxes them.

11. **Antipatterns.** Scan FOUNDATIONS/50-antipatterns/ + extensions. Antipatterns do not carry a stage floor — they apply at every stage. Flag risks in the candidate set.

12. **Solutions.** Check FOUNDATIONS/30-solutions/ for an existing composition that matches your candidate set. Prefer it over re-assembling patterns.

13. **Decisions.** Read ADRs at org, team, and project levels. Respect `accepted` ones.

## Report

Structure the output as:

**Stage**: the declared stage, and how it was determined (asked / declared / provided).

**Context(s)**: which matched and why.

**Pillars foregrounded**: the 1–3 quality lenses the task is optimising for. Rank any ordered findings (e.g. "top risks") by these pillars.

**Principles applied**: the principles (by ID) each recommended pattern realises. A finding without a principle citation is weaker than one with.

**Decision trees consulted**: any dtree used to pick between alternatives, and which options were kept vs rejected.

**Recommended patterns (current stage)**: each pattern with a one-line rationale, the level it comes from (foundation / org / team / project), and — for review-shaped traversals — a code citation (file:line or named range) backing the status.

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
