Traverse the Carta architectural knowledge base for the task below.

## Find Carta

Resolve the CARTA_PATH environment variable (run: echo $CARTA_PATH). This is the root of the Carta knowledge base. If unset, tell the user to configure it and stop.

If CARTA_PATH points to an organisation overlay, it will contain a `carta/` subdirectory (the generic core as a submodule). If it points directly to the generic core, there will be no `carta/` subdirectory.

Set two working references:
- CORE = CARTA_PATH/carta if that directory exists, otherwise CARTA_PATH itself
- OVERLAY = CARTA_PATH (only meaningful if CARTA_PATH contains overrides/, extensions/, stack/, or decisions/)

## Discover available content

List what exists at CORE and OVERLAY. Carta may be partially built — work only with what is present. The expected structure:

| Path | Contains |
|------|----------|
| CORE/10-contexts/ | System contexts (web app, pipeline, agentic system, ...) |
| CORE/20-patterns/ | Reusable architectural patterns by category |
| CORE/30-solutions/ | Composed patterns for common problems |
| CORE/40-standards/ | Non-negotiable practices |
| CORE/50-antipatterns/ | What not to do and why |
| CORE/90-decisions/ | Architecture Decision Records |
| OVERLAY/overrides/ | Org-specific pattern overrides (.override.md) |
| OVERLAY/extensions/ | Org-specific patterns not in core |
| OVERLAY/stack/ | Concrete technology choices |
| OVERLAY/decisions/ | Org-level ADRs |

Report briefly what directories exist so the user knows the scope of the traversal.

## Traverse

Work through these steps, skipping any that reference directories that don't exist:

1. **Context** — find the matching context in CORE/10-contexts/. Read it to get recommended_patterns links. If no context matches, state this and proceed pattern-by-pattern.

2. **Patterns** — for each candidate pattern in CORE/20-patterns/:
   - Check OVERLAY/overrides/ for a file named `<pattern-id>.override.md`. If it exists, read the override instead of the core node.
   - Read the frontmatter fields: applies_to, prerequisites, conflicts_with, contradicted_by.
   - Read "When to use" and "When NOT to use" to assess fit against the task.
   - Resolve prerequisites recursively — if pattern A requires pattern B, include B.

3. **Standards** — read CORE/40-standards/ and OVERLAY/standards/ for constraints that apply to this task. These are non-negotiable.

4. **Antipatterns** — scan CORE/50-antipatterns/ for pitfalls relevant to the task. Flag any that the candidate patterns risk triggering.

5. **Solutions** — check CORE/30-solutions/ for an existing composition that fits the task. Prefer a pre-composed solution over assembling patterns from scratch.

6. **Decisions** — check CORE/90-decisions/ and OVERLAY/decisions/ for ADRs that constrain or resolve the choice.

## Report

Structure your output as:

**Context**: which context(s) matched and why.

**Recommended patterns**: each pattern with a one-line rationale. Note which are core vs override.

**Prerequisites**: patterns that must be in place first.

**Standards**: applicable non-negotiable constraints.

**Avoid**: relevant antipatterns.

**Conflicts and contradictions**: any conflicts_with or contradicted_by edges found. Include the substance of the contradiction, not just the link.

**Gaps**: content that would have been useful but doesn't exist in Carta yet. This helps the team know what to author next.

Do not invent patterns, standards, or decisions that are not in the knowledge base. If Carta has insufficient content for the task, say so plainly and note what's missing.

## Task

$ARGUMENTS
