---
id: pattern-circuit-breaker
title: Circuit Breaker
type: pattern
category: resilience
maturity: stable
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

- Calling external services or unreliable dependencies (third-party APIs, databases, downstream microservices) where failures are possible and potentially prolonged.
- When cascading failures are a risk -- a slow or failing dependency can exhaust connection pools, thread pools, or memory in the calling service, causing it to fail in turn.
- In systems where fast failure is preferable to slow failure. A circuit breaker lets the caller fail immediately rather than waiting for a timeout, preserving resources and improving user experience with a timely fallback.
- When you need to give a struggling dependency time to recover. The open state stops sending traffic, reducing load on the failing service and giving it breathing room.

## When NOT to use

- Calling local or in-process dependencies where failure modes are limited to programming errors, not network or infrastructure issues.
- When the dependency has no meaningful failure mode -- for example, reading from a local configuration file or an in-memory cache.
- For fire-and-forget operations where the caller does not need to know or care about the outcome (e.g., emitting a non-critical analytics event to a message queue with at-least-once delivery guarantees).
- When the calling pattern is already request-scoped and isolated -- for instance, a batch job that processes items independently and can tolerate individual item failures without systemic risk.

## Decision inputs

- **What is the acceptable failure threshold?** Define the conditions that trip the breaker. Common approaches: a percentage of failures over a rolling window (e.g., 50% of requests failing over the last 10 requests) or a count-based threshold (e.g., 5 consecutive failures).
- **What is the timeout for the open state?** After the breaker opens, how long should it wait before allowing a probe request? Typical values range from 10 to 60 seconds depending on the dependency's expected recovery time.
- **What is the fallback behaviour?** Options include returning a cached response, a default value, a degraded result, or an explicit error. The fallback must be defined per use case -- there is no generic answer.
- **How will you monitor breaker state transitions?** Every state change (closed-to-open, open-to-half-open, half-open-to-closed) should emit a metric or log entry. Without observability, you cannot tune thresholds or detect misconfiguration.
- **What request properties define the circuit?** A single breaker per dependency is the default, but consider per-endpoint or per-tenant circuits if failure modes are localised.

## Solution sketch

The circuit breaker operates as a state machine with three states:

```
  [CLOSED] ---failure threshold reached---> [OPEN]
     ^                                        |
     |                                   timeout expires
     |                                        |
     |                                        v
     +----probe succeeds--------------- [HALF-OPEN]
     |                                        |
     +----<--(reset to closed)    probe fails--+--> [OPEN]
```

**Closed (normal operation).** All requests pass through to the dependency. The breaker counts failures within a rolling window. If the failure count or rate exceeds the configured threshold, the breaker transitions to the open state.

**Open (failing fast).** All requests are immediately rejected without calling the dependency. The caller receives the configured fallback response. After a configurable timeout period elapses, the breaker transitions to half-open.

**Half-open (probing).** A limited number of requests (typically one) are allowed through to test whether the dependency has recovered. If the probe succeeds, the breaker transitions back to closed and resets its failure counters. If the probe fails, the breaker returns to the open state and resets the timeout.

Key implementation considerations:

- Use a **sliding window** (time-based or count-based) rather than a simple counter to avoid tripping on stale failures.
- **Distinguish failure types.** Timeouts and 5xx errors should count toward the threshold. Client errors (4xx) generally should not -- they indicate a problem with the request, not the dependency.
- **Thread safety.** The breaker's state and counters must be safe for concurrent access. In most implementations this means atomic operations or a small critical section.
- **Combine with retries carefully.** Retries should happen before the circuit breaker evaluates the outcome. If you retry three times and all fail, that counts as one failure to the breaker -- not three. This is why the retry-with-backoff pattern is a prerequisite.

## Trade-offs

| Gain | Cost |
|------|------|
| Prevents cascade failures by stopping requests to an unhealthy dependency before the caller's resources are exhausted | Adds complexity to the call path -- each external call now has state machine logic, configuration, and fallback handling |
| Fails fast, freeing threads and connections for requests that can still succeed | Can mask transient errors if thresholds are too sensitive -- a brief network blip may open the breaker unnecessarily |
| Gives struggling dependencies time to recover by eliminating load during the open state | Requires per-dependency tuning of thresholds, timeouts, and failure classification -- poor defaults cause either premature tripping or no protection at all |
| Provides a natural hook for fallback behaviour (cached data, defaults, degraded features) | Half-open probing introduces a delay in recovery detection -- the system does not resume full traffic immediately when the dependency recovers |

## Implementation checklist

- [ ] Choose a circuit breaker library appropriate to your stack (e.g., resilience4j for JVM, polly for .NET, opossum for Node.js) or implement against the state machine described above
- [ ] Configure failure thresholds per dependency based on observed error rates and SLA requirements
- [ ] Define explicit fallback behaviour for each circuit -- cached response, default value, or graceful degradation
- [ ] Exclude client errors (4xx) from the failure count to avoid tripping the breaker on bad requests
- [ ] Emit metrics on every state transition (closed/open/half-open) and on every rejected request
- [ ] Set up alerts for breaker-open events so the team is notified when a dependency is failing
- [ ] Write integration tests that simulate dependency failures and verify the breaker opens, falls back, and recovers
- [ ] Coordinate circuit breaker settings with retry-with-backoff configuration to avoid retry amplification

## See also

- [[pattern-retry-with-backoff]] -- prerequisite; retries should be exhausted before the circuit breaker evaluates the outcome
- [[pattern-structured-logging]] -- log state transitions with correlation IDs for traceability during incidents
- [[pattern-rest-api]] -- circuit breakers are commonly applied to outbound REST API calls
