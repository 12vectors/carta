---
id: antipattern-self-judging-llm
title: Self-Judging LLM
type: antipattern
category: agentic
maturity: experimental
tags: [antipattern, experimental, agentic, evaluation, llm-as-judge, bias]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-ml-system]]"
  - "[[context-internal-tool]]"
mitigated_by:
  - "[[pattern-llm-as-judge-eval]]"
sources:
  - "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023) — https://arxiv.org/abs/2306.05685"
  - "LLM Evaluators Recognize and Favor Their Own Generations (Panickssery et al., 2024) — https://arxiv.org/abs/2404.13076"
---

## How to recognise

- Same model family (Claude-judges-Claude, GPT-judges-GPT) used as both generator and judge in an eval pipeline.
- No cross-family judge used for periodic calibration runs.
- No human-labelled calibration set; judge–human agreement is never measured.
- README or eval docs do not flag the self-bias limitation.
- Scores drift across same-family model versions and the drift is treated as signal, not noise.

## Why it happens

- Cost — a second vendor doubles the provider contract surface and billing footprint.
- Convenience — the same SDK, same auth, same Instructor wrapper already exists for the generator; reuse is trivial.
- Latency and regional affinity — same-vendor calls are often faster and cheaper per token.
- Complacency — "we picked a frontier model, it's fine"; evaluation needs *independence*, not capability.

## Consequences

- Scores systematically favour the generator's own style, phrasing, and reasoning shape.
- Comparative evaluations (prompt A/B, model-upgrade decisions) are invalid — the winner tends to be whichever candidate looks most like the judge.
- Regressions are invisible: when judge and generator update in lockstep, new failure modes go unmeasured.
- Downstream product decisions anchored on these scores inherit the bias without warning.

## How to fix

- Introduce a cross-family judge at least for periodic calibration runs, even if day-to-day eval still uses the same-family judge at prototype stage.
- Maintain a small human-labelled calibration set (20–50 exchanges per dimension) and measure judge–human agreement quarterly.
- Document the same-family limitation explicitly in the README or eval-harness docs whenever prototype-stage constraints preclude cross-family.
- At production stage, cross-family judge becomes the floor — not aspirational. Report agreement metrics on every run and page on drift.

## See also

- [[pattern-llm-as-judge-eval]] — the pattern this antipattern constrains. Its Stage-specific notes describe the graduation path.
- [[solution-llm-eval-harness]] — the composition where this antipattern most often hides. Calibration is an MVP-graduation step.
- [[stage-prototype]] — where same-family judging is acceptable *if documented*.
- [[stage-production]] — where cross-family judge becomes the floor.
