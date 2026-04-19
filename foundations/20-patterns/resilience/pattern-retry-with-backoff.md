---
id: pattern-retry-with-backoff
title: Retry with Exponential Backoff
type: pattern
category: resilience
maturity: stable
tags: [pattern, stable, resilience, fault-tolerance]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-circuit-breaker]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Release It! (Nygard, 2018) ch. 5"
  - "https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/"
---

## When to use

- Transient network faults (TCP resets, DNS blips, TLS handshake timeouts).
- Temporary downstream overload that resolves in seconds.
- Rate-limit responses (429) with a recommended backoff.
- Cloud infrastructure transience on managed DB/queue/storage calls.

## When NOT to use

- Deterministic errors (400, 401, 404, 422) — retry will not help.
- Non-idempotent operations without idempotency keys.
- Tight latency budgets where backoff delays blow the SLA.
- Known sustained outages — use `[[pattern-circuit-breaker]]` instead.

## Decision inputs

- Max retry count (typically 3-5).
- Backoff formula and base delay.
- Jitter strategy (full jitter recommended — see AWS source).
- Retryable-error allowlist (5xx, 429, timeouts, connection resets).
- Ceiling on total cumulative wait.

## Solution sketch

Attempt → on retryable failure, wait `base * 2^attempt + jitter`, retry up to N times, then surface the last error. Pair with a circuit breaker so sustained failure halts retries instead of amplifying load.

See the AWS Architecture Blog source for jitter derivations and Nygard ch. 5 for tuning.

## Trade-offs

| Gain | Cost |
|------|------|
| Handles transient failures transparently | Worst-case latency = sum of all backoff delays |
| Improves end-to-end reliability across network boundaries | Synchronised retries can amplify load (thundering herd) — jitter mitigates |
| Simple to implement | Requires idempotency or idempotency keys |
| Composes naturally with circuit breakers | Masks persistent failure when retry count is too high |

## Implementation checklist

- [ ] Define an explicit allowlist of retryable errors.
- [ ] Pick base delay, multiplier, and max retries per downstream SLA.
- [ ] Apply full or equal jitter.
- [ ] Cap cumulative backoff to bound worst-case latency.
- [ ] Ensure operations are idempotent or use idempotency keys.
- [ ] Log each attempt (number, delay, error) for observability.
- [ ] Combine with `[[pattern-circuit-breaker]]` to halt during outages.
- [ ] Test transient-failure and retry-exhaustion paths.

## See also

- [[pattern-circuit-breaker]] — stops retries when the dependency is persistently down.
