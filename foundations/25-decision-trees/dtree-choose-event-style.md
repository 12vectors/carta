---
id: dtree-choose-event-style
title: Choose an Event Style
type: decision-tree
maturity: stable
tags: [decision-tree, stable, events, integration]
decides_between:
  - "[[pattern-event-notification]]"
  - "[[pattern-event-carried-state-transfer]]"
  - "[[pattern-event-sourcing]]"
criteria:
  - "Consumer autonomy required (callback-free or not)"
  - "Payload size and volatility"
  - "Source-of-truth location (single authoritative store vs. local views)"
  - "Audit and replay requirements"
  - "Eventual-consistency tolerance"
related_patterns:
  - "[[pattern-event-driven-architecture]]"
  - "[[pattern-publish-subscribe]]"
---

## Problem

You've chosen events as the communication shape. Now choose what an event carries: a notification that something happened (pointer), a snapshot of state at the time it happened, or the full sequence of domain events.

## Criteria

- **Consumer autonomy required** — can consumers work without calling back to the producer?
- **Payload size and volatility** — small stable payload, or large frequently-changing state?
- **Source-of-truth location** — is there a single authoritative store, or do consumers build their own views?
- **Audit and replay requirements** — do you need "what was the state at time T" or event history for compliance?
- **Eventual-consistency tolerance** — how stale can a consumer's view legitimately be?

## Recommendation

| Situation | Choose |
|---|---|
| "Something happened — look it up if you need details", small payload, producer is authoritative | [[pattern-event-notification]] |
| Consumers want autonomy and don't want to call back; state fits in the event | [[pattern-event-carried-state-transfer]] |
| Domain needs full audit, replay, or temporal queries; log is the source of truth | [[pattern-event-sourcing]] |
| System-wide async integration across many consumers | [[pattern-publish-subscribe]] as the channel, one of the above as the payload style |

These are not mutually exclusive at system level — different event topics can use different styles. Mixing is fine if each topic is consistent.

## Fallback

Default to event notification. It is the lowest-commitment, lightest-payload option and leaves the producer authoritative. Upgrade to event-carried state transfer only when callback traffic becomes a measurable problem; upgrade to event sourcing only when audit or replay is a real domain requirement, not aspiration.
