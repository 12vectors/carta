# Operations

Carta defines four operations performed on the knowledge base. Each operation has a trigger, a procedure, a set of permitted actors, and a logging requirement.

All operations are logged in `LOG.md`. See **Logging** at the bottom of this document.

---

## Traverse

The primary operation. An agent with a task consults Carta to select patterns, check constraints, and compose a solution.

**Trigger:** an agent or human needs to make an architectural decision.

**Actor:** agent or human. No review required — traversal is read-only.

**Procedure:** see `traversal-protocol.md` for the full algorithm. Summary:

1. Consult `DECISION_TREE.md` to identify the relevant context(s).
2. From the context, follow `recommended_patterns` links to build a candidate set.
3. For each candidate, check fit (`When to use`, `When NOT to use`), prerequisites, conflicts, and contradictions.
4. Cross-reference standards and antipatterns.
5. Prefer pre-composed solutions from `foundations/30-solutions/` when available.
6. Check ADRs for constraints.
7. Report the recommended patterns with rationale.

**Output:** a recommendation — which patterns to apply, which to avoid, what prerequisites to satisfy, and what conflicts exist. If the decision is non-trivial, the traversal may also produce a new ADR (see **Recording a decision** in `CHARTER.md`).

**Log entry format:**
```
## [YYYY-MM-DD] traverse | <task summary>
Traversed: <context(s)> → <selected patterns>
ADR created: <adr filename, if any>
```

---

## Ingest

When a new ADR is committed, a pattern is added or changed, or an architectural decision is made outside Carta, the effects must be propagated across the graph.

**Trigger:** a merged PR that adds or modifies a node, or an external decision that needs to be reflected in the graph.

**Actor:** agent (proposes), human (reviews and merges). Agents must not merge their own ingest PRs.

**Procedure:**

1. Identify the triggering event (new ADR, modified pattern, external decision).
2. Determine which existing nodes are affected:
   - Nodes whose `contradicted_by` should be updated.
   - Nodes whose `maturity` may need to change.
   - Solutions whose `composes` list may need revision.
   - Contexts whose `recommended_patterns` may need updating.
   - Standards that may need new scope or exceptions.
3. For each affected node, draft the frontmatter and/or body changes.
4. Open a PR with all changes. The PR description must:
   - Name the triggering event.
   - List every affected node and what changed.
   - Explain why each change follows from the trigger.
5. A human reviews and merges.

**Output:** a PR updating affected nodes. Once merged, the graph is consistent with the new decision.

**Log entry format:**
```
## [YYYY-MM-DD] ingest | <trigger summary>
Trigger: <triggering node or event>
Updated: <node> (<what changed>)
Updated: <node> (<what changed>)
...
```

---

## Lint

A health check of the graph. Lint detects structural and semantic issues that degrade the knowledge base over time.

**Trigger:** periodic (scheduled), on-demand (manual run), or as part of a traversal when the agent notices inconsistencies.

**Actor:** agent or human (runs the check), human (decides what to fix). Agents may open PRs to fix issues found by lint, subject to the same review rules as ingest.

**Procedure:**

Run `tools/lint.py` or perform the equivalent checks manually. The lint operation checks for:

| Check | Description | Severity |
|-------|-------------|----------|
| Contradictions | Nodes whose claims conflict but aren't linked via `contradicted_by`. | error |
| Stale nodes | Patterns whose `sources` are all older than five years with no currency justification. | warning |
| Orphans | Nodes with no inbound links — nothing references them. | warning |
| Broken prerequisites | Circular or dangling prerequisite chains. | error |
| Missing pages | Concepts referenced in wikilinks but lacking their own node. | warning |
| Ungrounded patterns | Nodes with an empty `sources` field where required. | error |
| Phantom conflicts | `conflicts_with` edges that no longer hold after a recent ADR. | warning |
| Bidirectionality | `contradicted_by` links that exist in one direction but not the other. | error |
| Tag consistency | `tags` field missing the `type` or `maturity` value. | error |
| ID mismatch | `id` field doesn't match the filename. | error |

Severity levels:
- **error** — must be fixed before merge. `tools/validate.py` catches these in CI.
- **warning** — should be addressed but doesn't block merging. Tracked in lint reports.

**Output:** a lint report listing issues by severity. May be followed by a PR to fix the issues found.

**Log entry format:**
```
## [YYYY-MM-DD] lint | <trigger or "Periodic health check">
Errors: <count> (<summary>)
Warnings: <count> (<summary>)
<detail lines as needed>
```

---

## Capture

When a traversal produces a novel composition — patterns combined in a way not yet recorded in `foundations/30-solutions/` — the composition is captured as a new solution node.

Capture is how Carta compounds. Without it, useful pattern combinations discovered during real work disappear into chat history.

**Trigger:** a traversal that combines patterns in a way not covered by any existing solution in `foundations/30-solutions/`.

**Actor:** agent (drafts the solution node), human (reviews and merges).

**Procedure:**

1. During or after a traversal, the agent identifies that the recommended pattern set constitutes a novel composition.
2. The agent checks `foundations/30-solutions/` to confirm no existing solution covers this combination.
3. The agent drafts a new solution node following the schema in `node-schema.md`:
   - `composes` lists the patterns in implementation order.
   - `applies_to` lists the relevant contexts.
   - The body explains how the patterns fit together, not just what they are.
4. The agent opens a PR with the new solution node.
5. A human reviews. The solution must meet the same admission criteria as any other node (see `CHARTER.md`).

Not every traversal warrants a capture. Captures are for compositions that are **reusable** — likely to recur across tasks and teams. A one-off combination that's too specific to a single project belongs in an organisation, team, or project layer, not the foundations.

**Output:** a PR proposing a new solution node.

**Log entry format:**
```
## [YYYY-MM-DD] capture | <solution summary>
Origin: task "<originating task>"
Created: <solution filename>
Composed: <pattern> + <pattern> + ...
```

---

## Logging

Every operation is logged in `LOG.md` at the repository root. Entries are append-only and chronologically ordered, newest first.

Each entry starts with a consistent prefix:

```
## [YYYY-MM-DD] <operation> | <summary>
```

This format is parseable by both agents and simple tools:
- `grep "^## \[" LOG.md | head -10` shows the last 10 operations.
- `grep "traverse" LOG.md` shows all traversals.
- Agents read the log to understand recent activity and avoid redundant work.

The `LOG.md` tracks all operations across foundations, organisation, team, and project layers.
