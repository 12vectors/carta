---
id: pattern-rendering-strategy
title: Rendering Strategy
type: pattern
category: frontend
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, frontend, performance, rendering]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-list-virtualisation]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Rendering on the Web (Addy Osmani & Jason Miller, 2019, web.dev): https://web.dev/articles/rendering-on-the-web"
  - "Islands Architecture (Jason Miller, 2020): https://jasonformat.com/islands-architecture/"
---

## When to use

- Any time you are starting a new web application and must pick a rendering default.
- When Core Web Vitals (LCP, INP, CLS) are materially failing and the base architecture is the root cause.
- When SEO, first-paint, or time-to-interactive drive revenue and current rendering misses them.
- When bundle size has crept into territory that punishes every visitor on slower networks.

## When NOT to use

- Private authenticated dashboards where SEO and first-paint matter less than interactivity.
- Tiny internal tools where CSR with a bundler default is fine and debate is waste.
- Prototype-stage builds — defer the choice; revisit at MVP.

## Decision inputs

- Content freshness — is it static per build, per request, per user, or live?
- SEO requirement — do search engines need to index the rendered output?
- Interactivity — is most of the page static with a few interactive widgets, or fully dynamic?
- Data source — do you need per-request server data (auth, personalisation)?
- Team expertise and hosting target (edge, node server, static CDN).

## Solution sketch

| Strategy | Renders | Best for |
|----------|---------|----------|
| CSR (client-side) | Browser | Authenticated apps, tight interactivity, SEO not required |
| SSR (server-side) | Server per request | Personalised pages, SEO matters, fresh data |
| SSG (static) | Build time | Marketing, docs, rarely-changing content, best cost |
| ISR / revalidate | Build + periodic re-render | SSG where content changes slowly but not never |
| Islands | Server HTML + per-widget hydration | Mostly-static pages with a few interactive regions |

See Osmani & Miller for the trade-off tree; Miller for islands in detail.

## Trade-offs

| Gain | Cost |
|------|------|
| Pick a strategy that matches content dynamics → best Core Web Vitals | Mixing strategies in one app multiplies complexity |
| Islands and SSG ship less JS, cheaper and faster | Requires framework support (Astro, Remix, Next.js patterns) |
| SSR personalises without sacrificing first-paint | Server compute cost per request |

## Implementation checklist

- [ ] Classify each page or route by content freshness and SEO need.
- [ ] Default static to SSG; default dynamic to SSR; reserve CSR for authenticated-only routes.
- [ ] For mostly-static-with-islands pages, prefer Astro or similar over a full CSR framework.
- [ ] Pair with [[pattern-list-virtualisation]] when long lists dominate the page.
- [ ] Measure LCP, INP, CLS in production; reassess if the chosen strategy isn't hitting them.
- [ ] Document the chosen strategy per route — future contributors shouldn't have to reverse-engineer it.

## See also

- [[pattern-list-virtualisation]] — complementary performance tactic.
- [[pattern-component-composition]] — rendering strategy shapes where composition boundaries matter.
