---
id: pattern-react-loop
title: ReAct Loop (Reason + Act)
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-operational-excellence]]"
tags: [pattern, experimental, agentic, reasoning, tool-use]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-internal-tool]]"
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-tool-use]]"
  - "[[pattern-reflexion]]"
  - "[[pattern-plan-then-execute]]"
conflicts_with: []
contradicted_by: []
sources:
  - "ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022) — https://arxiv.org/abs/2210.03629"
  - "Building effective agents (Anthropic, 2024) — https://www.anthropic.com/engineering/building-effective-agents"
---

## When to use

- Task requires interleaved reasoning and external actions (search, lookup, compute).
- Outcome depends on information the model does not have at generation time.
- Intermediate observations reshape later steps; a static plan would be stale.
- You need a visible reasoning trace for debugging or audit.
- Task is open-ended with unpredictable branching.

## When NOT to use

- Single-shot tasks that need no external tools or lookups.
- Latency-critical paths where multiple model turns are unaffordable.
- Tasks with a known, stable procedure — use plan-then-execute.
- High-stakes actions without human approval gates or sandboxing.
- Workflows where deterministic code can do the job.

## Decision inputs

- Maximum loop iterations and total token budget per task.
- Tool latency budget per step and aggregate.
- Failure policy: stop, retry, escalate, hand off to human.
- Observation truncation rules for large tool outputs.
- Termination signal (explicit `final_answer` tool vs. heuristic).
- Trace storage and redaction requirements.

## Solution sketch

Loop: `Thought -> Action -> Observation -> Thought -> ...` until the model emits a terminal answer or a cap trips. Each turn: model produces a reasoning step plus one tool call; runtime executes the tool, appends the observation, re-invokes the model. Bound iterations, wall-clock, and tokens. Treat tool errors as observations the model can react to — do not swallow them. Persist the full trace (redacted) for replay and eval. Keep the tool surface small; every tool adds attack surface and cognitive load. Prefer one-tool-per-turn; parallel actions only when the model supports structured parallel calls and the tools are side-effect-free.

```
  [prompt] -> LLM -> (thought, action) -> tool -> observation -> LLM -> ...
                                                                     \-> final
```

## Trade-offs

| Gain | Cost |
|------|------|
| Grounds answers in fresh, external data | Multi-turn latency and token cost per task |
| Reasoning trace aids debugging and eval | Traces leak intermediate prompts — redact before storage |
| Adapts to tool errors mid-task | Loops can thrash without hard caps |
| Simple to implement on any function-calling model | Prompt drift as context grows; summarisation needed |
| Works across model vendors | Quality degrades sharply on weak models |

## Implementation checklist

- [ ] Define a bounded tool set with typed schemas.
- [ ] Set hard caps on iterations, wall-clock, and tokens.
- [ ] Require a terminal tool or sentinel to end the loop.
- [ ] Surface tool errors as observations, not exceptions.
- [ ] Truncate or summarise long observations before reinjection.
- [ ] Persist full trace with correlation ID; redact secrets.
- [ ] Emit metrics: steps, tool-error rate, termination cause.
- [ ] Gate destructive tools behind approval or dry-run.
- [ ] Evaluate against a fixed task set on every prompt change.

## See also

- [[pattern-tool-use]] — the action half of the loop.
- [[pattern-reflexion]] — add self-critique between iterations.
- [[pattern-plan-then-execute]] — alternative when steps are predictable.
- [[pattern-human-in-the-loop-interrupt]] — pause before risky actions.
- [[pattern-structured-logging]] — log each thought/action/observation.
