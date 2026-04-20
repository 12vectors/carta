---
id: principle-minimize-coordination
title: Minimize Coordination
type: principle
maturity: stable
pillar: "[[pillar-reliability]]"
related_patterns:
  - "[[pattern-database-per-service]]"
  - "[[pattern-event-sourcing]]"
  - "[[pattern-saga]]"
  - "[[pattern-read-replica]]"
tags: [principle, stable, reliability, scalability]
---

## Statement

Avoid synchronous cross-component coordination. Every required consensus, lock, or distributed transaction is a future incident.

## Rationale

Coordination imposes latency, reduces availability (all parties must be up), and couples deployments. Systems that coordinate less scale further and recover faster because each part can make progress independently. Eventual consistency is usually acceptable; strong consistency is usually expensive.

## How to apply

- Prefer local state and eventually-consistent replication over shared state.
- Use sagas and compensating transactions instead of distributed 2PC.
- Push ordering into a message log rather than global locks.
- Accept staleness where the domain tolerates it — state it explicitly in the API contract.

## Related patterns

- [[pattern-database-per-service]] — no shared schema; no cross-service joins.
- [[pattern-event-sourcing]] — ordering via append-only log, not locks.
- [[pattern-saga]] — replace distributed transactions with compensations.
- [[pattern-read-replica]] — serve reads without contending with writes.
