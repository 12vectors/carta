---
id: antipattern-silent-failure
title: Silent Failure
type: antipattern
category: resilience
maturity: stable
tags: [antipattern, stable, resilience, observability, error-handling]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-data-pipeline]]"
  - "[[context-batch-processing]]"
  - "[[context-internal-tool]]"
  - "[[context-agentic-system]]"
mitigated_by:
  - "[[pattern-structured-logging]]"
  - "[[pattern-dead-letter-channel]]"
  - "[[pattern-health-check-endpoint]]"
sources:
  - "Release It!, 2nd ed (Nygard, Pragmatic Bookshelf, 2018) — https://pragprog.com/titles/mnee2/release-it-second-edition/"
  - "Site Reliability Engineering (Beyer et al., O'Reilly, 2016) — https://sre.google/sre-book/table-of-contents/"
---

## How to recognise

- `except Exception: pass` or empty catch blocks anywhere in the call path.
- Failures caught and returned as vague strings (`run.error = "failed"`) with no log line.
- Broad `try / except` that suppresses the exception class a specific handler would have caught.
- Background workers that crash-and-restart with no event recorded.
- UI shows "something went wrong" while no backend log or metric fires.
- Post-incident log review reveals gaps where the failing path left no trace.

## Why it happens

- Defensive coding by cargo-cult — wrap everything in try/except "just in case".
- Linter or test-runner noise suppression: a flaky step got quieted and the quiet became permanent.
- Handler broadens over time: a specific catch accumulates unrelated exceptions.
- Logging isn't wired in from day one; the failure path is added first, the log is always "later".
- Developer fear of crash cascades leads to catch-and-continue as the default.

## Consequences

- Failures become invisible — MTTR dominated by detection, not recovery.
- Data corruption silently propagates; nothing flags the first bad write.
- Incident forensics is guesswork because the primary evidence is missing.
- Users see degraded behaviour long before operators do.
- LLM-backed systems waste budget on failing calls that never alert.

## How to fix

- Never write `except Exception: pass`. Handle a specific exception class or let it propagate.
- Every caught failure logs at `error` or `warning` with enough context to reconstruct the call.
- Background tasks publish completion and failure events; silent exit is a bug, not a state.
- Poison-message consumers route to a [[pattern-dead-letter-channel]] instead of swallowing.
- Health checks and dashboards show failure *rates*, not only failure *presence* — zero-rate doesn't mean healthy.
- Code review rejects broad catches without a reason comment documenting *why* the catch is that wide.

## See also

- [[pattern-structured-logging]] — the machinery that makes silent failures visible.
- [[pattern-dead-letter-channel]] — the right home for messages a consumer can't process.
- [[pattern-health-check-endpoint]] — distinguishes "process up" from "dependencies working".
- [[principle-design-for-failure]] — the principle violated by swallowing them.
- [[principle-observe-before-optimising]] — you cannot optimise or fix what you cannot see.
