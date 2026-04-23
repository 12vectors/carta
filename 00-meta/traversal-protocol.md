# Traversal Protocol

The algorithm an agent follows when consulting Carta to make an architectural decision. This is the normative reference for the traverse operation described in `operations.md`.

---

## Prerequisites

Before traversing, the agent must know:

1. **The task or goal.** What architectural decision needs to be made. This comes from the user, a spec, or an upstream workflow.
2. **The Carta root.** Where the knowledge base lives on disk. This is the repository root, which contains `foundations/`, `org/`, and optionally `teams/` and `projects/`.
3. **The scope (if any).** Which team and/or project to include in the traversal. If no scope is specified, the traversal uses only foundation and organisation levels.
4. **The target codebase (for review-shaped traversals).** When the traversal is auditing an existing application, the agent must have read access to the code. Pattern-level findings must be grounded in specific file:line evidence; an assertion like "no structured logging" is only useful if it can be defended with named files that do or do not import a logging module. Traversals that skip code-level reading produce aspirational advice; traversals that pair pattern checks with code reads produce defensible findings.
5. **The stage.** Which operational stage the system is aiming at: `prototype`, `mvp`, `production`, or `critical` (see `foundations/12-stages/`). If the caller did not provide it, the agent **must ask** before proceeding. Do not infer stage from repo signals (the presence of a Dockerfile or CI config is not a reliable indicator, and guessing silently produces wrong severities). Pose the question directly: *"Is this system at the prototype, MVP, production, or mission-critical stage?"* Once answered, record the stage in the report so the user can correct it if they disagree. A project that has declared its stage in `projects/<project>/stage.<project>.md` or an equivalent convention can be read without asking again.

---

## Four-level resolution

Carta resolves nodes across four levels, from most specific to least specific:

1. **Project** — `projects/<project>/overrides/`, `projects/<project>/extensions/`, `projects/<project>/standards/`, `projects/<project>/decisions/`
2. **Team** — `teams/<team>/overrides/`, `teams/<team>/extensions/`, `teams/<team>/standards/`, `teams/<team>/decisions/`
3. **Organisation** — `org/overrides/`, `org/extensions/`, `org/standards/`, `org/decisions/`
4. **Foundations** — `foundations/`

For **pattern overrides**, the most specific level wins:
1. Check `projects/<project>/overrides/<node-id>.<project>.md`
2. If not found, check `teams/<team>/overrides/<node-id>.<team>.md`
3. If not found, check `org/overrides/<node-id>.org.md`
4. If not found, use `foundations/<node-id>.md`

For **standards, decisions, antipatterns, and extensions**, all levels accumulate. Any level can override or relax guidance from a higher level, provided the reasoning is documented in a decision record at the appropriate level.

Not every level is required. If there is no team or project scope, skip those levels.

---

## Foundation layers

In addition to overrides, extensions, standards, and decisions, the foundations contain four upstream layers that the traversal consults alongside patterns:

- **Pillars** (`foundations/05-pillars/`) — quality lenses: `reliability`, `security`, `cost`, `operational-excellence`, `performance`. Every task optimises for one to three of these. Identifying them early frames later trade-offs and the final report.
- **Contexts** (`foundations/10-contexts/`) — system archetypes matched via the signal table in `DECISION_TREE.md`. Contexts produce the initial candidate set via `recommended_patterns`.
- **Principles** (`foundations/15-principles/`) — cross-cutting design heuristics (e.g. `principle-design-for-failure`, `principle-observe-before-optimising`). Principles provide the heuristic each pattern is meant to embody; citing the principle makes a finding durable beyond the specific pattern.
- **Decision trees** (`foundations/25-decision-trees/`) — selection guides between alternative patterns (API style, messaging style, service boundary, event style, data-access strategy, background-work strategy). Consult when candidates compete for the same architectural role.

These layers are not optional flavour. If the final report does not cite the pillars the task is optimising for, the principles supporting the recommended patterns, or the dtree consulted when alternatives appeared, the traversal is incomplete.

---

## Algorithm

### Step 1 — Identify contexts, pillars, and stage

Read `DECISION_TREE.md`. Match the task against the signal table to identify one or more relevant contexts from `foundations/10-contexts/`.

- Multiple contexts may apply. Include all that match.
- If no context matches, follow the fallback procedure in `DECISION_TREE.md` (check if the task is architectural, note missing contexts, or proceed pattern-by-pattern).

Also identify the **pillars** (`foundations/05-pillars/`) the task is optimising for. Most tasks foreground one to three of: `reliability`, `security`, `cost`, `operational-excellence`, `performance`. The pillars frame the rest of the traversal — they determine which principles to check in step 4 and which trade-offs to highlight in the report. A "refactor our background jobs for restart-safety" task foregrounds reliability and operational-excellence; a "cap LLM spend per tenant" task foregrounds cost and security.

Confirm the **stage** from the prerequisites (`prototype`, `mvp`, `production`, `critical`). Read the corresponding node in `foundations/12-stages/` to understand what relaxes at this stage and what stays baseline. The stage determines the severity band for every subsequent finding: the same missing auth is a blocker at production and acceptable at prototype.

### Step 2 — Build the candidate set

For each matched context, read its node file in `foundations/10-contexts/`. Collect all entries from its `recommended_patterns` field. The union across all matched contexts is the initial candidate set.

Also scan extensions at all applicable levels — `org/extensions/`, `teams/<team>/extensions/` (if scoped), `projects/<project>/extensions/` (if scoped) — for additional patterns whose `applies_to` includes the matched contexts. Add these to the candidate set.

If proceeding without a context (fallback), build the candidate set by scanning `foundations/20-patterns/` relevant to the task — either an architecture style (`styles/`), concern-scoped tactics (`tactics/<concern>/`), or messaging (`integration/`) — plus any relevant extensions.

### Step 3 — Resolve overrides

For each candidate pattern, check whether an override exists. Walk from most specific to least specific and use the first match:

1. If a project is scoped, check `projects/<project>/overrides/<pattern-id>.<project>.md`.
2. If a team is scoped, check `teams/<team>/overrides/<pattern-id>.<team>.md`.
3. Check `org/overrides/<pattern-id>.org.md`.
4. If no override exists at any level, use the foundation node.

Override resolution applies only to patterns. Contexts and antipatterns in the foundations are read directly (other levels extend these via `extensions/`, not overrides).

### Step 4 — Evaluate each candidate

For each pattern in the candidate set, read the node and assess fit:

1. **When to use** — do the task's characteristics match the described triggers?
2. **When NOT to use** — do any counter-indications apply?
3. **Decision inputs** — can the questions be answered? If critical inputs are unknown, flag them for the user rather than guessing.
4. **Principles** — look up the principles in `foundations/15-principles/` whose `pillar` matches the task's foregrounded pillars (from step 1), and whose `related_patterns` include this candidate. Note the principle alongside the pattern: this gives the finding durable backing ("we recommend a circuit breaker *because* design-for-failure"). If a candidate serves a principle that isn't listed on it, the edge may be missing — flag it as a Carta gap.
5. **Code evidence (review-shaped traversals).** Read the relevant files in the target codebase. For each pattern, cite specific files and line ranges that implement it, partially implement it, or fail to implement it. A finding like "no rate limiting" is stronger as "no rate-limiting middleware in `backend/app/main.py:1-40`; no `slowapi` / `starlette-rate-limit` imports across the repo." Pattern status values (`Present`, `Partial`, `Missing`, `Violated`) must be backed by code evidence, not inferred from absence of imports alone.
6. **Stage floor.** Compare the pattern's `stage_floor` (if set) against the task's declared stage from step 1. Stages rank `prototype` < `mvp` < `production` < `critical`.
   - If `stage_floor` ≤ task stage, the pattern is evaluated normally; any gap is a current finding.
   - If `stage_floor` > task stage, the pattern is **demoted**: it stays visible in the report as "defer to stage `<floor>`", not as a current blocker. The user sees what will tighten when they graduate, without being blamed for not having it now.
   - If `stage_floor` is absent, treat it as `prototype` (the pattern applies at every stage).

A pattern that fails "When NOT to use" is removed from the candidate set. A pattern whose "When to use" doesn't match is also removed, unless it was pulled in as a prerequisite (step 5).

### Step 5 — Resolve prerequisites

For each remaining candidate, read its `prerequisites` field. For each prerequisite:

1. If the prerequisite is already in the candidate set, no action needed.
2. If not, add it and evaluate it (step 4). A prerequisite may itself have prerequisites — resolve recursively.
3. If a prerequisite fails evaluation (doesn't fit the task), flag the conflict: the candidate pattern requires something that doesn't apply. The user must decide whether to proceed.

Guard against circular prerequisites. If pattern A requires B and B requires A, flag the cycle and present both to the user.

### Step 6 — Check conflicts

For each remaining candidate, read its `conflicts_with` field. If two candidates in the set conflict with each other:

1. Present both patterns and the nature of the conflict to the user.
2. Do not silently drop either one. The user decides which to keep.
3. If an ADR at any level resolves the conflict for this context, follow the ADR's guidance. More specific ADRs take precedence.

### Step 7 — Resolve alternatives via decision trees

For each remaining candidate, check `foundations/25-decision-trees/` for a dtree whose `decides_between` includes this pattern. If the candidate set contains two or more patterns the dtree picks between (REST vs GraphQL vs gRPC, sync RPC vs pub-sub vs async-request-reply, monolith vs microservices, notification vs state-transfer, cache vs replica vs materialized view, inline vs queue vs workflow engine), apply the dtree:

1. Read the dtree's `criteria` and the task's characteristics from step 1.
2. Walk the `## Recommendation` table; pick the option that matches the task's situation.
3. Keep the chosen pattern in the candidate set; mark the others as "considered and rejected via `[[dtree-…]]`" in the report.
4. If the task spans situations (e.g. public API and internal API in one service), a dtree may pick two patterns — document both and the boundary between them.

Dtrees do not override conflicts — they inform choice between non-conflicting alternatives. A dtree recommendation does not silence a flagged conflict or contradiction from the earlier steps.

### Step 8 — Check contradictions

For each remaining candidate (including those selected via a dtree in step 7), read its `contradicted_by` field. For each contradiction:

1. Read the contradicting node to understand the substance of the disagreement.
2. Check whether an ADR resolves the contradiction for this context.
3. If resolved, follow the ADR. If unresolved, present the contradiction to the user with both sides.

Contradictions are informational, not eliminative. A pattern with an unresolved contradiction is still a valid candidate — the user just needs to know about the disagreement.

### Step 9 — Cross-reference standards

Collect standards from all applicable levels:

1. Read `foundations/40-standards/` — meta-standards and cross-cutting concerns.
2. Read `org/standards/` — org-level standards.
3. If a team is scoped, read `teams/<team>/standards/` — team-level standards.
4. If a project is scoped, read `projects/<project>/standards/` — project-level standards.

For each standard whose `applies_to` includes the matched contexts (or that has no `applies_to`, meaning it's universal):

1. Check whether any candidate pattern violates the standard.
2. If so, flag the violation. Check whether a decision at any level explicitly relaxes the standard for this context. If a decision exists, note the relaxation and its reasoning. If not, the violation must be resolved.

### Step 10 — Cross-reference antipatterns

Read all antipattern nodes in `foundations/50-antipatterns/` whose `applies_to` includes the matched contexts. Also check extensions at all applicable levels for additional antipatterns.

For each:

1. Check whether the candidate set risks triggering the antipattern.
2. If so, flag it with the antipattern's `How to recognise` signals and `How to fix` guidance.

This is a negative filter. Antipatterns don't add to the candidate set; they flag risks in it.

### Step 11 — Check for existing solutions

Read `foundations/30-solutions/` and check whether any existing solution's `composes` list is a subset or match of the current candidate set.

- If an exact or near-exact match exists, prefer the pre-composed solution. It includes integration guidance (how the patterns fit together) that the individual pattern nodes don't.
- If a partial match exists, note it — the existing solution may cover part of the task.

### Step 12 — Check ADRs

Collect decisions from all applicable levels:

1. Read `org/decisions/`.
2. If a team is scoped, read `teams/<team>/decisions/`.
3. If a project is scoped, read `projects/<project>/decisions/`.

For each ADR whose `affects` list includes any candidate pattern or matched context:

1. If the ADR is `accepted`, its constraints apply. Adjust the candidate set accordingly.
2. If the ADR is `superseded`, follow the superseding ADR instead.
3. If the ADR is `proposed`, note it as pending — the decision isn't final.

More specific decisions take precedence when they cover the same concern (project > team > org).

### Step 13 — Report

Present the result:

- **Context(s):** which contexts matched and why.
- **Stage:** the declared operational stage (prototype / mvp / production / critical). Every severity in the report is relative to this stage. State how the stage was determined (asked, project declaration, caller-provided) so the user can correct it.
- **Pillars foregrounded:** the 1–3 quality lenses the task is optimising for. Use these to order any ranked findings (e.g. "top gaps by risk") — a reliability-foregrounded task should rank reliability findings first.
- **Principles applied:** the principles from `foundations/15-principles/` each recommended pattern realises. Cite by ID. A finding without a principle citation is weaker than a finding with one.
- **Decision trees consulted:** which dtrees were used to pick between alternatives, and which options were kept vs. rejected.
- **Recommended patterns:** each selected pattern with a one-line rationale and, for review-shaped traversals, a code citation (`file:line` or a named file range) backing the status. Note which level the pattern comes from (foundation, org override, team override, or project override). Separate **current** patterns (stage floor met) from **deferred** patterns (stage floor above current stage) — deferred items are listed under a "When you graduate to stage X" sub-heading, not mixed in with current findings.
- **Prerequisites:** patterns that must be in place first, in dependency order.
- **Standards:** applicable constraints, noting which level they come from. Flag any that have been relaxed by a decision, with the reasoning.
- **Antipatterns to avoid:** relevant risks.
- **Conflicts and contradictions:** any unresolved issues, with both sides presented.
- **Existing solutions:** any matching or partial-match solutions from `foundations/30-solutions/`.
- **Gaps:** content that would have been useful but doesn't exist in Carta yet — missing patterns, missing contexts, missing principles, missing dtrees, and missing or stale edges between existing nodes.
- **Open questions:** decision inputs from step 4 that couldn't be answered.

If the decision is non-trivial, recommend recording it as an ADR at the appropriate level.

If the pattern combination is novel (not covered by any existing solution), consider proposing a capture (see `operations.md`).

---

## Principles

Three principles govern how an agent behaves during traversal:

1. **Don't fabricate.** If Carta lacks content for a decision, say so. Don't invent patterns, standards, or constraints that aren't in the knowledge base. Reporting a gap is more valuable than guessing.

2. **Don't decide silently.** When conflicts, contradictions, or ambiguities arise, present them to the user. The agent's job is to surface the relevant information and trade-offs, not to make the call.

3. **Prefer the graph over general knowledge.** If Carta has guidance on a topic, follow the graph — including its contradictions and constraints. If Carta is silent, the agent may draw on general knowledge but should flag that the recommendation is not grounded in the knowledge base.
