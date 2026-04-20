---
id: context-agentic-system
title: Agentic System
type: context
maturity: experimental
tags: [context, experimental, agentic, llm]
signals:
  - "A language model drives at least part of the control flow"
  - "The system calls tools, retrieves data, or invokes other models based on model output"
  - "Multi-turn interaction with state held across turns"
  - "Observability focus is on traces of reasoning and tool calls, not only request/response"
recommended_patterns:
  - "[[pattern-react-loop]]"
  - "[[pattern-tool-use]]"
  - "[[pattern-plan-then-execute]]"
  - "[[pattern-orchestrator-workers]]"
  - "[[pattern-human-in-the-loop-interrupt]]"
  - "[[pattern-llm-as-judge-eval]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-distributed-tracing]]"
recommended_standards: []
common_antipatterns: []
related:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
sources:
  - "Building effective agents (Anthropic, 2024) — https://www.anthropic.com/engineering/building-effective-agents"
  - "Cognitive Architectures for Language Agents (Sumers et al., 2023) — https://arxiv.org/abs/2309.02427"
---

## Description

A system where a language model participates in control flow — deciding what tool to call next, what to retrieve, whether to reply or continue reasoning. Agentic systems span a spectrum from simple tool-using chatbots to multi-agent orchestration. The defining shape is that some decisions are made by an LLM at runtime, not by the application code.

## Key concerns

- **Non-determinism.** Same input can produce different outputs; tests and deploys must accommodate this.
- **Tool-call safety.** Tools can have real-world effects (send email, modify data); accidental or adversarial invocations are first-class risks.
- **Cost and latency.** Token costs scale with context and iteration count; loops and reflection multiply spend.
- **Evaluation.** Correctness is often judgemental; evals are behavioural, sampled, and statistical rather than unit-test exact.
- **Human oversight.** Non-trivial actions frequently need a human checkpoint — the design question is where, not whether.

## Typical architecture

- **Single-agent loop** — one model, a set of tools, a ReAct-style reason/act loop.
- **Plan-then-execute** — a planner decomposes the task; a cheaper executor runs each step.
- **Orchestrator-workers** — a lead agent delegates subtasks to specialist sub-agents in parallel.
- **Human-in-the-loop** — the agent pauses at defined checkpoints for approval, edit, or rejection.

## See also

- [[context-web-application]] — agents commonly live behind a web API.
- [[context-event-driven-system]] — long-running agent runs often use async events for tool invocation and status.
