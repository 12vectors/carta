---
id: antipattern-prop-drilling
title: Prop Drilling
type: antipattern
category: frontend
maturity: stable
tags: [antipattern, stable, frontend, react]
applies_to:
  - "[[context-web-application]]"
mitigated_by:
  - "[[pattern-component-composition]]"
  - "[[pattern-state-colocation]]"
related: []
sources:
  - "When to break up a component into multiple components (Kent C. Dodds, 2019): https://kentcdodds.com/blog/when-to-break-up-a-component-into-multiple-components"
  - "State Colocation (Kent C. Dodds, 2019): https://kentcdodds.com/blog/state-colocation-will-make-your-react-app-faster"
---

## How to recognise

- The same prop travels through three or more components before reaching the consumer.
- Intermediate components accept props they don't use, just to forward them.
- Refactors touch many files whenever a single prop's shape changes.
- Component signatures balloon with pass-through props.
- Developers reach for a global store "because props are annoying".

## Why it happens

- State was lifted too high — often to the app root — without considering composition.
- Intermediate components couple to props they shouldn't know about.
- No slot or `children` composition — every level has to be a parameter stop.
- Team treats "context" as scary and avoids it even where it fits.

## Consequences

- Change amplification — one prop rename costs many file edits.
- Components lose reusability — they can only be used inside the drill path.
- Re-renders cascade because state lives at a high ancestor; siblings re-render on irrelevant changes.
- Developers over-correct by lifting everything to a global store — a different failure mode.

## How to fix

- Apply [[pattern-state-colocation]] — move state down to its nearest common ancestor.
- Apply [[pattern-component-composition]] — pass `children` or slots instead of prop chains.
- Use context narrowly for genuinely cross-cutting values (auth, theme); don't use it for everything.
- For server state, use a data-fetching library so components read directly instead of drilling.

## See also

- [[pattern-state-colocation]] — primary structural fix.
- [[pattern-component-composition]] — partner fix that removes the drill stops.
