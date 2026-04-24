---
id: pattern-accessibility-baseline
title: Accessibility Baseline
type: pattern
category: frontend
maturity: stable
stage_floor: mvp
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, frontend, accessibility, a11y]
applies_to:
  - "[[context-web-application]]"
  - "[[context-internal-tool]]"
prerequisites: []
related:
  - "[[pattern-component-composition]]"
  - "[[pattern-list-virtualisation]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Web Content Accessibility Guidelines (WCAG) 2.1, W3C Recommendation (2018, updated 2025): https://www.w3.org/TR/WCAG21/"
  - "The A11Y Project: https://www.a11yproject.com/"
  - "Resilient Web Design (Jeremy Keith, 2016): https://resilientwebdesign.com/"
---

## When to use

- Any public-facing web product — accessibility is table stakes, not a feature.
- Internal tools used by diverse workforces (enterprise, government, healthcare).
- Regulated markets — EU, UK, US public sector require WCAG conformance.
- Any product where form completion, navigation, or information access is the job.

## When NOT to use

- Prototype-stage spikes testing a throwaway idea (but ship nothing to real users without revisiting).
- Highly specialised visual-only tools (CAD, 3D modelling) where WCAG guidance is weaker — even then, apply what does apply.

## Decision inputs

- Target conformance level (WCAG 2.1 A, AA, AAA — AA is typical floor).
- Regulatory driver (EAA, Section 508, provincial laws).
- Automated-tooling budget (axe-core, Lighthouse, Pa11y).
- Testing with assistive tech (screen readers, keyboard-only users) — automated checks catch <40%.

## Solution sketch

Floor the product on four pillars, per WCAG:

- **Perceivable** — alt text, captions, sufficient colour contrast (4.5:1 body text).
- **Operable** — full keyboard navigation, visible focus indicators, no keyboard traps.
- **Understandable** — labelled form fields, error messages that identify the error and a fix.
- **Robust** — valid semantic HTML; ARIA only when HTML can't express the role.

Use native elements first (`<button>`, `<a>`, `<label>`), ARIA second. Progressive enhancement (Keith) — the page works without JS, enhances with it.

## Trade-offs

| Gain | Cost |
|------|------|
| Reaches every user, including assistive-tech users | Requires discipline through the whole component lifecycle, not a late audit |
| Better SEO and keyboard UX as a side effect | Design freedom is constrained — visual-only affordances need alternatives |
| Reduces legal exposure in regulated markets | Testing with real assistive tech is learned, not automated |

## Implementation checklist

- [ ] Run axe-core (or equivalent) on every page in CI; block merges on new violations.
- [ ] Prefer semantic HTML elements; introduce ARIA only when necessary.
- [ ] Label every form field (`<label for>` or `aria-label`); associate error messages with fields.
- [ ] Test every flow keyboard-only without touching a mouse.
- [ ] Enforce colour-contrast ratios in design tokens, not just CSS.
- [ ] Include one screen-reader pass per release (VoiceOver, NVDA, JAWS rotation).

## See also

- [[pattern-component-composition]] — shared shells are the right place to bake in semantics.
- [[pattern-list-virtualisation]] — virtualisation easily breaks a11y; audit together.
