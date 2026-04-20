---
id: pattern-compensating-transaction
title: Compensating Transaction
type: pattern
category: data
maturity: stable
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, stable, data, rollback, consistency]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-saga]]"
conflicts_with: []
contradicted_by: []
sources:
  - "https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction"
---

## When to use

- A multi-step operation has already committed steps when a later step fails.
- Rollback via distributed transaction (2PC) is unavailable or too expensive.
- Each committed step has a semantically meaningful undo action.
- Business tolerates "apologise and correct" semantics instead of strict atomicity.
- Partial failures would otherwise leave the system in an invalid state.

## When NOT to use

- The operation is truly atomic within a single store — use local transactions.
- Steps are irreversible with no reconciliation path (physical shipment, paid-out funds without refund mechanism).
- A forward-only retry will eventually succeed and is acceptable.
- When a saga-level decision already applies — use the compensation as part of it.

## Decision inputs

- Undo semantics for every step — what "reverse" means in the domain.
- Idempotency of the compensating action itself.
- Ordering — compensations usually run in reverse of the forward order.
- Visibility — is partial state observable during compensation.
- Escalation when a compensation also fails (retry, page, manual).

## Solution sketch

For each forward step that commits externally visible state, define a compensating action that logically reverses it. On failure mid-workflow, execute compensations in reverse order for every step that already completed. Compensations are themselves transactions — they can fail, must be idempotent, and must be retried until they succeed or an operator intervenes.

```
Forward:  [A] -> [B] -> [C FAILS]
Compensate:         <- [undo B] <- [undo A]
```

"Undo" is rarely a literal rollback. A charged card becomes a refund; a reserved seat becomes a release; a sent email becomes an apology email. Record both the forward and compensating actions for audit. Most often used as the failure-handling mechanism inside a saga.

## Trade-offs

| Gain | Cost |
|------|------|
| Multi-step consistency without distributed transactions | Every step needs a designed, tested undo |
| Works across heterogeneous services and stores | Intermediate state is visible to users and downstream systems |
| Compensation is auditable — every undo is explicit | Compensation failures need their own escalation path |
| Domain-specific undos can be more useful than a raw rollback | Some effects can't be undone — only reconciled or apologised for |

## Implementation checklist

- [ ] List every forward step that commits external state.
- [ ] Define a compensating action for each; document the semantics.
- [ ] Make every compensation idempotent and retryable.
- [ ] Persist a journal of forward and compensating actions.
- [ ] Run compensations in reverse order of completion.
- [ ] Define escalation when a compensation exhausts retries.
- [ ] Test happy path, mid-flight failure, and compensation failure.
- [ ] Communicate visible intermediate state to consumers (status fields, events).

## See also

- [[pattern-saga]] — the usual container for compensating transactions.
- [[pattern-idempotency-key]] — required for safe compensation retries.
- [[pattern-transactional-outbox]] — reliable publication of compensation events.
- [[pattern-retry-with-backoff]] — applied to the compensation itself.
