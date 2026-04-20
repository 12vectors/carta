---
id: pattern-timeout
title: Timeout
type: pattern
category: resilience
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, resilience, fault-tolerance]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-bulkhead]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Release It!, 2nd ed (Nygard, Pragmatic Bookshelf, 2018) — https://pragprog.com/titles/mnee2/release-it-second-edition/"
---

## When to use

- Every outbound network call — default on, not opt-in.
- Calls to dependencies whose latency distribution has a long tail.
- Synchronous request paths with a finite per-request budget.
- Background jobs where hung work would pin a worker indefinitely.
- Lock acquisition, DB queries, and any blocking I/O.

## When NOT to use

- Streaming or long-poll connections with explicit heartbeats instead.
- Batch jobs intentionally designed to run for hours with liveness probes.
- In-process pure computation with deterministic completion.

## Decision inputs

- Observed p99/p99.9 latency of the dependency under load.
- Upstream deadline budget — timeouts must fit inside it.
- Cost of a false positive (cancelling a near-complete request).
- Connect timeout vs read/total-request timeout distinction.
- Propagation of deadline across downstream calls (deadline budgets).

## Solution sketch

Set an explicit upper bound on every I/O call. Prefer a total-request deadline propagated from the caller over fixed per-hop values — each downstream subtracts elapsed time from the budget. Typical split: `connect ~1s`, `read = p99 * 1.5` with a hard ceiling. On timeout, release the resource, surface a typed error, and let retry/circuit-breaker policy decide next steps.

```
deadline_in = now + 2s
 └─ call A (budget 2s)  → returns in 400ms, remaining 1.6s
     └─ call B (budget 1.6s) → times out at 1.6s, not 2s
```

See Nygard ch. 5 for timeout-cascade failure modes.

## Trade-offs

| Gain | Cost |
|------|------|
| Bounds worst-case latency; releases pool slots | Cancels near-complete requests on noisy tails |
| Prevents hung threads from exhausting the process | Requires per-dependency tuning from real latency data |
| Surfaces dependency slowness as an observable signal | Default library values are usually wrong (too high or missing) |
| Enables deadline propagation across hops | Non-cancellable operations may keep running after timeout |

## Implementation checklist

- [ ] Set an explicit timeout on every outbound call — no defaults.
- [ ] Distinguish connect vs read vs total-request timeouts.
- [ ] Derive values from measured p99/p99.9, not guesses.
- [ ] Propagate a deadline budget through the call chain.
- [ ] Ensure timeout cancellation actually releases the underlying resource.
- [ ] Emit timeout counts per dependency; alert on rate changes.
- [ ] Pair with `[[pattern-retry-with-backoff]]` for transient timeouts.
- [ ] Pair with `[[pattern-circuit-breaker]]` when timeouts persist.

## See also

- [[pattern-circuit-breaker]] — trips when timeouts pass a threshold.
- [[pattern-retry-with-backoff]] — retry a timed-out idempotent call.
- [[pattern-bulkhead]] — timeouts let bulkhead pool slots recycle.
