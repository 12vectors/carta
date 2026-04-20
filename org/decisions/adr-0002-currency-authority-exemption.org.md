---
id: adr-0002-currency-authority-exemption
title: Relax Currency rule for authoritative, generic sources
type: adr
status: accepted
date: 2026-04-20
maturity: stable
tags: [adr, stable, charter-amendment, currency]
affects:
  - "[[CHARTER]]"
supersedes: ""
superseded_by: ""
---

## Context

Carta's foundations enforce a Currency admission criterion (CHARTER §Form criteria 5). As originally drafted, any source older than five years required an explicit note confirming the pattern still holds.

Seeding the foundations surfaced the friction. Canonical works like Fowler's *Patterns of Enterprise Application Architecture* (2002), Hohpe & Woolf's *Enterprise Integration Patterns* (2003), and Cockburn's *Hexagonal Architecture* (2005) ground a meaningful fraction of the pattern catalogue. The principles they describe have not moved; the tech stack around them has. Forcing a "still relevant because…" note on every citation of these works creates boilerplate without protecting the reader.

The risk the rule was designed to mitigate — patterns decaying as the field moves on — is real for implementation-specific or fast-moving-domain guidance (cloud idioms, LLM agents, modern data infra) but not for shape-level patterns from canonical authors.

## Decision

Amend CHARTER §Form criteria 5 (Currency). Sources older than five years are accepted without a justification note when both conditions hold:

1. The author is canonical in the domain (initial set: Fowler, Hohpe, Nygard, Evans, Kleppmann, Cockburn).
2. The pattern is stack-agnostic and shape-level.

Patterns touching fast-moving territory — specific cloud or framework idioms, LLM agents, modern data infrastructure — require a Currency note regardless of author age.

The canonical-author list is maintainable: additions happen via a new ADR, not silent expansion.

## Consequences

**Positive.**
- Admission friction drops for ~30% of the seeded inventory (EIP messaging, PoEAA-derived data patterns, hexagonal architecture).
- PRs stay focused on substantive criteria (Decidability, Coherence) rather than Currency boilerplate.
- The "fast-moving territory" carve-out preserves the rule's intent where it mattered most.

**Negative.**
- Adds a judgement call — "is this author canonical?" — mitigated by the enumerated initial list.
- Creates a small asymmetry: two same-age citations may be treated differently based on authorship.

**Neutral.**
- Lint's Currency check still enforces the rule for non-exempt sources; demotion path unchanged.

## Alternatives considered

- **Raise the threshold to ten years.** Would still force notes on PoEAA and EIP. Rejected — the issue is not the number but the mismatch between age and relevance for canonical works.
- **Remove the Currency rule entirely.** Rejected — it provides real protection against stale guidance in fast-moving domains.
- **Apply the exemption per-source rather than per-author.** Operationally heavier and harder to explain. The per-author list is a compact proxy.
