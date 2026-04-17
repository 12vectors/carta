# Traversal Protocol

The algorithm an agent follows when consulting Carta to make an architectural decision. This is the normative reference for the traverse operation described in `operations.md`.

---

## Prerequisites

Before traversing, the agent must know:

1. **The task or goal.** What architectural decision needs to be made. This comes from the user, a spec, or an upstream workflow.
2. **The Carta root.** Where the knowledge base lives on disk. This is the repository root, which contains `foundations/`, `org/`, and optionally `teams/` and `projects/`.
3. **The scope (if any).** Which team and/or project to include in the traversal. If no scope is specified, the traversal uses only foundation and organisation levels.

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

## Algorithm

### Step 1 — Identify contexts

Read `DECISION_TREE.md`. Match the task against the signal table to identify one or more relevant contexts from `foundations/10-contexts/`.

- Multiple contexts may apply. Include all that match.
- If no context matches, follow the fallback procedure in `DECISION_TREE.md` (check if the task is architectural, note missing contexts, or proceed pattern-by-pattern).

### Step 2 — Build the candidate set

For each matched context, read its node file in `foundations/10-contexts/`. Collect all entries from its `recommended_patterns` field. The union across all matched contexts is the initial candidate set.

Also scan extensions at all applicable levels — `org/extensions/`, `teams/<team>/extensions/` (if scoped), `projects/<project>/extensions/` (if scoped) — for additional patterns whose `applies_to` includes the matched contexts. Add these to the candidate set.

If proceeding without a context (fallback), build the candidate set by scanning `foundations/20-patterns/` categories relevant to the task, plus any relevant extensions.

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

### Step 7 — Check contradictions

For each remaining candidate, read its `contradicted_by` field. For each contradiction:

1. Read the contradicting node to understand the substance of the disagreement.
2. Check whether an ADR resolves the contradiction for this context.
3. If resolved, follow the ADR. If unresolved, present the contradiction to the user with both sides.

Contradictions are informational, not eliminative. A pattern with an unresolved contradiction is still a valid candidate — the user just needs to know about the disagreement.

### Step 8 — Cross-reference standards

Collect standards from all applicable levels:

1. Read `foundations/40-standards/` — meta-standards and cross-cutting concerns.
2. Read `org/standards/` — org-level standards.
3. If a team is scoped, read `teams/<team>/standards/` — team-level standards.
4. If a project is scoped, read `projects/<project>/standards/` — project-level standards.

For each standard whose `applies_to` includes the matched contexts (or that has no `applies_to`, meaning it's universal):

1. Check whether any candidate pattern violates the standard.
2. If so, flag the violation. Check whether a decision at any level explicitly relaxes the standard for this context. If a decision exists, note the relaxation and its reasoning. If not, the violation must be resolved.

### Step 9 — Cross-reference antipatterns

Read all antipattern nodes in `foundations/50-antipatterns/` whose `applies_to` includes the matched contexts. Also check extensions at all applicable levels for additional antipatterns.

For each:

1. Check whether the candidate set risks triggering the antipattern.
2. If so, flag it with the antipattern's `How to recognise` signals and `How to fix` guidance.

This is a negative filter. Antipatterns don't add to the candidate set; they flag risks in it.

### Step 10 — Check for existing solutions

Read `foundations/30-solutions/` and check whether any existing solution's `composes` list is a subset or match of the current candidate set.

- If an exact or near-exact match exists, prefer the pre-composed solution. It includes integration guidance (how the patterns fit together) that the individual pattern nodes don't.
- If a partial match exists, note it — the existing solution may cover part of the task.

### Step 11 — Check ADRs

Collect decisions from all applicable levels:

1. Read `org/decisions/`.
2. If a team is scoped, read `teams/<team>/decisions/`.
3. If a project is scoped, read `projects/<project>/decisions/`.

For each ADR whose `affects` list includes any candidate pattern or matched context:

1. If the ADR is `accepted`, its constraints apply. Adjust the candidate set accordingly.
2. If the ADR is `superseded`, follow the superseding ADR instead.
3. If the ADR is `proposed`, note it as pending — the decision isn't final.

More specific decisions take precedence when they cover the same concern (project > team > org).

### Step 12 — Report

Present the result:

- **Context(s):** which contexts matched and why.
- **Recommended patterns:** each selected pattern with a one-line rationale. Note which level it comes from (foundation, org override, team override, or project override).
- **Prerequisites:** patterns that must be in place first, in dependency order.
- **Standards:** applicable constraints, noting which level they come from. Flag any that have been relaxed by a decision, with the reasoning.
- **Antipatterns to avoid:** relevant risks.
- **Conflicts and contradictions:** any unresolved issues, with both sides presented.
- **Existing solutions:** any matching or partial-match solutions from `foundations/30-solutions/`.
- **Gaps:** content that would have been useful but doesn't exist in Carta yet.
- **Open questions:** decision inputs from step 4 that couldn't be answered.

If the decision is non-trivial, recommend recording it as an ADR at the appropriate level.

If the pattern combination is novel (not covered by any existing solution), consider proposing a capture (see `operations.md`).

---

## Principles

Three principles govern how an agent behaves during traversal:

1. **Don't fabricate.** If Carta lacks content for a decision, say so. Don't invent patterns, standards, or constraints that aren't in the knowledge base. Reporting a gap is more valuable than guessing.

2. **Don't decide silently.** When conflicts, contradictions, or ambiguities arise, present them to the user. The agent's job is to surface the relevant information and trade-offs, not to make the call.

3. **Prefer the graph over general knowledge.** If Carta has guidance on a topic, follow the graph — including its contradictions and constraints. If Carta is silent, the agent may draw on general knowledge but should flag that the recommendation is not grounded in the knowledge base.
