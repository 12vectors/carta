---
id: pattern-orchestrator-workers
title: Orchestrator-Workers
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-performance]]"
tags: [pattern, experimental, agentic, orchestration, multi-agent]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-internal-tool]]"
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-plan-then-execute]]"
  - "[[pattern-human-in-the-loop-interrupt]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Building effective agents (Anthropic, 2024) — https://www.anthropic.com/engineering/building-effective-agents"
  - "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation (Wu et al., 2023) — https://arxiv.org/abs/2308.08155"
---

## When to use

- Task splits into subtasks with different skills, tools, or context needs.
- Subtasks can run in parallel for wall-clock wins.
- Each worker benefits from a narrower prompt and smaller tool set.
- You need role isolation: e.g. retriever, coder, reviewer.
- One agent with all tools is hitting selection or context limits.

## When NOT to use

- Task fits comfortably in a single agent with a small tool set.
- Subtasks are tightly coupled; coordination overhead outweighs wins.
- You lack observability to debug cross-agent failures.
- Budget cannot absorb the orchestrator's additional turns.
- A deterministic pipeline would do — avoid LLMs coordinating LLMs.

## Decision inputs

- Worker boundary: by skill, by data source, or by tool group.
- Communication shape: structured handoff, shared state, or message bus.
- Orchestrator model vs. worker model capability and cost.
- Concurrency and timeout per worker; aggregate deadline.
- Failure policy: fail task, retry worker, substitute worker, degrade.
- Termination: orchestrator decides, quorum, or fixed DAG.

## Solution sketch

One orchestrator agent decomposes the task and dispatches subtasks to specialised workers; workers return structured results; orchestrator synthesises. Workers do not call each other directly — all routing flows through the orchestrator to preserve auditability and bound fan-out. Define each worker's input and output as a typed schema. Parallelise independent workers; serialise where outputs feed into the next. Keep the orchestrator model strong (it's the bottleneck) and workers narrow and cheap. Enforce per-worker budgets and timeouts. Collapse the pattern to plan-then-execute when the plan is known up front; use orchestrator-workers when the orchestrator must react to worker results and dispatch more work.

```
         [orchestrator]
        /      |       \
   [worker] [worker] [worker]   (parallel or DAG)
        \      |       /
         [orchestrator synth]
```

## Trade-offs

| Gain | Cost |
|------|------|
| Focused prompts and tool sets per worker | Orchestrator turns add latency and cost |
| Parallel workers reduce wall-clock time | Coordination and error handling complexity |
| Role isolation improves quality and audit | Cross-agent failures are hard to debug without tracing |
| Scales past single-agent tool-count limits | Risk of reinventing a workflow engine poorly |
| Works across model vendors | Emergent loops and chatter without strict turn caps |

## Implementation checklist

- [ ] Define workers by a single responsibility and a typed schema.
- [ ] Route all inter-worker communication through the orchestrator.
- [ ] Set per-worker timeout, token budget, and turn cap.
- [ ] Parallelise independent workers with a hard fan-out limit.
- [ ] Specify failure policy per worker: retry, substitute, or fail.
- [ ] Trace orchestrator and workers under one correlation ID.
- [ ] Emit metrics: worker failure rate, parallel efficiency, total cost.
- [ ] Prefer a deterministic pipeline when the DAG is stable.
- [ ] Evaluate end-to-end; regressions often hide in the orchestrator.

## See also

- [[pattern-plan-then-execute]] — when the plan is produced once up front.
- [[pattern-human-in-the-loop-interrupt]] — approval gates on dispatched work.
- [[pattern-distributed-tracing]] — required to debug multi-agent runs.
- [[pattern-rate-limiting]] — cap fan-out against downstream tools.
