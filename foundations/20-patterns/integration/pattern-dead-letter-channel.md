---
id: pattern-dead-letter-channel
title: Dead Letter Channel
type: pattern
category: integration
maturity: stable
pillars:
  - "[[pillar-reliability]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, messaging, reliability, dlq, integration]
applies_to:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
prerequisites: []
related:
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-competing-consumers]]"
conflicts_with: []
contradicted_by: []
sources:
  - "EIP (Hohpe & Woolf, 2003) — https://www.enterpriseintegrationpatterns.com/patterns/messaging/DeadLetterChannel.html"
---

## When to use

- Any durable queue or topic with consumers that can reject a message.
- Poison messages (malformed, unknown schema, permanent failures) must not block the queue.
- Retries are bounded and exhausted — messages need somewhere safe to land.
- Compliance requires you preserve failed messages for investigation or replay.
- You need a clean signal ("DLQ arrival") to alert on.

## When NOT to use

- Transient in-memory queues with no durability or replay need.
- Workloads where silent drop is acceptable (metrics, non-critical telemetry).
- When the real issue is retry storms — fix retry policy first; DLQ is downstream.
- Broker already provides an equivalent built-in (check SQS/Kafka DLT support).

## Decision inputs

- Max-receive / delivery-attempt count before moving to DLQ.
- DLQ retention — long enough to investigate, short enough not to hoard.
- Who owns the DLQ and who triages it?
- Replay mechanism — is there a one-click path back to the source queue?
- PII and regulatory implications of storing failed payloads.
- Alerting thresholds: first arrival, rate, depth.

## Solution sketch

A dedicated channel receives messages the consumer could not process. The broker moves them after N failed deliveries; the original queue drains unblocked.

```
[Queue] -> [Consumer] --fail N times--> [DLQ] --triage--> [Replay / Discard]
```

- **Fail-fast** on permanent errors (schema, auth); **retry** on transient ones.
- Include failure context: original headers, attempt count, last error, trace ID.
- DLQ is a **signal**, not a graveyard — every DLQ message needs an owner.
- Build a replay tool early; a DLQ without replay is just data hoarding.
- Alert on first DLQ arrival and on growth rate, not just depth.

## Trade-offs

| Gain | Cost |
|------|------|
| Poison messages do not block the main queue | Extra queue and tooling to operate and monitor |
| Preserves evidence for debugging and audits | DLQ becomes a dumping ground if no triage process |
| Clean signal for alerting and SLO accounting | Retention and PII policies add compliance burden |
| Enables safe replay after fixing the root cause | Replay can re-introduce bad data if not carefully scoped |

## Implementation checklist

- [ ] Configure max-receive / delivery-attempt limit on every durable queue.
- [ ] Route failed messages to a per-queue DLQ; do not share one DLQ.
- [ ] Include attempt count, last error, and trace ID in DLQ metadata.
- [ ] Distinguish transient vs permanent failures — do not retry permanent ones.
- [ ] Alert on first DLQ arrival, depth, and age.
- [ ] Build a replay tool that can target selected messages.
- [ ] Set retention matched to triage SLA; encrypt at rest if PII possible.
- [ ] Run a DLQ-triage runbook drill periodically.

## See also

- [[pattern-retry-with-backoff]] — retries run first; DLQ catches what retries cannot fix.
- [[pattern-competing-consumers]] — DLQ is essential when many workers share a queue.
- [[pattern-idempotency-key]] — replay from DLQ demands idempotent consumers.
