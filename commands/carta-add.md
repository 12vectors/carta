Draft a new Carta node following the writing rules, then validate it.

## Find Carta

Resolve the CARTA_PATH environment variable (run: `echo $CARTA_PATH`). This is the root of the Carta knowledge base. If unset, tell the user to configure it and stop.

CARTA_PATH should point to the repository root — the directory containing `foundations/`, and optionally `org/`, `teams/`, and `projects/`.

## Load the rules

**Before drafting anything**, read these files in full:

1. `CARTA_PATH/00-meta/writing-rules.md` — voice and length rules. These are non-negotiable.
2. `CARTA_PATH/00-meta/node-schema.md` — the frontmatter contract and required body sections.
3. The template for the node type being authored, from `CARTA_PATH/templates/`:
   - pattern → `tpl-pattern.md`
   - antipattern → `tpl-antipattern.md`
   - standard → `tpl-standard.md`
   - solution → `tpl-solution.md`
   - context → `tpl-context.md`
   - adr → `tpl-adr.md`

Do not skip this step. The writing rules exist precisely because agents left to their own devices write too much.

## Clarify before writing

Ask the user (if not already specified):

- **Node type.** pattern, antipattern, standard, solution, context, or adr.
- **Level.** foundation, org, team (which?), or project (which?).
- **Scope summary.** One sentence: what does this node assert?
- **Sources.** At least one verifiable source for `pattern`, `antipattern`, `solution`. Book + chapter, paper with DOI/URL, blog post with URL, public incident report, or named open-source project. No "team discussion" or "industry practice".

If the user cannot provide a source for a type that requires one, stop and ask them to supply one before drafting.

## Draft

Apply every rule in `writing-rules.md`. The ones most often violated:

- **Directive, not explanatory.** Don't teach the reader what the pattern is. Tell them when to use it and when not to.
- **Bullets over prose.** Default to bullets everywhere except `## Description`, `## Context`, `## Problem`, `## Rationale`.
- **Length caps.** Respect the per-section caps in `writing-rules.md`. When in doubt, cut.
- **Delegate depth to sources.** If a reader needs a full explanation, they follow the source link. Don't restate it.
- **No tutorials.** `Solution sketch` is a sketch. A minimal diagram or URI table is fine; a working implementation is not.
- **Frontmatter is the graph.** Spend effort on `applies_to`, `prerequisites`, `conflicts_with`, `mitigated_by`, etc. Keep the body thin.

Follow the filename conventions in `node-schema.md`:

- Foundation: `<id>.md` in the correct subdirectory. For patterns that is `foundations/20-patterns/styles/`, `foundations/20-patterns/tactics/<concern>/`, or `foundations/20-patterns/integration/` depending on the `category` value.
- Org: `<id>.org.md` under `org/{overrides,extensions,standards,decisions}/`.
- Team: `<id>.<team>.md` under `teams/<team>/...`.
- Project: `<id>.<project>.md` under `projects/<project>/...`.

## Place the file

Write the draft to the correct location based on type and level. Overrides require a co-located ADR at the same level — if the user is creating an override without an ADR, prompt them to author the ADR too (or agree to author it next).

## Validate

After writing the file, from CARTA_PATH, run:

```bash
python tools/validate.py --root .
python tools/lint.py --root .
```

Report:

1. **Validation errors** — must be fixed before the node is complete. Fix them and re-run until clean.
2. **Lint warnings** — especially any `Writing rule` warnings (length caps, bullet counts, explanatory phrases). Show the user each warning and offer to trim. Do not auto-trim without confirmation if the content is intentional.
3. **Gaps** — wikilinks in the new node that target nodes that don't exist yet. Note these as follow-up work.

## Finish

Summarise:

- File created (with path).
- Frontmatter highlights (type, level, key links).
- Lint warnings outstanding.
- Suggested follow-ups (missing linked nodes, co-required ADRs, etc.).

Do not commit unless the user asks — they curate.

## Task

$ARGUMENTS
