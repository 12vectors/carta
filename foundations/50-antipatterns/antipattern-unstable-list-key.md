---
id: antipattern-unstable-list-key
title: Unstable List Key
type: antipattern
category: frontend
maturity: stable
tags: [antipattern, stable, frontend, react]
applies_to:
  - "[[context-web-application]]"
mitigated_by: []
related:
  - "[[pattern-component-composition]]"
sources:
  - "React — Rendering Lists (keys, reconciliation): https://react.dev/learn/rendering-lists"
---

## How to recognise

- List items use `key={index}` or `key={Math.random()}`.
- Reordering or filtering a list produces wrong per-item state (selected flag, inline edits, scroll position).
- Inputs inside list items lose focus or draft text on re-render.
- Lists render fine until an item is inserted at the top, then state scrambles.
- Animations skip or double-play on list changes.

## Why it happens

- No stable ID on the domain object — developer reaches for index or random as a placeholder.
- Copy-pasted code from a tutorial that used index for illustration.
- Lists are rendered eagerly during prototyping; keys are "finalised later", never.
- Library-generated keys (e.g. from a hash) change on every render.

## Consequences

- Component instances are remounted or misidentified — state, focus, and animation break.
- Bugs reproduce only after a sort or filter, making them hard to diagnose.
- Virtualisation libraries (see [[pattern-list-virtualisation]]) misbehave because they rely on stable keys.
- Subtle data-loss bugs — the wrong edited row is saved because React tied the DOM to the wrong item.

## How to fix

- Use a stable, unique-per-sibling domain ID as the key (`item.id`, `user.uuid`).
- If the data lacks an ID, assign one at the boundary where the list is produced, not at render time.
- Never use `Math.random()` or `Date.now()` for keys.
- Use index only for lists that are append-only, never reorder, and whose items have no per-item state.

## See also

- [[pattern-component-composition]] — well-composed lists usually have a clearer place to keep IDs.
- [[pattern-list-virtualisation]] — amplifies this antipattern's damage.
