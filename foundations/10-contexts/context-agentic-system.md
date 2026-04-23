---
id: context-agentic-system
title: Agentic System
type: context
maturity: experimental
tags: [context, experimental, agentic, llm]
signals:
  - "A language model drives at least part of the system's control flow"
  - "The system calls tools, retrieves data, or invokes other models based on model output"
  - "Multi-turn interaction with state held across turns"
  - "Observability focus is on traces of reasoning and tool calls, not only request/response"
  - "Non-determinism of outputs is accepted; correctness is measured behaviourally via evals"
recommended_patterns:
  - "[[pattern-react-loop]]"
  - "[[pattern-tool-use]]"
  - "[[pattern-reflexion]]"
  - "[[pattern-plan-then-execute]]"
  - "[[pattern-orchestrator-workers]]"
  - "[[pattern-human-in-the-loop-interrupt]]"
  - "[[pattern-llm-as-judge-eval]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-distributed-tracing]]"
  - "[[pattern-correlation-id]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-timeout]]"
  - "[[pattern-rate-limiting]]"
  - "[[pattern-llm-budget-enforcement]]"
  - "[[pattern-prompt-injection-defense]]"
  - "[[pattern-cache-aside]]"
  - "[[pattern-feature-flag]]"
recommended_standards: []
common_antipatterns:
  - "[[antipattern-silent-failure]]"
related:
  - "[[context-web-application]]"
  - "[[context-event-driven-system]]"
  - "[[context-ml-system]]"
sources:
  - "Building effective agents (Anthropic, 2024) — https://www.anthropic.com/engineering/building-effective-agents"
  - "Cognitive Architectures for Language Agents (Sumers et al., 2023) — https://arxiv.org/abs/2309.02427"
  - "ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022) — https://arxiv.org/abs/2210.03629"
  - "How we built our multi-agent research system (Anthropic, 2024) — https://www.anthropic.com/engineering/built-multi-agent-research-system"
---

## Description

A system where a language model participates in control flow — deciding what tool to call next, what to retrieve, whether to reply or continue reasoning. Agentic systems span a spectrum from tool-using chatbots to multi-agent orchestration. The defining shape is that some runtime decisions are made by an LLM, not by application code. This shifts the operational model from deterministic request-response to sampled, non-deterministic behaviour where evaluation is behavioural, traces are the primary observability artefact, and tool-call safety becomes a first-class design concern.

## Key concerns

- **Non-determinism.** Same input can produce different outputs; tests, deploys, and incident triage must accommodate this.
- **Tool-call safety.** Tools can have real-world effects (send email, modify data); accidental or adversarial invocations are first-class risks.
- **Cost and latency.** Token costs scale with context and iteration count; loops and reflection multiply spend.
- **Evaluation.** Correctness is judgemental; evals are behavioural, sampled, and statistical rather than unit-test exact.
- **Human oversight.** Non-trivial actions frequently need a human checkpoint — the design question is where, not whether.

## Typical architecture

- **Single-agent loop** — one model, a bounded tool set, a ReAct-style reason/act loop with iteration and token caps.
- **Plan-then-execute** — a planner decomposes the task; a cheaper executor runs each step against a fixed plan.
- **Orchestrator-workers** — a lead agent delegates subtasks to specialist sub-agents in parallel and aggregates.
- **Human-in-the-loop** — the agent pauses at defined checkpoints (risky tool calls, low-confidence outputs) for approval, edit, or rejection.

## See also

- [[context-web-application]] — agents commonly live behind a web API.
- [[context-event-driven-system]] — long-running agent runs often use async events for tool invocation and status.
- [[context-ml-system]] — systems where the model lifecycle (training, fine-tuning, drift) is itself in scope.
- [[dtree-choose-service-boundary]] — decide whether agent orchestration lives in one service or many.
- [[solution-llm-eval-harness]] — composition for building an eval workbench on top of an agentic system.
