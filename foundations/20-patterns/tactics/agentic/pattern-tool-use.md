---
id: pattern-tool-use
title: Tool Use (Function Calling)
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-operational-excellence]]"
  - "[[pillar-reliability]]"
tags: [pattern, experimental, agentic, tool-use, function-calling]
applies_to:
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-react-loop]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-idempotency-key]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Toolformer: Language Models Can Teach Themselves to Use Tools (Schick et al., 2023) — https://arxiv.org/abs/2302.04761"
  - "Model Context Protocol (Anthropic, 2024) — https://www.anthropic.com/news/model-context-protocol"
---

## When to use

- Task needs access to live data, computation, or side-effecting systems.
- The set of actions is bounded and expressible as typed functions.
- You want the model to choose actions, not just generate text.
- You need auditable calls with structured arguments and results.
- Multiple downstream services must be composable behind one agent.

## When NOT to use

- Pure text transformation with no external state.
- Action space is unbounded or undocumented — define a narrower tool first.
- Calls are latency-critical and the tool layer adds round-trips.
- Model lacks reliable function-calling support for your schema complexity.
- You cannot enforce idempotency or authorisation on the tool targets.

## Decision inputs

- Tool count and schema complexity versus model capability on your evals.
- Auth model: per-user identity, service account, or delegated token.
- Idempotency keys for retries of non-safe tools.
- Rate limits per tool and per caller.
- Dry-run / confirm-before-execute for destructive actions.
- Schema language: vendor-native JSON schema, MCP, or in-house.

## Solution sketch

Expose each capability as a typed function: name, description, input schema, output schema. Register the set with the model at invocation. On each turn, parse the model's tool call, validate arguments against the schema, authorise the caller, execute, and return a structured result. Reject invalid calls with a machine-readable error the model can correct. Keep tool descriptions short and disambiguating — names and docstrings are the contract. Prefer a protocol (MCP-style) over bespoke wiring when exposing the same tools to multiple agents. Log every call with correlation ID, arguments, and outcome.

## Trade-offs

| Gain | Cost |
|------|------|
| Grounds model in real systems and data | Each tool expands attack surface and failure modes |
| Structured arguments enable validation and audit | Schema drift between model and runtime breaks silently |
| Composable: same tools work across agents | Prompt tax — large tool lists degrade selection quality |
| Vendor-agnostic via JSON schema / MCP | Function-calling quality varies sharply across models |
| Testable in isolation from the model | Authorisation and idempotency must be solved per tool |

## Implementation checklist

- [ ] Define tools with typed input and output schemas.
- [ ] Validate arguments before execution; return structured errors.
- [ ] Enforce authorisation at the tool boundary, not in the prompt.
- [ ] Require idempotency keys for non-safe actions.
- [ ] Apply per-tool rate limits and timeouts.
- [ ] Keep tool count small; split agents before exceeding ~20 tools.
- [ ] Evaluate tool selection accuracy on a fixed task set.
- [ ] Log calls with correlation ID, arguments, result, and duration.
- [ ] Gate destructive tools behind dry-run or human approval.
- [ ] Prefer a portable protocol (e.g. MCP) over per-vendor wiring.

## See also

- [[pattern-react-loop]] — the common host loop for tool use.
- [[pattern-retry-with-backoff]] — retry transient tool failures.
- [[pattern-idempotency-key]] — make retries safe for side-effecting tools.
- [[pattern-rate-limiting]] — protect tool backends from runaway loops.
- [[pattern-human-in-the-loop-interrupt]] — approval gate for high-risk tools.
