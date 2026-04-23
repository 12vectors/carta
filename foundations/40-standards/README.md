# Foundations / Standards

This directory is **intentionally sparse**. Per `CHARTER.md` §"Standards in the foundations", `foundations/40-standards/` holds only:

- **Meta-standards** — guidance on how to write standards well (e.g. "every standard must specify what failure to comply looks like and what the remediation is").
- **Templates** — the structural form a standard should take (frontmatter schema, required sections, enforceability levels).
- **Cross-cutting concerns** — practices so universally agreed that they meet all five admission criteria (e.g. "secrets must not be committed to version control"). These are rare.

**Opinionated standards** — API design conventions, naming rules, testing requirements, version policies — are organisational, team, or project choices. They live at the levels where those choices are made:

- `org/standards/`
- `teams/<team>/standards/`
- `projects/<project>/standards/`

A worked example of the pattern is `org/standards/standard-api-versioning.org.md`, which the Carta starter ships with. That file illustrates the shape an opinionated standard should take; its content is an example choice, not a foundation-level mandate.

If you find yourself wanting to add an opinionated standard to `foundations/40-standards/`, stop and consider whether the standard genuinely generalises across organisations and stacks. If it names a specific stack, vendor, framework, or language, it belongs in an organisation level.

See `CHARTER.md` for the full admission criteria.
