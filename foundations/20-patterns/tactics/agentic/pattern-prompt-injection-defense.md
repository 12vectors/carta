---
id: pattern-prompt-injection-defense
title: Prompt Injection Defense
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
tags: [pattern, experimental, agentic, security, llm, prompt-injection]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-internal-tool]]"
  - "[[context-web-application]]"
prerequisites:
  - "[[pattern-input-validation]]"
related:
  - "[[pattern-tool-use]]"
  - "[[pattern-human-in-the-loop-interrupt]]"
  - "[[pattern-llm-budget-enforcement]]"
  - "[[pattern-structured-logging]]"
conflicts_with: []
contradicted_by: []
sources:
  - "OWASP LLM Top 10: LLM01 — Prompt Injection (2025) — https://genai.owasp.org/llmrisk/llm01-prompt-injection/"
  - "Mitigating jailbreaks and prompt injections (Anthropic, 2024) — https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks"
  - "Prompt injection archive (Willison, ongoing) — https://simonwillison.net/tags/prompt-injection/"
---

## When to use

- LLM receives user-provided text that could attempt to override system instructions.
- LLM output triggers real-world effects (tool calls, messages sent, data written).
- Untrusted content (web pages, documents, third-party exchanges) is mixed into the context window.
- Multi-tenant LLM features where one user's input reaches another user's context.
- Any public or semi-public LLM endpoint without a hardened intermediary.

## When NOT to use

- Single-user developer tools where the user is the only source of input and trusts themselves.
- Pure-text generation with no tool use and no downstream effects beyond display.
- Hard-sandboxed environments where the worst-case model output is a displayed string.
- Fixed-prompt systems where no user input reaches the context window at all.

## Decision inputs

- Trust boundary — which parts of the context come from untrusted sources, and which from system owners?
- Output routing — does model output trigger tool calls, write data, or return to users only?
- Content-source trust — is any retrieved or imported content treated as equivalent to user input?
- Tolerance for false positives — how much legitimate use can be refused by defences?
- Enforcement points — input validation, prompt structure, tool arg validation, output checks, or all of the above.

## Solution sketch

Treat user-sourced text as **data**, not **instructions**. Concretely:

1. **Separate roles structurally.** System prompt holds the instructions; user input goes only in user-role messages. Never concatenate user text into the system prompt.
2. **Validate tool-call arguments.** Every tool call the model produces is validated against its schema before execution; arguments never bypass validation because "the model meant it".
3. **Harden downstream effects.** Destructive actions (writes, sends, payments) require either a human checkpoint ([[pattern-human-in-the-loop-interrupt]]) or a second, independent check on the action payload.
4. **Separate untrusted content.** Retrieved documents, imported exchanges, and tool outputs are framed explicitly as untrusted content in the prompt.
5. **Defence in depth.** Input classifiers, prompt design, tool-arg validation, and output-side checks each fail independently; layer them.

```
[user text] --(data)--> [user message]
[system owner] --> [system prompt — instructions only]
[model output] --> [tool-arg validator] --> [side-effect gate (HITL or auto-check)] --> [action]
```

Complete prevention is not currently achievable; the goal is bounded blast radius.

## Trade-offs

| Gain | Cost |
|------|------|
| Reduces hijack of model instructions via user-supplied text | Extra validation layers add latency and complexity |
| Tool-arg validation catches arguments the model produced under attack | Legitimate edge-case prompts may be refused; needs tuning |
| Human-in-the-loop on destructive actions bounds worst-case damage | UX friction; users dislike frequent approval prompts |
| Defence-in-depth survives single-layer bypasses | More moving parts to maintain as models and attack techniques evolve |

## Implementation checklist

- [ ] Inventory every place user, tool, or retrieved text enters the context window.
- [ ] Enforce strict role separation: instructions in system, data in user/tool roles.
- [ ] Validate every tool-call argument against a schema before execution.
- [ ] Put a human checkpoint on destructive actions (send, write, pay, execute).
- [ ] Tag retrieved content as untrusted in the prompt structure itself.
- [ ] Log every refused or suspected-injection input with correlation ID for review.
- [ ] Add output-side checks for leaked secrets or prohibited actions.
- [ ] Run a red-team pass against known injection patterns before shipping.
- [ ] Re-evaluate quarterly — attack patterns evolve faster than model defences.

## Stage-specific notes

- **At [[stage-prototype]]**: concatenating operator-supplied persona, scenario, or config text into the system prompt is acceptable — the operator is the trust boundary. Third-party content in any prompt (retrieved docs, tool outputs, bot transcripts fed to a judge) is untrusted at every stage; tag it structurally, never splice it into the system prompt.
- **At [[stage-mvp]]**: audit every prompt site for external-content concatenation. Add explicit "untrusted content follows" markers around retrieved text, tool outputs, and transcripts. Log suspected-injection inputs by correlation ID.
- **At [[stage-production]]**: layer defences — input classifier, prompt structure, tool-arg validation, output-side checks. Cross-family judge removes the transcript-injection attack on self-scoring pipelines.
- **At [[stage-critical]]**: scheduled red-team pass against known injection patterns; output filter alerts on suspected secret leakage.

## See also

- [[pattern-input-validation]] — prerequisite; prompt-injection defence sits on top.
- [[pattern-tool-use]] — the tool surface is the attacker's primary target; narrow it.
- [[pattern-human-in-the-loop-interrupt]] — the last-line defence for destructive actions.
- [[pattern-llm-budget-enforcement]] — bounds the cost of injection-driven loops.
- [[pattern-structured-logging]] — required to review suspected-injection events.
