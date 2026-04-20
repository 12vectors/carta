---
id: pattern-saga
title: Saga
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, data, distributed-transaction, long-running]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites:
  - "[[pattern-database-per-service]]"
related:
  - "[[pattern-compensating-transaction]]"
  - "[[pattern-transactional-outbox]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://microservices.io/patterns/data/saga.html"
  - "Sagas (Garcia-Molina & Salem, ACM SIGMOD 1987) — https://doi.org/10.1145/38713.38742"
---

## When to use

- A business transaction spans multiple services, each with its own store.
- You need atomicity-like guarantees without distributed (2PC) transactions.
- Steps are long-running (seconds to days) and must survive restarts.
- Each step has a meaningful compensating action if later steps fail.
- Intermediate visibility of partial state is acceptable to the business.

## When NOT to use

- Single-service transactions — use local ACID.
- Workflows where steps cannot be semantically undone (irreversible external effects without reconciliation).
- Strict linearisability or read-your-writes across all services.
- Simple request-response interactions with no multi-step commit.

## Decision inputs

- Orchestration vs. choreography — central coordinator or event-driven chain.
- Idempotency on every step and every compensation.
- Timeouts per step and the policy for stuck sagas (retry, compensate, page).
- Isolation strategy for intermediate state (semantic locks, commutative updates).
- Observability — correlation ID, saga ID, step status, compensation trail.

## Solution sketch

A saga is a sequence of local transactions, each in its own service. On success the next step runs; on failure, previously completed steps are undone by running their compensating transactions in reverse. Two coordination styles:

- **Orchestration** — a saga coordinator service issues commands to each step and decides when to compensate. Easier to reason about, single place for retries and timeouts.
- **Choreography** — each service reacts to events from the previous step. No central coordinator, but the end-to-end flow is implicit in the event graph.

```
[Step 1] -> [Step 2] -> [Step 3]            (happy path)
[Step 1] -> [Step 2] -> [Step 3 FAILS]
[Comp 1] <- [Comp 2] <- (Step 3 no-op)      (compensation)
```

Every step and compensation must be idempotent. Use the outbox pattern to publish step completions reliably.

## Trade-offs

| Gain | Cost |
|------|------|
| Multi-service atomicity without 2PC | Compensations must exist and be correct for every step |
| Long-running workflows survive restarts and partial failures | Intermediate state is visible — no isolation |
| Orchestration gives a single place to debug and evolve | Orchestrator can become a monolith of business logic |
| Choreography keeps services loosely coupled | Choreographed flow is hard to see or audit end-to-end |

## Implementation checklist

- [ ] Choose orchestration or choreography and justify it.
- [ ] Define every step and its compensation; document what "undo" means.
- [ ] Make every step and compensation idempotent.
- [ ] Persist saga state (coordinator or per-service) to survive crashes.
- [ ] Publish step events via an outbox, not a dual write.
- [ ] Set timeouts per step with escalation to compensation or manual action.
- [ ] Propagate a saga/correlation ID through every message and log line.
- [ ] Build a runbook for stuck sagas and manual intervention.

## See also

- [[pattern-database-per-service]] — the constraint that forces sagas.
- [[pattern-compensating-transaction]] — the undo mechanism each step needs.
- [[pattern-transactional-outbox]] — reliable event publication between steps.
- [[pattern-idempotency-key]] — make step handlers safe to retry.
