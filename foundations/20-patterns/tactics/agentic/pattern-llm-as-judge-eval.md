---
id: pattern-llm-as-judge-eval
title: LLM-as-Judge Evaluation
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, experimental, agentic, evaluation, quality]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-internal-tool]]"
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-reflexion]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023) — https://arxiv.org/abs/2306.05685"
  - "Introducing Structured Outputs in the API (OpenAI, 2024) — https://openai.com/index/introducing-structured-outputs-in-the-api/"
---

## When to use

- Output quality is fuzzy: tone, helpfulness, faithfulness, relevance.
- No deterministic oracle exists and human labelling is too slow or costly.
- You need scalable regression testing across many prompts or models.
- Pairwise preference is enough — "A better than B" beats absolute scores.
- Agent loops need an automated stop or scoring signal.

## When NOT to use

- A deterministic verifier exists — tests, schemas, rules — use that.
- Stakes demand human review (legal, medical, safety decisions).
- Judge and generator are the same model and family — self-bias invalidates.
- Your eval set is too small to detect judge noise (< ~50 items).
- Output is code or data with objective correctness criteria.

## Decision inputs

- Judge rubric: pairwise preference, rubric score, or pass/fail.
- Judge model distinct from the generator; ideally different vendor or family.
- Structured output schema for judge decisions (enum + rationale).
- Calibration set with human labels to measure judge agreement.
- Position, verbosity, and self-preference bias mitigations.
- Cost budget: judges run on every eval or sample.

## Solution sketch

For each candidate output, prompt a judge model with the task, the output (or two outputs for pairwise), and a rubric. Require structured output — an enum verdict plus a short rationale — so results aggregate. Use a different model family for the judge than the generator to reduce self-preference bias. For pairwise, randomise order per pair to control position bias; optionally swap and require consistency. Calibrate the judge on a small human-labelled set; report agreement (accuracy or Cohen's kappa) alongside the eval. Re-calibrate on every judge-model or rubric change. Treat the judge as a noisy instrument: aggregate over many items, don't trust single scores.

## Trade-offs

| Gain | Cost |
|------|------|
| Scales fuzzy evaluation beyond human capacity | Judge agreement with humans is imperfect and drifts |
| Pairwise is cheap, robust, and actionable | Position, verbosity, and self-preference biases |
| Structured verdicts aggregate across runs | Calibration against human labels is ongoing work |
| Works across model vendors | Judge-model upgrades silently shift your metric |
| Enables automated regression gates | Per-eval token cost adds up on large suites |

## Implementation checklist

- [ ] Pick pairwise preference over absolute scores where possible.
- [ ] Use a judge model from a different family than the generator.
- [ ] Require structured output: verdict enum plus short rationale.
- [ ] Randomise order in pairwise; optionally require swap-consistency.
- [ ] Maintain a human-labelled calibration set; report agreement.
- [ ] Version the rubric and judge model alongside the eval.
- [ ] Re-calibrate after any rubric or judge-model change.
- [ ] Keep eval suites large enough to detect judge noise.
- [ ] Never ship a product metric backed only by self-judgment.

## Stage-specific notes

- **At [[stage-prototype]]**: same-family judge (Claude judging Claude) is acceptable if the self-bias risk is documented in the README. Cross-family judge is MVP work, not a prototype gate.
- **At [[stage-mvp]]**: introduce a small human-labelled calibration set (20–50 exchanges per dimension) and measure judge–human agreement. Drifting agreement means the rubric prompt needs revision before the scores do.
- **At [[stage-production]]**: cross-family judge becomes the floor, not the aspiration. Report agreement metrics on every run; regressions in agreement page the owner the same way latency regressions do.
- **At [[stage-critical]]**: multi-judge ensemble or human spot-check sampling on a fixed percentage of every run. Judge-model regressions become an explicit error-budget line item.

## See also

- [[pattern-reflexion]] — inner-loop use of a judge to drive retries.
- [[pattern-structured-logging]] — persist verdicts and rationales.
