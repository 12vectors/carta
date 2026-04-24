---
id: pattern-state-colocation
title: State Colocation
type: pattern
category: frontend
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, frontend, state, react]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-component-composition]]"
conflicts_with: []
contradicted_by: []
sources:
  - "State Colocation will make your React app faster (Kent C. Dodds, 2019): https://kentcdodds.com/blog/state-colocation-will-make-your-react-app-faster"
---

## When to use

- New state: place it at the lowest common ancestor of its users, not in a global store by default.
- Auditing a global store — most state there is used by one subtree.
- Performance work — lifted state triggers unnecessary renders across unrelated components.
- After onboarding a state-management library and watching re-render counts explode.

## When NOT to use

- State that genuinely spans unrelated branches of the tree (auth, theme, feature flags).
- Server-synchronised state — use a data-fetching library (TanStack Query, SWR) rather than hand-roll.
- Cross-cutting concerns better expressed via context with narrow providers.

## Decision inputs

- How many components read or write this state?
- Do they share a reasonable common ancestor below the root?
- Does this state survive navigation or page reload?
- Are there render-cost hot spots tied to state at the wrong level?

## Solution sketch

Start local. Lift only when a second consumer appears — and lift only to the nearest ancestor.

```
Before:  <App store={everything}> → every child re-renders on any state change
After:   state lives inside <EditPanel>; <Sidebar> doesn't re-render when edits happen
```

Dodds' rule: "the state should live as close to the components that use it as possible."

## Trade-offs

| Gain | Cost |
|------|------|
| Fewer unnecessary renders across unrelated subtrees | Lifting later is manual work each time a second consumer shows up |
| Easier reasoning — state is visible where it is used | Component boundaries must be set up to accept the lifted state |
| Smaller surface for state bugs | No single source-of-truth convenience; devs must know where to look |

## Implementation checklist

- [ ] Default new state to `useState` inside the component that uses it.
- [ ] Lift only when a second reader/writer appears; lift to the nearest common ancestor.
- [ ] Reserve global stores for genuinely cross-tree state (auth, theme, i18n).
- [ ] Prefer data-fetching libraries for server state, not hand-rolled state.
- [ ] Profile renders; investigate any global store write that re-renders components not using it.

## See also

- [[pattern-component-composition]] — structural partner; composition sets up the ancestor that state lives in.
- [[antipattern-prop-drilling]] — the failure mode when colocation is over-applied.
