Traverse the Carta architectural knowledge base for the task below.

## Find Carta

Resolve the CARTA_PATH environment variable (run: echo $CARTA_PATH). This is the root of the Carta knowledge base. If unset, tell the user to configure it and stop.

CARTA_PATH should point to the repository root — the directory containing `foundations/`, and optionally `org/`, `teams/`, and `projects/`.

Set working references:
- FOUNDATIONS = CARTA_PATH/foundations
- ORG = CARTA_PATH/org
- TEAM = CARTA_PATH/teams/<team> if a team scope is specified or can be inferred from the current working directory
- PROJECT = CARTA_PATH/projects/<project> if a project scope is specified or can be inferred from the current working directory

## Discover available content

List what exists at each level. Carta may be partially built — work only with what is present. The expected structure:

| Path | Contains |
|------|----------|
| FOUNDATIONS/10-contexts/ | System contexts (web app, pipeline, agentic system, ...) |
| FOUNDATIONS/20-patterns/ | Reusable architectural patterns by category |
| FOUNDATIONS/30-solutions/ | Composed patterns for common problems |
| FOUNDATIONS/40-standards/ | Meta-standards and templates |
| FOUNDATIONS/50-antipatterns/ | What not to do and why |
| ORG/overrides/ | Org-specific pattern overrides (`.org.md` suffix) |
| ORG/extensions/ | Org-specific patterns not in foundations |
| ORG/standards/ | Org-level concrete standards |
| ORG/decisions/ | Org-level ADRs |
| TEAM/overrides/ | Team-specific pattern overrides (`.<team>.md` suffix) |
| TEAM/extensions/ | Team-specific patterns |
| TEAM/standards/ | Team-level standards |
| TEAM/decisions/ | Team-level ADRs |
| PROJECT/overrides/ | Project-specific pattern overrides (`.<project>.md` suffix) |
| PROJECT/extensions/ | Project-specific patterns |
| PROJECT/standards/ | Project-level standards |
| PROJECT/decisions/ | Project-level ADRs |

Report briefly what directories exist so the user knows the scope of the traversal.

## Traverse

Work through these steps, skipping any that reference directories that don't exist:

1. **Context** — find the matching context in FOUNDATIONS/10-contexts/. Read it to get recommended_patterns links. If no context matches, state this and proceed pattern-by-pattern.

2. **Patterns** — for each candidate pattern in FOUNDATIONS/20-patterns/:
   - Check for overrides in most-specific-first order: PROJECT/overrides/ → TEAM/overrides/ → ORG/overrides/. Override files use the level suffix convention: `<pattern-id>.org.md`, `<pattern-id>.<team>.md`, `<pattern-id>.<project>.md`. If an override exists, read it instead of the foundation node. Most specific wins.
   - Also check ORG/extensions/, TEAM/extensions/, and PROJECT/extensions/ for additional patterns relevant to the task.
   - Read the frontmatter fields: applies_to, prerequisites, conflicts_with, contradicted_by.
   - Read "When to use" and "When NOT to use" to assess fit against the task.
   - Resolve prerequisites recursively — if pattern A requires pattern B, include B.

3. **Standards** — read FOUNDATIONS/40-standards/, ORG/standards/, TEAM/standards/, and PROJECT/standards/ for constraints that apply to this task. Check whether any decision explicitly relaxes a standard — if so, note the relaxation and reasoning.

4. **Antipatterns** — scan FOUNDATIONS/50-antipatterns/ and extensions for pitfalls relevant to the task. Flag any that the candidate patterns risk triggering.

5. **Solutions** — check FOUNDATIONS/30-solutions/ for an existing composition that fits the task. Prefer a pre-composed solution over assembling patterns from scratch.

6. **Decisions** — check ORG/decisions/, TEAM/decisions/, and PROJECT/decisions/ for ADRs that constrain or resolve the choice. More specific levels take precedence: project → team → org when they cover the same concern.

## Report

Structure your output as:

**Context**: which context(s) matched and why.

**Recommended patterns**: each pattern with a one-line rationale. Note which are foundation, org override, team override, or project override.

**Prerequisites**: patterns that must be in place first.

**Standards**: applicable constraints, noting which level they come from. Flag any that have been relaxed by a decision.

**Avoid**: relevant antipatterns.

**Conflicts and contradictions**: any conflicts_with or contradicted_by edges found. Include the substance of the contradiction, not just the link.

**Gaps**: content that would have been useful but doesn't exist in Carta yet. This helps the team know what to author next.

Do not invent patterns, standards, or decisions that are not in the knowledge base. If Carta has insufficient content for the task, say so plainly and note what's missing.

## Task

$ARGUMENTS
