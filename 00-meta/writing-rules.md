# Writing Rules

Rules for authoring Carta nodes. The goal is **directive brevity** — just enough for a coding agent to make a decision, with sources for anyone who needs depth.

These rules are soft-enforced: `tools/lint.py` warns when content exceeds the thresholds below. Warnings are signals, not blockers.

---

## The core rule

**Carta tells you *what to do* in *which context*. Not *what a pattern is* or *how it works*.**

A coding agent reading a pattern node should finish knowing:

- Does this pattern apply to the task in front of me? (yes / no / under what condition)
- Is there a prerequisite, conflict, or antipattern I need to respect?
- Where do I go for a full explanation if I need one?

Everything else is noise.

---

## Rules

### 1. Directive, not explanatory

State the position. Don't teach the reader what the pattern is — the name and sources do that.

**Bad.** *The circuit breaker operates as a state machine with three states: closed, open, and half-open. In the closed state, all requests pass through...*

**Good.** *Use when calling external dependencies where prolonged failures could exhaust caller resources. Not for in-process or fire-and-forget calls.*

### 2. Bullets over prose

Every body section (except `## Description`, `## Context`, `## Problem`, `## Rationale`) should default to bullets. If a bullet needs more than ~25 words, it's probably prose — split it or cut it.

### 3. Length caps

Soft caps per section. Exceeding them fires a lint warning.

| Section | Cap |
|---------|-----|
| `## When to use` | ≤6 bullets, ≤25 words each |
| `## When NOT to use` | ≤6 bullets, ≤25 words each |
| `## Decision inputs` | ≤6 bullets, ≤30 words each |
| `## Solution sketch` | ≤150 words total, no step-by-step tutorials |
| `## How to recognise` / `## Why it happens` / `## Consequences` / `## How to fix` | ≤6 bullets each, ≤25 words each |
| `## Trade-offs` | ≤5 rows |
| `## Implementation checklist` | ≤10 items, each a single verifiable action |
| `## Description` / `## Key concerns` (context) | ≤150 words total |

These are warnings, not errors. If a pattern genuinely needs more, write more — but justify it.

### 4. Delegate depth to sources

Every `pattern`, `antipattern`, and `solution` must cite at least one source. Don't re-explain what the source already explains well. Link out.

**Bad.** A 400-word block explaining how exponential backoff with jitter calculates delays.

**Good.** *See [AWS: Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) for the delay-calculation derivation.*

### 5. No tutorials, minimal code

`## Solution sketch` is a *sketch*, not a walkthrough. A small diagram, a signature, or a URI example is fine. A working implementation is not.

**Fine.** A 4-line API URI table (`GET /orders`, `POST /orders`, …) or a three-state transition diagram.

**Not fine.** A 20-line code block that an agent could write itself from the pattern name.

### 6. Implementation checklists are verifiable actions

Each item must be something a reviewer can tick off by looking at the code. Not "think about X" or "consider Y".

**Bad.** *Consider whether retries are appropriate for your operation.*

**Good.** *Define an allowlist of retryable error codes (5xx, 429, connection-reset).*

### 7. Cut before you add

If a sentence doesn't change what an agent decides, delete it. Background, motivation, history, and sympathy-for-the-reader framing all belong in sources, not in Carta.

Phrases that usually signal deletable content: *"In other words"*, *"This means that"*, *"For example, imagine"*, *"It's important to note"*, *"Historically"*.

### 8. Frontmatter is the graph

Most of the signal in a Carta node is in the frontmatter: `applies_to`, `prerequisites`, `conflicts_with`, `contradicted_by`, `mitigated_by`. Keep those rich; let the body stay thin.

### 9. Overrides override, don't re-derive

An org/team/project override exists to change a foundation node's guidance. State what changes and why. Don't restate the parts that stayed the same — the traversal reads foundation and override together.

### 10. Write for the agent first, the human second

The primary reader is a coding agent resolving whether to apply this pattern in a given task. A human skimming the file should still get value, but clarity for the agent drives the voice: short, declarative, decision-oriented.

---

## Anti-examples in the current foundations

The foundation patterns in `foundations/20-patterns/` were authored before these rules existed. They read like textbook entries — fine as reference material, too verbose as agent input. Treat them as a known debt to trim, not as a model to copy.

---

## See also

- [`node-schema.md`](node-schema.md) — structural contract (frontmatter, required sections).
- [`CHARTER.md`](../CHARTER.md) — admission criteria for foundation-level content.
- [`../commands/carta-add.md`](../commands/carta-add.md) — the `/carta-add` command, which loads these rules before drafting.
