---
id: pattern-test-data-builder
title: Test Data Builder
type: pattern
category: testing
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, testing, fixtures]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
prerequisites: []
related:
  - "[[pattern-test-pyramid]]"
  - "[[pattern-test-double]]"
conflicts_with: []
contradicted_by: []
sources:
  - "xUnit Test Patterns (Gerard Meszaros, Addison-Wesley 2007) — Test Data Builder, Object Mother"
  - "Growing Object-Oriented Software, Guided by Tests (Freeman & Pryce, Addison-Wesley 2009)"
---

## When to use

- Test setup for a domain object is verbose, repetitive, or brittle across many tests.
- A test's intent is drowned by irrelevant field construction.
- The same fixture recurs across many tests with small per-test variations.
- ORM factories can't flex enough without bloating the production model.

## When NOT to use

- One or two fields to set — a literal constructor is clearer.
- Tests for the value object's construction itself — builders hide what you're verifying.
- Fixtures that must match production data exactly — use recorded fixtures or snapshots.

## Decision inputs

- How many construction fields are required vs defaulted?
- How often does a given fixture recur across the suite?
- In-language builder vs persistence-aware factory (factory_bot, Bogus, AutoFixture)?
- Where do builders live — production module or isolated test support?

## Solution sketch

A builder exposes a fluent API with sane defaults; tests override only what matters.

```
orderBuilder().withStatus(PAID).withCustomer(aCustomer()).build()
```

Prefer composition — `aCustomer()` returns a prebuilt customer, letting the test's intent live in one line. Keep builders in a shared test-support module (GOOS ch. 22).

## Trade-offs

| Gain | Cost |
|------|------|
| Tests read like domain sentences, not construction boilerplate | Another layer to maintain alongside the model |
| Fixture changes land in one place, not every test | Over-broad builders hide meaningful fixture differences |
| Composable — builders nest inside other builder calls | Lazy builders can mask invalid states production would reject |

## Implementation checklist

- [ ] Start with defaults that produce a valid, production-legal object.
- [ ] Expose `withX` methods returning the builder (pick mutable or immutable).
- [ ] Nest builders rather than pass raw primitives across types.
- [ ] Keep builders in test-support; never import them from production code.
- [ ] Fail fast if defaults produce an invalid instance.

## See also

- [[pattern-test-pyramid]] — builders mostly serve the base and mid layers.
- [[pattern-test-double]] — often wraps stubs/fakes to hide setup.
