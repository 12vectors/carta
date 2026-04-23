---
id: pattern-reflexion
title: Reflexion (Self-Critique + Retry)
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-reliability]]"
tags: [pattern, experimental, agentic, self-critique, retry]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-internal-tool]]"
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-llm-as-judge-eval]]"
  - "[[pattern-react-loop]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn et al., 2023) — https://arxiv.org/abs/2303.11366"
  - "Self-RAG (Asai et al., 2023) — https://arxiv.org/abs/2310.11511"
---

## When to use

- Task has a verifiable signal: tests pass, schema validates, assertion holds.
- First-pass answers are often close but need correction.
- You can afford 2-3x token cost for a quality lift.
- Failure modes are diverse — static retry with the same prompt won't help.
- Debugging, code repair, or structured generation with clear invariants.

## When NOT to use

- No external verifier or ground truth — critiques become hallucinated approval.
- Latency-sensitive paths where extra turns are unaffordable.
- Tasks where the model's self-assessment is known to be unreliable on your evals.
- When a stronger model, better prompt, or retrieval would fix the gap more cheaply.
- Open-ended creative tasks with no failure criterion.

## Decision inputs

- Verifier signal: unit tests, schema validation, judge model, rule engine.
- Max retry count and total token budget per task.
- Critique granularity: full-rewrite vs. targeted patch.
- Whether critique and attempt share a model or use separate roles.
- Termination: on-pass, on-no-improvement, or hard cap.
- Storage of failure traces for offline prompt improvement.

## Solution sketch

After the agent produces an attempt, run a verifier. On failure, feed the attempt plus the verifier's output back to the model with instructions to critique and retry. Keep the critique in context across iterations — the lesson is the signal, not just the error. Cap retries (2-3 is typical). Use an external deterministic verifier whenever possible; fall back to an LLM judge only for fuzzy criteria. Separate the critique role from the attempt role to reduce the model's bias toward defending its own output. Stop early when the verifier passes or no progress is made between rounds.

```
  attempt -> verify --pass--> done
                  \--fail--> critique -> retry (attempt + critique)
```

## Trade-offs

| Gain | Cost |
|------|------|
| Lifts pass rate on verifiable tasks without training | 2-3x tokens and latency per task |
| Surfaces failure reasons useful for prompt improvement | Without a real verifier, critiques are unreliable |
| Works with any function-calling model | Critique loops can reinforce wrong beliefs — bound them |
| Separates generation from evaluation concerns | Two prompts to maintain and version |
| Failure traces feed offline eval improvements | Adds a critique-prompt tax on every call path |

## Implementation checklist

- [ ] Define a deterministic verifier; use an LLM judge only as fallback.
- [ ] Cap retries (2-3) and total token budget per task.
- [ ] Keep critique text in context; don't just restart.
- [ ] Separate the critique role from the attempt role.
- [ ] Stop on verifier pass or no-progress between rounds.
- [ ] Log attempts, critiques, and outcomes with correlation IDs.
- [ ] Evaluate lift on a fixed task set; remove if lift is marginal.
- [ ] Compare against a stronger single-shot model baseline.

## See also

- [[pattern-llm-as-judge-eval]] — when the verifier must itself be an LLM.
- [[pattern-react-loop]] — embed reflexion between observe and act steps.
- [[pattern-retry-with-backoff]] — the code-only analogue for transient errors.
