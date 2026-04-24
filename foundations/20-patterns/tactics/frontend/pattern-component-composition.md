---
id: pattern-component-composition
title: Component Composition
type: pattern
category: frontend
maturity: stable
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, frontend, architecture]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-state-colocation]]"
  - "[[pattern-error-boundary]]"
conflicts_with: []
contradicted_by: []
sources:
  - "React — Passing Props to a Component: https://react.dev/learn/passing-props-to-a-component"
  - "When to break up a component into multiple components (Kent C. Dodds, 2019): https://kentcdodds.com/blog/when-to-break-up-a-component-into-multiple-components"
---

## When to use

- A component has become hard to navigate, test, or reason about — it is now the pain, not the features inside it.
- Repeated structural patterns (layout + content) benefit from a reusable shell with `children` slots.
- You need two pieces of UI to share layout/behaviour but not state.
- Prop drilling is obscuring intent (see [[antipattern-prop-drilling]]).

## When NOT to use

- Early — don't pre-split because "this component feels big". Dodds: duplication is cheaper than the wrong abstraction.
- When splitting requires passing more props than the original component's API.
- To satisfy an arbitrary line-count rule; behaviour cohesion matters more than size.
- Component-per-element splitting — that's fragmentation, not composition.

## Decision inputs

- Is there a *second* caller or caller-shape that would reuse the extracted part?
- Is the extracted piece a stable boundary (layout/shell) or caller-specific logic?
- Can the split be done without sprouting a prop-forwarding chain?
- Would the split let a test target a narrower surface?

## Solution sketch

Compose via `children`, slot props, or render props rather than prop chains.

```jsx
// Shell exposes slots; callers fill them
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>{content}</Card.Body>
</Card>
```

Split when one of the following is true: duplication is real, the sub-tree has its own lifecycle, or testing the whole in isolation is painful. Otherwise, leave it.

## Trade-offs

| Gain | Cost |
|------|------|
| Reusable shells without duplicating layout or logic | Compound components need a consistent API convention |
| Smaller test surfaces per unit | Over-splitting fragments state and scatters related behaviour |
| Composition boundaries often align with [[pattern-error-boundary]] placement | Early splits solidify the wrong abstraction |

## Implementation checklist

- [ ] Wait for a concrete trigger (duplication, test pain, independent lifecycle) before splitting.
- [ ] Prefer `children` or slot props to parameter chains.
- [ ] Co-locate the tests and types alongside each composed piece.
- [ ] Keep state where it's used — pair with [[pattern-state-colocation]].
- [ ] Avoid forwarding props through three or more levels; that's [[antipattern-prop-drilling]].

## See also

- [[pattern-state-colocation]] — complementary guideline.
- [[antipattern-prop-drilling]] — the failure mode that often drives composition.
