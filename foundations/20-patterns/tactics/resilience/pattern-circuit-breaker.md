---
id: pattern-circuit-breaker
title: Circuit Breaker
type: pattern
category: resilience
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, resilience, fault-tolerance, cascading-failure]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-retry-with-backoff]]"
related:
  - "[[pattern-structured-logging]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Release It! (Nygard, 2018) ch. 5"
  - "https://martinfowler.com/bliki/CircuitBreaker.html"
---

## When to use

- Calling external or downstream services where prolonged failures could exhaust the caller's resources.
- When cascading failure is a real risk (shared thread/connection pools, synchronous fan-out).
- When fast failure + fallback is better UX than waiting for a timeout.
- When the dependency benefits from reduced load while recovering.

## When NOT to use

- In-process or local calls with no network/infrastructure failure mode.
- Fire-and-forget paths where the caller does not care about the outcome.
- Request-scoped batch work where individual item failure is already tolerated.

## Decision inputs

- Failure threshold (count or percentage over a rolling window).
- Open-state timeout before a probe is allowed.
- Fallback behaviour per use case (cached, default, degraded, error).
- Circuit granularity (per dependency, per endpoint, per tenant).
- Metrics and alerts on state transitions.

## Solution sketch

Three-state machine: **closed** (pass through, counting failures) → **open** (fail fast, run fallback) → **half-open** (probe one request). Counts timeouts and 5xx; client 4xx do not trip. Retries (see prerequisite) run *inside* the breaker — N retries failing = 1 breaker failure.

```
[CLOSED] --threshold--> [OPEN] --timeout--> [HALF-OPEN] --success--> [CLOSED]
                                                      \--failure--> [OPEN]
```

See Fowler's write-up (linked in sources) for state-machine details and Nygard ch. 5 for tuning guidance.

## Trade-offs

| Gain | Cost |
|------|------|
| Stops cascade failures from exhausting caller resources | State machine, config, and fallback logic on every call path |
| Fails fast — frees threads and connections | Sensitive thresholds cause spurious trips on transient blips |
| Gives failing dependency room to recover | Requires per-dependency tuning; poor defaults mean no protection |
| Natural hook for fallback behaviour | Half-open probing delays full recovery detection |

## Implementation checklist

- [ ] Pick a library (resilience4j, polly, opossum) or implement the state machine directly.
- [ ] Configure thresholds per dependency from observed error rates.
- [ ] Define an explicit fallback for each circuit.
- [ ] Exclude 4xx from the failure count.
- [ ] Emit metrics on every state transition and rejected request.
- [ ] Alert on breaker-open events.
- [ ] Integration-test failure, fallback, and recovery paths.
- [ ] Coordinate with retry config to avoid retry amplification.

## See also

- [[pattern-retry-with-backoff]] — prerequisite; retries are exhausted before the breaker evaluates.
- [[pattern-structured-logging]] — log transitions with correlation IDs.
- [[pattern-rest-api]] — commonly applied to outbound REST calls.
