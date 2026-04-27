Perform a multi-pass Carta review of an existing codebase.

## When to use this vs `/carta`

Use `/carta-review` when:
- You're auditing an existing application against Carta's knowledge base.
- The scope is more than a handful of files (dozens to hundreds).
- Every finding must be backed by a `file:line` citation.
- The review benefits from iteration: one pass picks up prereqs or antipatterns the first pass didn't consider.

Use `/carta` instead for quick "what pattern applies to X?" conversations — no codebase read required.

**Output**: by default the report is **concise** — top issues, status-grouped findings, a one-line "Already in place" summary, empty sections collapsed. Ask for `verbose`, `full`, or "show every pattern" after the run to see the full scorecard with `Present` rows, principles applied, decision trees consulted, and full standards list. The subagent emits both forms in a single run, so verbose detail is available without re-running.

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

Produce a concise, terminal-friendly report. Order matters — a
skim-reader should get the answer in the first ~6 lines.

Layout (use these section headers verbatim, in this order):

**Top issues (act on these first):**
The 3 highest-priority findings, ordered by foregrounded pillar.
Format per line: `[!] pattern-name — file:line — one-line rationale`.
If fewer than 3 issues exist, list what you have. If zero, say so
explicitly ("No current-stage gaps surfaced.").

**Scope:** one line — "foundation + org [+ team <name>] [+ project <name>]".
**Stage:** one line — declared stage + how determined (asked / declared).
**Pillars:** one line — 1–3 foregrounded.
**Contexts:** one line — matched contexts.

**Missing / Violated:** status-grouped bullets. Each finding:
  `[!] pattern-name (<level>) — file:line — short rationale`.

**Partial:** same format with `[~]`.

**Already in place (N):** ONE line, names only — no per-pattern detail.
  Example: `Already in place (8): pattern-rest-api, pattern-timeout, …`.

**Deferred to <stage>:** terse — "When you graduate to <stage>:
  pattern-bulkhead, pattern-leader-election." Group by graduation stage.

**Avoid:** antipatterns flagged with `[!]` plus file:line and one-line
  rationale. Same single-bullet format as Missing.

**Standards:** populated only if there are violations or relaxations.
**Conflicts and contradictions:** populated only when present.
**Existing solutions:** populated only when a solution matches.

**Gaps in Carta itself:** terse bullets — missing pattern, context,
  dtree, or edge that would have helped this traversal.

**Iteration:** ONE line — "Stable after N passes; M candidates
  evaluated." If the 4-pass cap tripped, name the candidates the last
  pass added on a second line.

--- Rules for the concise body ---

- **Collapse empty sections.** If a section has no entries, omit the
  header entirely. Empty sections train readers to skip everything.
- **Single-column bullets, never tables.** Tables wrap badly at 80
  columns. Every finding is one bullet line.
- **Status markers** in front of each finding: `[!]` Missing / Violated,
  `[~]` Partial, `[?]` Open question. Pure ASCII — no colour, no unicode.
- **Cap rationale at ~15 words per finding.** Detail belongs in the
  verbose appendix.
- **Order findings by foregrounded pillar** so the highest-pillar
  issues come first within each section.
- **Repeat the top 3 inside Missing / Violated.** Top issues serves the
  skim-reader; the section serves the full reader. Repetition is fine.
- **No per-Present detail** in the concise body — only the names line.

--- Verbose appendix (always emit; parent shows on request) ---

AFTER the END marker, emit this block. The parent will show it only if
the user asks for "full", "verbose", "every pattern", or per-pattern
detail. Always produce it — running the subagent twice is more
expensive than emitting both modes once.

  VERBOSE APPENDIX (parent: relay only if user asks for full / verbose
  / per-pattern detail):

  **Pattern scorecard (full):** markdown table with one row per
  candidate including `Present` rows.
  | Pattern | Level | Status | Code evidence | Rationale |

  **Per-Present evidence:** for each `Already in place` pattern, a
  file:line citation and one-line rationale.

  **Principles applied:** which principle each recommended pattern
  realises, by id.

  **Decision trees consulted:** which dtrees ran, which options were
  selected vs rejected, the criteria used.

  **Standards (full):** every applicable standard, including those
  that are not violated.

  **Prerequisites:** patterns that must be in place first, in
  dependency order.

--- Rules (apply to both blocks) ---

- Do not invent patterns, standards, decisions, or code citations.
- Absence-of-imports is evidence only when paired with a scope ("across
  backend/app/**/*.py, no X module is imported") — never on its own.
- Every pattern status must have a file:line citation.
- Every antipattern flag must have a file:line citation.
- Report Carta gaps as a first-class section — missing content is more
  valuable than confidently filling the gap with guesses.

--- Output format (IMPORTANT) ---

Wrap the concise body between these exact markers:

---BEGIN CARTA REVIEW REPORT---

(concise body here — every section above, every file:line citation,
 every Carta gap, but NOT the verbose appendix)

---END CARTA REVIEW REPORT---

Then emit the VERBOSE APPENDIX block AFTER the END marker. The parent
relays the marked block by default and shows the appendix only when
the user asks for it. Do not put the appendix inside the markers.
```

## Present the subagent's report

**The report is the product of this command. Your job is to relay it verbatim — not to summarise it.** The subagent emits a concise body between marker lines (`---BEGIN CARTA REVIEW REPORT---` and `---END CARTA REVIEW REPORT---`) followed by a `VERBOSE APPENDIX` block after the END marker. Default behaviour: relay the marked block in full; hold the appendix back unless the user asks for it.

Format your response to the user exactly in this order:

1. **A one-sentence stance** before the report — the overall fit / gaps verdict in ≤25 words. The report itself leads with `Top issues`, so do NOT repeat those findings here; just frame the verdict ("Production-stage payments-api: solid pipeline; rate-limiting and idempotency are the two production blockers.").

2. **The concise report, rendered verbatim.** Paste everything the subagent produced between the markers, unchanged. Do not paraphrase. Do not abbreviate. Do not collapse bullet lists. The concise format already cuts what's safely cuttable; further trimming undoes the design.

3. **One-sentence iteration note** if the subagent reported a 4-pass cap without convergence. Suggest scoping the next run smaller (single service, single context, single concern).

4. **Restate the "Gaps in Carta itself" section** at the bottom if the report contains one, as a separate call-out distinct from application-level findings. This is Carta's compounding knowledge output; it's important enough to surface twice rather than lose to scroll.

5. **Offer follow-ups** (pick what fits; offer 3 of these, not all):
   - (a) trim to a top-5 concrete action list for the target codebase.
   - (b) dive deeper on one specific finding with more file reads.
   - (c) draft the Carta gap fixes as edits against `$CARTA_PATH`.
   - (d) **show the verbose appendix** — full pattern scorecard with `Present` rows, principles applied, dtrees consulted, full standards list. Use this when the user asks for "full", "verbose", "every pattern", or per-Present detail; relay the `VERBOSE APPENDIX` block the subagent emitted after the END marker.
   - (e) explain why a specific pattern was scored Present — pull the per-Present line from the appendix.

Never summarise the report in place of relaying it. A summary without the full report forces the user to ask you to play it back — which wastes a turn and defeats the subagent's multi-pass work. The subagent runs *so that* the user can read the structured output.

The verbose appendix is data the subagent already paid to produce; show it on request without re-running. If the user wants the appendix appended every time (some teams do), they can say so — relay it inline after the marked block on subsequent runs.

Do not edit or commit anything in the target codebase. This command is read-only against the target.

## Task

$ARGUMENTS
