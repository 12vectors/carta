---
id: dtree-choose-background-work
title: Choose a Background Work Strategy
type: decision-tree
maturity: stable
tags: [decision-tree, stable, background-jobs, async]
decides_between:
  - "[[pattern-async-request-reply]]"
  - "[[pattern-queue-based-load-leveling]]"
  - "[[pattern-competing-consumers]]"
criteria:
  - "Durability — must the task survive process crash, deploy, or host loss?"
  - "Volume — events per minute vs. events per second vs. events per millisecond?"
  - "Delay semantics — immediate, scheduled, periodic, or long-running (minutes to days)?"
  - "Retry and delivery guarantees — at-most-once / at-least-once / exactly-once with compensation?"
  - "Operational complexity budget — can the team run a broker, a workflow engine, or only a process?"
  - "Caller visibility — does the caller need a status or result handle after accepting the request?"
related_patterns:
  - "[[pattern-saga]]"
  - "[[pattern-orchestrator-workers]]"
  - "[[pattern-idempotency-key]]"
---

## Problem

You've identified work that should not block the inbound request. Four shapes exist: inline in-process tasks (FastAPI BackgroundTasks, threading, `asyncio.create_task`), a durable queue with separate workers, a workflow engine (Temporal, Prefect, Airflow), or an event-triggered serverless function. Each trades durability, throughput, and operational complexity differently. The classic trap is defaulting to in-process tasks and discovering at the first crash that runs are being lost silently.

## Criteria

- **Durability** — must the task survive process crash, deploy, or host loss?
- **Volume** — events per minute vs. per second vs. per millisecond?
- **Delay semantics** — immediate, scheduled, periodic, long-running (minutes to days)?
- **Retry and delivery guarantees** — at-most-once / at-least-once / exactly-once with compensation?
- **Operational complexity budget** — can the team run a broker, a workflow engine, or only a process?
- **Caller visibility** — does the caller need a status or result handle after accepting the request?

## Recommendation

| Situation | Choose |
|---|---|
| Short, fast work, loss on crash is acceptable, low volume | **Inline in-process** (FastAPI `BackgroundTasks`, `asyncio.create_task`) — no pattern needed |
| Durable, short-to-medium work; caller needs status; volume fits a single broker | [[pattern-async-request-reply]] over a queue, with [[pattern-competing-consumers]] on the worker side |
| Durable, bursty, producer must not block on slow consumers; back-pressure matters | [[pattern-queue-based-load-leveling]] + [[pattern-competing-consumers]] |
| Long-running (minutes to days), multi-step, needs timers, retries, compensation | **Workflow engine** (Temporal, Prefect, Airflow) — no direct Carta pattern; often composes with [[pattern-saga]] |
| Event-triggered, spiky, operational-cost-sensitive | **Serverless triggered function** (Lambda, Cloud Run Jobs) — no direct Carta pattern; pair with [[pattern-idempotency-key]] |
| Agent-driven fan-out and aggregation of LLM subtasks | [[pattern-orchestrator-workers]] (agentic variant) |

In every durable option, make each task idempotent — retries happen constantly. Use [[pattern-idempotency-key]] at the HTTP boundary if callers can retry creates.

## Fallback

When in doubt, choose a durable queue over inline in-process. The operational cost is one more moving part; the cost of losing production work on every deploy is much higher. Inline is legitimate for ephemeral, low-stakes work (cache warming, fire-and-forget telemetry) where loss on crash is explicitly acceptable — but that acceptance should be stated, not assumed.
