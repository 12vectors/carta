---
id: pattern-llm-budget-enforcement
title: LLM Budget Enforcement
type: pattern
category: agentic
maturity: experimental
pillars:
  - "[[pillar-cost]]"
  - "[[pillar-reliability]]"
  - "[[pillar-security]]"
tags: [pattern, experimental, agentic, cost, llm, budget]
applies_to:
  - "[[context-agentic-system]]"
  - "[[context-web-application]]"
prerequisites: []
related:
  - "[[pattern-rate-limiting]]"
  - "[[pattern-throttling]]"
  - "[[pattern-tool-use]]"
  - "[[pattern-orchestrator-workers]]"
  - "[[pattern-react-loop]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Azure API Management: LLM token limit policy — https://learn.microsoft.com/en-us/azure/api-management/azure-openai-token-limit-policy"
  - "Anthropic API Rate Limits — https://docs.anthropic.com/en/api/rate-limits"
  - "OpenAI Rate Limits — https://platform.openai.com/docs/guides/rate-limits"
---

## When to use

- Multi-tenant LLM features where one tenant can drive the provider bill.
- Autonomous agent loops (`[[pattern-react-loop]]`, `[[pattern-orchestrator-workers]]`) that can run away under pathological input.
- Paid-per-token providers (Anthropic, OpenAI, Gemini) where request count alone doesn't bound spend.
- Any public or semi-public endpoint that invokes an LLM without a cost-bounding intermediary.

## When NOT to use

- Fixed-cost on-prem or self-hosted models where marginal spend per token is effectively zero.
- Systems where upstream provider quota already binds total spend and per-tenant fairness isn't required.
- Single-user developer tools where the user holds their own provider key and pays directly.
- Hard real-time paths where the pre-call counter check dominates the latency budget.

## Decision inputs

- Principal granularity — per user, per session, per project, per org, per feature?
- Budget period — hourly, daily, monthly, rolling window?
- Breach action — block, degrade (smaller/cheaper model), queue with delay, or alert-only?
- Cost measurement — input+output tokens, provider-reported dollar cost, or locally-computed estimate from cached unit prices?
- Enforcement point — API gateway, app middleware, or LLM-provider proxy (LiteLLM, Portkey, Azure APIM)?

## Solution sketch

Maintain a counter per principal (user, project, org) over the budget window, keyed in a fast store with TTL (Redis, Dynamo, or in-process for single-instance). **Pre-call** check: if `counter + estimated_cost` exceeds the budget, reject or degrade. **Post-call** update: increment counter with the provider's reported usage (tokens-in, tokens-out, dollar estimate). Alert at configurable thresholds (50%, 80%, 100%). Provide an override path for incident response and VIP grants. Reconcile internal counters against provider billing daily — drift indicates a unit-price bug.

```
[request] -> [pre-call check: counter + est_cost ≤ budget?]
                        |
                no <---- + ----> yes
                 |              |
              reject          call LLM
                               |
                         [post-call: counter += actual_usage]
```

## Trade-offs

| Gain | Cost |
|------|------|
| Bounds per-actor spend; one bad tenant cannot drain the org's budget | Counter storage, atomic increment, TTL semantics |
| Surfaces runaway agentic loops and abusive prompts before the bill does | Users hit budget walls — needs clear UX and escalation |
| Enables per-tier pricing and fair-use multi-tenancy | Cost accuracy depends on an up-to-date unit-price table |
| Separates cost-control from request-rate control | Adds a dependency on the counter store on every call |

## Implementation checklist

- [ ] Define the principal (user, session, project, org) and the budget unit (tokens, dollars, requests).
- [ ] Store counters with explicit TTL matching the budget window.
- [ ] Pre-call: atomic read-check-block on the counter.
- [ ] Post-call: update counter with the provider's reported usage, not the pre-call estimate.
- [ ] Emit alerts at 50%, 80%, 100% of budget to the responsible team or principal.
- [ ] Implement an override mechanism for incidents and short-term grants, with audit.
- [ ] Log every rejection with principal, period, budget, and cause.
- [ ] Reconcile daily: internal counter totals vs. provider billing totals.
- [ ] Load-test counter race conditions under burst and TTL rollover.
- [ ] Make budget-breach errors distinguishable from other 4xx/5xx at the API surface.

## See also

- [[pattern-rate-limiting]] — per-client request-rate cap; complements budget enforcement but does not replace it (a few expensive requests can still bust a budget).
- [[pattern-throttling]] — server-side load-shedding; different lever, same symptom surface.
- [[pattern-tool-use]] — each model-invocable tool is a potential cost multiplier per turn.
- [[pattern-orchestrator-workers]] — fan-out amplifies cost; enforce budgets at the orchestrator, not per worker.
- [[pattern-react-loop]] — loop iterations multiply tokens; iteration caps and budgets together bound spend.
