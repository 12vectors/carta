---
id: pattern-list-virtualisation
title: List Virtualisation
type: pattern
category: frontend
maturity: stable
pillars:
  - "[[pillar-performance]]"
tags: [pattern, stable, frontend, performance]
applies_to:
  - "[[context-web-application]]"
  - "[[context-internal-tool]]"
prerequisites: []
related:
  - "[[pattern-rendering-strategy]]"
conflicts_with: []
contradicted_by: []
sources:
  - "TanStack Virtual (Tanner Linsley): https://tanstack.com/virtual/latest"
  - "Rendering on the Web (Osmani & Miller, web.dev): https://web.dev/articles/rendering-on-the-web"
---

## When to use

- Lists, tables, or grids where visible row count is small but dataset size is hundreds+.
- Infinite-scroll experiences driven by long feeds (logs, messages, traces).
- Interactive tools (admin panels, spreadsheets) where users scroll through large datasets.
- When profile data shows the list DOM is the render-cost hot spot.

## When NOT to use

- Short, bounded lists — virtualisation adds complexity without payoff.
- Lists that must be fully present in the DOM (print, full-page find, screen reader scans of everything).
- Content with variable and unpredictable heights where measurement overhead outweighs the win.

## Decision inputs

- Median and maximum row count in realistic data.
- Row height stability — fixed, known, or measured on mount?
- Accessibility obligations — virtualised rows not in DOM can be invisible to assistive tech.
- Framework support — TanStack Virtual, react-window, react-virtualized, Vue/Solid equivalents.

## Solution sketch

Only render rows inside (or near) the viewport; recycle DOM nodes as the user scrolls.

```
Dataset: 10,000 rows
DOM:     ~20 rendered (visible + overscan buffer)
Scroll:  translate the rendered window as position changes
```

Fixed-height rows are cheapest. Variable heights require measuring and caching. Pair with keyboard-accessible scrolling (`aria-rowindex`, focus management) so screen readers don't lose the plot.

## Trade-offs

| Gain | Cost |
|------|------|
| Constant-time render cost regardless of dataset size | Accessibility needs extra care — virtualised rows are off-DOM |
| Memory and paint time collapse | Variable row heights require measurement infra |
| Makes in-browser filtering on large datasets viable | Scroll restoration, anchors, and print behave differently |

## Implementation checklist

- [ ] Pick a maintained library (TanStack Virtual, react-window) — rolling your own is rarely justified.
- [ ] Set overscan to smooth scroll; measure to tune.
- [ ] For variable heights, measure on mount and cache; invalidate on data change.
- [ ] Mark list semantics with `aria-rowcount` / `aria-rowindex` so assistive tech knows position.
- [ ] Test keyboard navigation; ensure focus and tab order survive virtualisation.
- [ ] Verify print and "find in page" behaviour; fall back if they matter.

## See also

- [[pattern-rendering-strategy]] — virtualisation is often the final optimisation after rendering choice.
- [[pattern-accessibility-baseline]] — the trade-off to keep an eye on.
- [[antipattern-unstable-list-key]] — virtualisation amplifies the damage.
