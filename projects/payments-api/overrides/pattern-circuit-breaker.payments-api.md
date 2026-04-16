---
id: pattern-circuit-breaker
title: Circuit Breaker (Payments API — Extended Timeouts)
type: pattern
category: resilience
maturity: stable
tags: [pattern, resilience, stable]
applies_to:
  - "[[context-web-application]]"
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

> [!info] Project override
> This overrides the foundation [[pattern-circuit-breaker]] for the payments-api project.
> See [[adr-0001-relaxed-circuit-breaker-timeouts.payments-api]] for the reasoning.

## When to use

Same as the foundation pattern — calling external services or unreliable dependencies where cascading failures are a risk. In the payments-api context, the primary circuit-broken dependency is the payment processor (Stripe, Adyen, or similar).

## When NOT to use

- Calling local/in-process dependencies.
- Internal service-to-service calls within the payments domain — use the foundation circuit breaker settings (5s timeout) for these.
- For fire-and-forget operations like analytics events.

## Decision inputs

- **Timeout:** 30 seconds for payment processor calls (not the foundation default of 5 seconds). Payment processors routinely take 10-20 seconds for 3D Secure flows, bank verification, and cross-border transactions.
- **Failure threshold:** 40% over a 20-request sliding window (relaxed from 50% over 10 requests). Payment processor errors are often transient and self-correcting.
- **Half-open probe interval:** 60 seconds (up from 30 seconds). Give the processor more recovery time before probing.
- **Fallback behaviour:** queue the payment for async retry rather than failing immediately. Payments are high-value operations — a user who sees "payment failed" may not retry.

## Solution sketch

Same three-state machine as the foundation pattern (closed → open → half-open), with these adjustments:

1. **Timeout: 30s** — payment processors are slow but reliable. A 5s timeout would trip the circuit on normal 3D Secure flows.
2. **Failure window: 20 requests** — larger window smooths out isolated failures from specific card networks.
3. **Fallback: async queue** — when the circuit opens, enqueue the payment attempt for background retry rather than returning an immediate error. Notify the user that payment is "processing" rather than "failed."
4. **Separate circuits per processor** — if you integrate with multiple payment processors, each gets its own circuit. A Stripe outage should not trip the Adyen circuit.

## Trade-offs

| Gain | Cost |
|------|------|
| Avoids false circuit trips on normal slow payment flows | Higher latency budget — 30s ties up a connection and a user's attention |
| Async fallback preserves payment intent | Async queue adds complexity and requires idempotency guarantees |
| Per-processor circuits contain blast radius | More circuits to monitor and tune |
| Fewer false "payment failed" errors shown to users | Longer time to detect genuine processor outages |

## Implementation checklist

- [ ] Circuit breaker timeout set to 30s for payment processor clients.
- [ ] Foundation default (5s) retained for all non-processor dependencies.
- [ ] Failure threshold: 40% over 20-request sliding window.
- [ ] Separate circuit instances per payment processor.
- [ ] Async retry queue implemented with idempotency keys.
- [ ] "Payment processing" user-facing state implemented (not "payment failed").
- [ ] Circuit state changes logged with structured logging (open/close events, affected processor).
- [ ] Dashboard showing per-processor circuit state and trip frequency.
- [ ] Alert on circuit open events for any processor.

## See also

- [[pattern-retry-with-backoff]] — retries happen within the 30s timeout window before the circuit considers it a failure
- [[pattern-structured-logging]] — circuit state transitions must be logged for operational visibility
- [[adr-0001-relaxed-circuit-breaker-timeouts.payments-api]] — the decision record explaining these overrides
