---
id: solution-llm-eval-harness
title: LLM Evaluation Harness
type: solution
maturity: stable
tags: [solution, stable, agentic, eval, llm-as-judge]
composes:
  - "[[pattern-pipeline]]"
  - "[[pattern-orchestrator-workers]]"
  - "[[pattern-llm-as-judge-eval]]"
  - "[[pattern-llm-budget-enforcement]]"
  - "[[pattern-prompt-injection-defense]]"
  - "[[pattern-idempotency-key]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-correlation-id]]"
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-internal-tool]]"
prerequisites: []
related:
  - "[[pattern-tool-use]]"
  - "[[pattern-react-loop]]"
  - "[[dtree-choose-background-work]]"
sources:
  - "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023) — https://arxiv.org/abs/2306.05685"
  - "Building effective agents (Anthropic, 2024) — https://www.anthropic.com/engineering/building-effective-agents"
  - "OpenAI Evals — https://github.com/openai/evals"
  - "Evaluating LLM-based Applications (Eugene Yan, 2024) — https://eugeneyan.com/writing/llm-evaluators/"
---

## Problem

You have an LLM-powered product (chatbot, agent, copilot, eval workbench) and need to know whether prompt changes, model upgrades, or orchestration changes make it better or worse — without manually reading every output. Manual review is fine for ten conversations, untenable for a thousand. The team needs a repeatable harness that replays scenarios against the system, scores the results along named dimensions, and produces comparable numbers across runs.

This is the shape of every serious eval workbench in production use today: tools like OpenAI Evals, Anthropic's internal evals, LangSmith, Langfuse, and in-house harnesses at companies shipping LLM features. It pairs naturally with agent-orchestration systems where behaviour is non-deterministic and correctness is behavioural.

## Composition

The harness combines seven patterns. Order reflects implementation sequence:

1. **[[pattern-pipeline]]** — the overall shape. A run is a pipeline of stages: *scenario selection → execution → exchange capture → evaluation → aggregation*. Each stage produces typed artefacts consumed by the next. Restartable from any stage.
2. **[[pattern-orchestrator-workers]]** — a coordinator (the scenario runner) drives N persona workers in parallel. Each worker holds one conversational turn-loop against the system under test. Bounded concurrency via a semaphore.
3. **[[pattern-llm-as-judge-eval]]** — an evaluator LLM scores each captured exchange against a rubric per dimension (e.g. security, appropriateness, fidelity). This is the component whose calibration matters most; plan it first, not last.
4. **[[pattern-llm-budget-enforcement]]** — per-run token/cost ceiling. Without this, a poorly-bounded scenario loop or a large dataset × expensive model can burn through the provider bill in minutes.
5. **[[pattern-prompt-injection-defense]]** — imported exchanges and persona configs are untrusted input from the model's perspective. Strict role separation: persona instructions in system prompts; external text in user/tool roles; no concatenation.
6. **[[pattern-idempotency-key]]** — evaluations are expensive; a retried run must not re-score the same exchanges. Each exchange carries an idempotent key consumable by the evaluator.
7. **[[pattern-structured-logging]]** + **[[pattern-correlation-id]]** — a run ID ties the scenario, every turn, every judge call, and every score together. At prototype stage a print-with-fields approach is enough; at MVP, structured JSON + tracing is mandatory for debugging eval regressions.

```
[scenarios] -> [runner]--(N workers)--> [system under test] -> [exchanges]
                   ↓                                                ↓
             [budget counter]                            [judge (LLM-as-eval)]
                                                                    ↓
                                                             [scored exchanges]
                                                                    ↓
                                                              [aggregated run]
```

The first four patterns are mandatory at every stage. The last three are MVP-graduation additions that prototype harnesses legitimately defer.

## Decision inputs

- **Rubric design.** Are you scoring along predefined dimensions (safety, helpfulness, on-spec), free-form judge rationale, or a hybrid? Predefined scales better; free-form lets you discover failure modes.
- **Judge model choice.** Cross-family judge (e.g. GPT grading Claude) is methodologically cleaner but doubles provider contracts. Same-family is acceptable at prototype if self-bias is documented. Cross-family becomes a production floor.
- **Persona fidelity.** LLM-driven personas with structured outputs (e.g. via Instructor) cover more ground than scripted turns but cost more per run. Weak personas produce weak signal regardless of rubric quality.
- **Calibration set.** Do you have a small human-labelled set to measure judge agreement? Without it, judge drift is invisible.
- **Scope of coverage.** A handful of canonical scenarios vs. a large generated scenario set. Small + high quality beats large + noisy for iteration speed.
- **Execution durability.** In-process background tasks are fine at prototype; production harnesses need durable queues and restartable workers (see [[dtree-choose-background-work]]).

## Trade-offs

| Gain | Cost |
|------|------|
| Repeatable, comparable eval without per-output manual review | LLM judges are noisy; without a calibration set, scores can drift unnoticed |
| Fast iteration on prompts and model choice — compare N vs N+1 | Budget can spike if scenarios generate long turns; hard per-run caps are mandatory |
| Catches multi-turn failure modes humans miss in one-shot review | Persona quality bounds signal quality — bad personas produce misleading pass rates |
| Structured artefacts (runs, exchanges, scores) become the eval dataset | Storage and replay infrastructure grow with scenario count |
| Composition is stage-appropriate — prototype can skip logging/idempotency without breaking the core | Teams under-invest in judge calibration and self-bias controls |

## Implementation sequence

A prototype-stage implementation order that graduates cleanly to MVP:

1. **Pick dimensions first.** Concrete rubric per dimension (e.g. "Does the bot refuse out-of-scope requests? y/n/partial"). Change later if needed but start concrete.
2. **Implement the pipeline skeleton.** Stages as pure functions: `scenarios → runs`, `runs → exchanges`, `exchanges → scores`, `scores → aggregates`. Typed I/O.
3. **Build persona-agent loops** with [[pattern-orchestrator-workers]]. Bound concurrency via a semaphore from day one — unbounded fan-out is the classic foot-gun.
4. **Wire the judge** with [[pattern-llm-as-judge-eval]]. Structured outputs (JSON mode or equivalent) so scores are parseable, not prose.
5. **Add budget enforcement** ([[pattern-llm-budget-enforcement]]). A per-run token counter with a hard cap is sufficient at prototype; Redis / provider proxy is MVP.
6. **Enforce role separation** ([[pattern-prompt-injection-defense]]). Persona and scenario text never concatenate into the system prompt.
7. **Persist runs, exchanges, scores** as versioned artefacts — Parquet, JSON Lines, or SQLite. Raw exchanges are the replayable truth; treat them as such.
8. *(MVP graduation)* Add idempotency keys on expensive stages so restarts don't re-score. Add structured logging + correlation IDs so cross-component debugging is possible.
9. *(MVP graduation)* Build a calibration set — 20–50 human-labelled exchanges per dimension. Measure agreement between judge and human quarterly. Rebuild rubric prompts when agreement drifts.
10. *(Production graduation)* Move from in-process BackgroundTasks to a durable queue (see [[dtree-choose-background-work]]). Cross-family judge. Error budgets on judge latency and agreement.

## See also

- [[pattern-llm-as-judge-eval]] — the most-calibration-sensitive component of the composition.
- [[pattern-llm-budget-enforcement]] — the non-negotiable control even at prototype stage.
- [[pattern-orchestrator-workers]] — the turn-loop orchestration shape.
- [[dtree-choose-background-work]] — the graduation path for execution durability.
- [[stage-prototype]], [[stage-mvp]], [[stage-production]] — the stages this solution graduates through.
