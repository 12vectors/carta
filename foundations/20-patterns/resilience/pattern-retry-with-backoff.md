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

Apply retry with exponential backoff when calling services that may experience transient failures. Common triggers include:

- **Network blips.** TCP resets, DNS hiccups, TLS handshake timeouts -- brief interruptions that resolve on their own.
- **Temporary overload.** The downstream service is shedding load or restarting and will recover within seconds.
- **Rate limiting.** The service returns 429 Too Many Requests and expects you to slow down before retrying.
- **Cloud infrastructure transience.** Managed services (databases, queues, object stores) occasionally return 500-series errors that succeed on a second attempt.

The pattern is most valuable when the caller can tolerate a small increase in latency in exchange for significantly higher end-to-end reliability.

## When NOT to use

- **Deterministic errors.** A 400 Bad Request, 401 Unauthorized, 404 Not Found, or 422 Unprocessable Entity will not succeed on retry. Retrying these wastes resources and delays meaningful error reporting.
- **Non-idempotent operations without idempotency keys.** If the operation has side effects (creating an order, sending an email) and you have no idempotency mechanism, a retry after an ambiguous failure can cause duplicates.
- **Tight latency budgets.** If the caller has a 200ms SLA and each retry attempt adds 100ms+ of backoff delay, retries will blow the budget. Fail fast instead.
- **Permanent downstream outages.** If the service is down for maintenance or has a known issue, retries just add load. Use a [[pattern-circuit-breaker]] to short-circuit instead.

## Decision inputs

Before implementing, resolve these questions:

- **How many retries?** Typically 3-5. More retries increase the chance of eventual success but also increase worst-case latency and load on the downstream service.
- **What backoff strategy?** Exponential backoff (doubling the delay each attempt) is the standard choice. Linear and fixed-interval backoff are simpler but less effective at reducing thundering-herd effects.
- **Add jitter?** Yes, almost always. Without jitter, clients that fail at the same time will retry at the same time, creating periodic load spikes. Full jitter (randomizing the delay between 0 and the computed backoff) is recommended.
- **Which errors are retryable?** Define an explicit allowlist: 5xx status codes, network timeouts, connection resets, and 429 responses. Never retry client errors (4xx other than 429).
- **What is the maximum total wait?** Set a ceiling on cumulative retry time so that the worst case is bounded. For example, cap total backoff at 10 seconds regardless of the retry count.

## Solution sketch

1. **Attempt the operation.**
2. **On transient failure**, compute the delay: `delay = base_delay * 2^attempt + random_jitter`.
   - Example progression with 100ms base: 100ms, 200ms, 400ms, 800ms.
   - Add jitter: `actual_delay = random(0, delay)` (full jitter) or `actual_delay = delay/2 + random(0, delay/2)` (equal jitter).
3. **Wait** for the computed delay.
4. **Retry** the operation.
5. **After max retries**, give up and propagate the error to the caller with context about the failure (number of attempts, last error).

```
max_retries = 4
base_delay  = 100ms

for attempt in 0..max_retries:
    response = call_service(request)
    if response.is_success:
        return response
    if not is_retryable(response.status):
        raise PermanentError(response)
    delay = base_delay * (2 ** attempt)
    sleep(delay + random(0, delay))  # full jitter

raise RetriesExhaustedError(attempts=max_retries, last_error=response)
```

Pair this with a [[pattern-circuit-breaker]] so that sustained failures trip the breaker and stop retries entirely, preventing prolonged load on a failing service.

## Trade-offs

| Gain | Cost |
|------|------|
| Handles transient failures transparently without caller intervention | Increases latency on failure paths -- worst case is the sum of all backoff delays |
| Improves end-to-end reliability for operations crossing network boundaries | Can amplify load on a struggling service if many clients retry simultaneously (thundering herd) |
| Simple to implement and reason about | Adds complexity around idempotency -- callers must ensure retried operations are safe to repeat |
| Pairs naturally with circuit breakers for layered resilience | Masks persistent failures if retry counts are too high, delaying detection |

## Implementation checklist

- [ ] Define the set of retryable error codes and exception types explicitly
- [ ] Choose base delay, multiplier, and max retries based on downstream SLA
- [ ] Add full or equal jitter to prevent thundering herd
- [ ] Set a maximum total backoff ceiling to bound worst-case latency
- [ ] Ensure all retried operations are idempotent (or use idempotency keys)
- [ ] Log each retry attempt with attempt number, delay, and error for observability
- [ ] Combine with a circuit breaker to avoid retrying during sustained outages
- [ ] Write tests that simulate transient failures and verify retry/backoff behaviour

## See also

- [[pattern-circuit-breaker]] -- stops retries entirely when a downstream service is persistently failing
