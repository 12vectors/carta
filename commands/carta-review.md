Perform a multi-pass Carta review of an existing codebase.

## When to use this vs `/carta`

Use `/carta-review` when:
- You're auditing an existing application against Carta's knowledge base.
- The scope is more than a handful of files (dozens to hundreds).
- Every finding must be backed by a `file:line` citation.
- The review benefits from iteration: one pass picks up prereqs or antipatterns the first pass didn't consider.

Use `/carta` instead for quick "what pattern applies to X?" conversations — no codebase read required.

## Find Carta and resolve scope

1. Resolve CARTA_PATH (`echo $CARTA_PATH`). If unset, tell the user to configure it and stop.
2. Parse the target codebase path from the user's invocation. If not provided, default to the current working directory. Confirm with the user if ambiguous.
3. Infer team and project scope from the working directory name if obvious; otherwise ask (or proceed with foundation + org only).

## Confirm the stage

Ask the user what operational stage the target system is at: `prototype`, `mvp`, `production`, or `critical`. See `foundations/12-stages/` for what each means.

- If the user already stated it in the task, use that.
- If the project has been scaffolded by `/carta-project-setup`, read `entries[adr-0001-project-charter.<project>].stage` from `INDEX.yaml` and say so. If that charter is still `status: proposed`, confirm with the user rather than trust it.
- Otherwise **ask the user directly** — do not infer from repo signals.

Record the declared stage and how you learned it; both go in the final report.

## Delegate to a review subagent

Spawn a `general-purpose` subagent via the Agent tool. The subagent handles the multi-pass traversal with its own context budget (which is the point — review-shaped traversals against a large repo exceed what a single-turn response can handle).

Pass the subagent this self-contained prompt, with the placeholders filled in:

```
You are performing a Carta review of an existing codebase. The review must
be iterative and stop when the candidate set is stable, not when the
response clock runs out.

Setup:
- CARTA_PATH = <expanded absolute path>
- Codebase root = <expanded absolute path>
- Team scope (if any) = <team name or 'none'>
- Project scope (if any) = <project name or 'none'>
- Stage = <prototype|mvp|production|critical>
- Stage source = <asked | project-declaration | caller-provided>
- Task = <user's question, or 'full architectural review'>

Load these Carta files first (Read):
- CARTA_PATH/INDEX.yaml — the pre-computed graph index (at the repository root; it spans every level). Use it for structural queries (context_to_patterns, pillar_to_principles, pattern_to_dtrees, overrides, prerequisites_closure, context_to_standards, context_to_antipatterns, affects_to_adrs, solution_composes). Never directory-scan for these — use the index.
- CARTA_PATH/00-meta/traversal-protocol.md — normative algorithm
- CARTA_PATH/DECISION_TREE.md — context signal table
- CARTA_PATH/foundations/12-stages/stage-<stage>.md — what relaxes, what stays baseline

Maintain explicit state across passes: a candidate set (pattern id → status),
a findings list (finding → evidence), a pass counter. Write these down in
your working output so you can check them at the end of each pass.

--- PASS 1: Frame ---

1. Match the codebase and task against DECISION_TREE.md signals. Identify
   applicable contexts; read each context node to see its signals,
   recommended_patterns, and common_antipatterns.
2. Identify the 1–3 pillars the task is optimising for (from
   foundations/05-pillars/). State them explicitly.
3. Re-read the stage node; note what relaxes and what stays baseline.

--- PASS 2: Candidate assembly ---

4. For each matched context, read `context_to_patterns[<ctx>]` from the
   index. This already includes foundation patterns AND any
   org/team/project extensions whose `applies_to` matches — do not
   directory-scan `extensions/` separately, the index covers it. Add
   every entry key to the candidate set.
5. For each candidate, read `overrides[<id>]` from the index — it names
   the winning entry key at each level (project, team, org). Pick
   most-specific-first: project → team → org → foundation. Resolve the
   winning entry via `entries[<key>].path`. Record which level the
   pattern came from (it goes in the scorecard).
6. Apply stage_floor: for each candidate with stage_floor > current stage,
   mark it 'deferred to stage X' in the candidate set. Do not drop — it
   still appears in the report, just in the deferred section.

--- PASS 3: Code evidence (the expensive pass) ---

7. For each current-stage candidate, read the relevant files in the
   codebase. Use Grep/Glob to locate implementations; use Read to inspect.
   Budget 3–8 file reads per pattern; prefer depth over breadth. Also
   read `pattern_to_principles[<id>]` from the index so the scorecard can
   cite the principles each pattern realises.
8. Assign each pattern a status — Present, Partial, Missing, or Violated —
   and attach a file:line citation (or named file range). An assertion
   like 'no structured logging' must be backed by 'no logging module
   imported in backend/app/main.py:1-40 or across backend/app/**/*.py'.
9. Note code findings that suggest additional patterns not yet in the
   candidate set (e.g. BackgroundTasks usage suggests
   pattern-async-request-reply and dtree-choose-background-work).

--- PASS 4: Iterate until stable (cap 4 iterations total) ---

10. For each candidate surviving passes 2–3:
    a. Read `prerequisites_closure[<id>]` from the index — transitive
       and cycle-safe. Add any missing to the candidate set.
    b. Read `conflicts_with` from `entries[<key>]`. Flag pairs in the set.
    c. Read `contradicted_by` from `entries[<key>]`. Note contradictions;
       check whether an ADR resolves each.
11. For each candidate, read `pattern_to_dtrees[<id>]` from the index.
    For any pair of candidates that both appear in a dtree's
    `decides_between`, apply the dtree (read the dtree node, walk its
    Criteria against task characteristics, use its Recommendation
    table). Keep the selected option; mark others 'considered and
    rejected via [[dtree-X]]'.
12. Evaluate every newly-added candidate via pass 3 (code evidence).
13. Stop iterating when a pass adds no new candidates. Cap at 4 total
    iterations regardless of stability.

--- PASS 5: Cross-reference ---

14. Standards: use `context_to_standards[<ctx>]` for each matched
    context, plus `context_to_standards.__universal` for standards
    that apply everywhere. Read each standard's body to check whether
    any candidate violates it in code. Check whether an ADR relaxes it.
15. Antipatterns: use `context_to_antipatterns[<ctx>]` for each matched
    context. Antipatterns have no stage_floor — they apply at every
    stage. For each, read the body and check the codebase for its
    `How to recognise` signals. Cite file:line evidence per flagged
    antipattern.
16. Solutions: walk `solution_composes` — each entry is solution-id →
    composed-patterns. Does any solution's composes list match a subset
    of the current candidate set? Prefer pre-composed solutions when
    they cover the shape.
17. ADRs: for each candidate pattern id and matched context id, read
    `affects_to_adrs[<id>]`. Filter to the scopes that apply (org
    always; team/project only if scoped). For each ADR, apply its
    constraints (`accepted` binds; `superseded` redirects; `proposed`
    is pending).

--- PASS 6: Report ---

Structure the output exactly:

**Carta scope** — directories present; team/project scope.
**Context(s)** — which matched and why.
**Stage** — declared stage + how determined.
**Pillars foregrounded** — 1–3 lenses.
**Principles applied** — principles (by ID) each recommended pattern
  realises. Pull from foundations/15-principles/ by matching pillar and
  related_patterns.
**Decision trees consulted** — which dtrees, and which options were
  selected vs rejected.

**Pattern scorecard (current stage)** — a markdown table:
  | Pattern | Level | Status | Code evidence | Rationale |

**Deferred to stage X** — patterns above the current stage floor,
  grouped by the stage they unlock. Terse, not itemised.

**Prerequisites** — patterns that must be in place first.
**Standards** — applicable, violations, relaxing ADRs.
**Avoid** — antipatterns flagged with code evidence.
**Conflicts and contradictions** — unresolved pairs.
**Existing solutions** — matches or partial matches from
  foundations/30-solutions/.

**Top gaps, ranked by risk** — ordered by the foregrounded pillars.
  Include the pillar each finding serves.

**Gaps in Carta itself** — missing patterns, contexts, principles,
  dtrees, or edges that would have helped this traversal. This is
  how Carta grows; take it seriously.

**Iteration log** — how many passes ran, why you stopped (stable or
  cap), and any parts of the protocol you had to skip and why.

--- Rules ---

- Do not invent patterns, standards, decisions, or code citations.
- Absence-of-imports is evidence only when paired with a scope ("across
  backend/app/**/*.py, no X module is imported") — never on its own.
- Every pattern status must have a file:line citation.
- Every antipattern flag must have a file:line citation.
- Report Carta gaps as a first-class section — missing content is more
  valuable to the user than confidently filling the gap with guesses.
- If the 4-iteration cap trips, say so and name which candidates the
  last pass added. The scope may be too big for a single review.

--- Output format (IMPORTANT) ---

Your final message back to the parent agent IS the report. The parent
will relay your entire output to the user. Do not truncate, summarise,
or replace any section with a placeholder. Do not say 'see tool result
above' or 'full report omitted'.

Wrap your report between these exact marker lines so the parent can
identify the block to relay:

---BEGIN CARTA REVIEW REPORT---

(full structured report here — every section from Pass 6, every
 pattern-scorecard row, every file:line citation, every Carta gap)

---END CARTA REVIEW REPORT---

Anything outside the markers (e.g. a brief meta-note to the parent
about the iteration-cap result) is fine but will not be relayed to
the user verbatim. Put everything the user needs to see between the
markers.
```

## Present the subagent's report

**The report is the product of this command. Your job is to relay it verbatim — not to summarise it.** The subagent will emit its report between marker lines (`---BEGIN CARTA REVIEW REPORT---` and `---END CARTA REVIEW REPORT---`). The content between those markers must reach the user in full.

Format your response to the user exactly in this order:

1. **A two-sentence lead** (≤60 words total). The overall stance (fit / gaps) and the three most-important current-stage findings. Put the lead before the report so a skim-reader gets the headline first.

2. **The full report, rendered verbatim.** Paste everything the subagent produced between its markers, unchanged. Do not paraphrase. Do not abbreviate tables. Do not replace bullet lists with "…and more". If the report is long, it's long — that's precisely why `/carta-review` spawns a subagent with its own context budget. A truncated relay defeats the workflow.

3. **One-sentence iteration note** if the subagent reported a 4-pass cap without convergence. Suggest scoping the next run smaller (single service, single context, single concern).

4. **Restate the "Gaps in Carta itself" section** at the bottom if the report contains one, as a separate call-out distinct from application-level findings. This is Carta's compounding knowledge output; it's important enough to surface twice rather than lose to scroll.

5. **Offer a follow-up**: (a) trim to a top-5 concrete action list for the target codebase, (b) dive deeper on one specific finding with more file reads, or (c) draft the Carta gap fixes as edits against `$CARTA_PATH`.

Never summarise the report in place of relaying it. A summary without the full report forces the user to ask you to play it back — which wastes a turn and defeats the subagent's multi-pass work. The subagent runs *so that* the user can read the structured output.

Do not edit or commit anything in the target codebase. This command is read-only against the target.

## Task

$ARGUMENTS
