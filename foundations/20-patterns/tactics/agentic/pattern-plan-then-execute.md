---
id: pattern-plan-then-execute
title: Plan-Then-Execute
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-cost]]"
tags: [pattern, experimental, agentic, planning, orchestration]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-orchestrator-workers]]"
  - "[[pattern-react-loop]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Plan-and-Solve Prompting (Wang et al., 2023) — https://arxiv.org/abs/2305.04091"
  - "How we built our multi-agent research system (Anthropic, 2024) — https://www.anthropic.com/engineering/built-multi-agent-research-system"
---

## When to use

- Task decomposes into discrete, mostly-independent steps.
- You want to preview and validate the plan before any side effects.
- Steps can run on cheaper or smaller models than the planner.
- Parallelisable subtasks would benefit from explicit scheduling.
- Auditors require a written plan separate from execution traces.

## When NOT to use

- Task state changes unpredictably mid-run — use ReAct instead.
- Steps are tightly dependent and each result reshapes the next.
- The planner cannot see enough context to produce a usable plan.
- Task is short enough that planning overhead dwarfs execution.
- You lack a contract to validate the plan against before executing.

## Decision inputs

- Planner model vs. executor model capability and cost split.
- Whether steps are ordered, parallelisable, or a DAG.
- Replan trigger: on error, on drift, never.
- Plan validation: schema, rules, human review, dry-run.
- Maximum steps per plan and maximum depth of subtasks.
- Isolation between executors: shared state, message passing, or sandbox.

## Solution sketch

Two phases. Phase 1 (plan): a planner model produces a structured list of steps — each with a goal, inputs, expected output, and assigned tool or worker. Validate the plan (schema, budget, forbidden actions) before execution. Phase 2 (execute): run steps in declared order or as a DAG; each executor is a focused agent or deterministic function. Collect results and return. On step failure, either fail the task, retry the step, or trigger a bounded replan — pick one policy and stick to it. Use a cheaper model for executors when each step is narrow. Differentiates from ReAct: planning and execution are separated, not interleaved.

## Trade-offs

| Gain | Cost |
|------|------|
| Plan is inspectable before any side effect | Stale plan if the environment shifts mid-run |
| Cheaper executors per step reduce total cost | Planner errors compound across the whole run |
| Parallel steps reduce wall-clock time | Coordination, state-passing, and failure handling complexity |
| Clean audit trail: plan + per-step results | Replanning logic is subtle; easy to loop |
| Works across model vendors | Unsuitable for tasks with unpredictable branching |

## Implementation checklist

- [ ] Define a plan schema: step id, goal, tool, inputs, dependencies.
- [ ] Validate plans against budget, forbidden actions, and step cap.
- [ ] Choose an executor model appropriate to step complexity.
- [ ] Specify a single failure policy: fail, retry, or bounded replan.
- [ ] Parallelise independent steps; declare dependencies explicitly.
- [ ] Persist plan and per-step results with correlation IDs.
- [ ] Emit metrics: plan size, step failures, replan count.
- [ ] Dry-run or human-review plans that touch high-risk systems.
- [ ] Evaluate end-to-end on a fixed task set.

## See also

- [[pattern-orchestrator-workers]] — runtime shape for executing the plan.
- [[pattern-react-loop]] — alternative when interleaved reasoning is required.
- [[pattern-human-in-the-loop-interrupt]] — approve plans before execution.
- [[pattern-distributed-tracing]] — trace plan and step execution together.
