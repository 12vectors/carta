---
id: pattern-human-in-the-loop-interrupt
title: Human-in-the-Loop Interrupt
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-security]]"
  - "[[pillar-reliability]]"
tags: [pattern, experimental, agentic, human-in-the-loop, approval]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-internal-tool]]"
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-react-loop]]"
  - "[[pattern-tool-use]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Making it easier to build human-in-the-loop agents with interrupt (LangChain, 2024) — https://www.langchain.com/blog/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt"
  - "Building effective agents (Anthropic, 2024) — https://www.anthropic.com/engineering/building-effective-agents"
---

## When to use

- Agent actions are irreversible, costly, or affect real users.
- Regulation or policy requires a human decision on specific actions.
- Confidence is low or the model requested clarification.
- Action touches PII, payments, production data, or external communications.
- You need a graceful handoff when the agent is out of its depth.

## When NOT to use

- All agent actions are safe, reversible, and sandboxed.
- Human SLA is longer than the task's acceptable latency.
- Decision volume would overwhelm reviewers — narrow the gate or automate.
- You cannot durably persist and resume agent state across the pause.
- Approvals are rubber-stamped — the gate adds cost without signal.

## Decision inputs

- Which action classes trigger an interrupt (allowlist, not denylist).
- Approval SLA and escalation path if the reviewer does not respond.
- Durable state store for pausing and resuming runs.
- Reviewer UI: what context they see; what options they have.
- Audit requirements: who approved, when, with what reason.
- Timeout behaviour: auto-deny, auto-approve, or escalate.

## Solution sketch

Model risky tools so they can emit an `interrupt` instead of executing. The runtime persists the full agent state, emits an approval request to a reviewer channel, and suspends. On approval, rejection, or edit, the runtime resumes the agent with the decision injected as an observation. Reviewers see the proposed action, arguments, and the preceding trace — enough to decide without reading the whole transcript. Define interrupts at the tool boundary, not in the prompt; the prompt cannot be trusted to gate itself. Set a timeout with an explicit default (usually deny). Record the decision and reviewer identity on the run.

## Trade-offs

| Gain | Cost |
|------|------|
| Bounds blast radius of high-risk agent actions | Approval latency breaks real-time UX |
| Clear audit trail of who approved what | Durable state and resumption machinery to build |
| Reviewer edits improve quality over time | Reviewer fatigue leads to rubber-stamping |
| Enables agents in regulated domains | Narrow gate misses new risks as tools evolve |
| Safe fallback for low-confidence cases | Auto-deny timeouts cause silent task failures |

## Implementation checklist

- [ ] Enumerate action classes that require approval (allowlist).
- [ ] Enforce interrupts at the tool layer, not via prompt.
- [ ] Persist full agent state so runs can resume cleanly.
- [ ] Build a reviewer UI with action, arguments, and trace context.
- [ ] Set an explicit timeout and default decision on no-response.
- [ ] Support approve / reject / edit outcomes from reviewers.
- [ ] Log reviewer identity, decision, and rationale with the run.
- [ ] Alert on rubber-stamp patterns (approval rate, time-to-decide).
- [ ] Test resume-from-pause on every release.

## See also

- [[pattern-react-loop]] — the loop that gets paused.
- [[pattern-tool-use]] — enforce the interrupt at the tool boundary.
- [[pattern-idempotency-key]] — required if resumed runs may retry actions.
- [[pattern-structured-logging]] — record approval decisions with run IDs.
