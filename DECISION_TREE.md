# Decision Tree

Top-level routing for agents performing a Carta traversal. This document maps a task to one or more contexts in `10-contexts/`, which in turn link to recommended patterns.

---

## How to use

1. Read the task description.
2. Work through the **signal table** below. For each context, check whether the task exhibits the listed signals. A context applies if **any** of its signals match.
3. Most tasks match one primary context and zero or more secondary contexts. Identify all that apply — don't stop at the first match.
4. If no context matches, see **Unmatched tasks** at the bottom.
5. Proceed to the matched context node(s) in `10-contexts/` and follow their `recommended_patterns` links.

Contexts are not mutually exclusive. A conversational AI product is both `context-agentic-system` and `context-web-application`. A real-time analytics dashboard is both `context-data-pipeline` and `context-web-application`. Apply all relevant contexts; the pattern intersection is where the useful guidance lives.

---

## Signal table

Each row lists the signals that indicate a context is relevant. Signals are observable properties of the task or system, not implementation choices.

| Context | Signals |
|---------|---------|
| [[context-web-application]] | Serves HTTP requests to users or other services. Has a UI, API endpoints, authentication, sessions, or request-response cycles. Users interact with it through a browser or mobile client. |
| [[context-data-pipeline]] | Moves, transforms, or enriches data between systems. Has stages (extract, transform, load). Cares about throughput, schema evolution, data quality, and lineage. May be batch or streaming. |
| [[context-ml-system]] | Trains, evaluates, serves, or monitors machine learning models. Has a model lifecycle (training, validation, deployment, monitoring). Cares about reproducibility, feature management, and model drift. |
| [[context-agentic-system]] | Uses LLMs or other AI models as reasoning components. Has tool use, multi-step planning, memory, or autonomous decision-making. May orchestrate multiple models or agents. Cares about guardrails, observability, and human-in-the-loop controls. |
| [[context-event-driven-system]] | Components communicate through events rather than direct calls. Has producers, consumers, event stores, or message brokers. Cares about ordering, idempotency, eventual consistency, and event schema evolution. |
| [[context-batch-processing]] | Processes large volumes of data on a schedule or trigger rather than continuously. Has jobs, schedulers, checkpointing, and retry logic. Cares about idempotency, failure recovery, and resource efficiency. Distinct from data pipelines in that the focus is execution rather than data flow. |

---

## Disambiguation

When signals overlap, these distinctions help:

**Data pipeline vs batch processing.** A data pipeline is defined by the *flow of data* between systems — extraction, transformation, loading, lineage tracking. Batch processing is defined by *how work is executed* — scheduled jobs, chunked processing, checkpointing. A nightly ETL job is both. A Spark job that computes aggregates without moving data between systems is batch processing but not a data pipeline. When both apply, use both.

**ML system vs agentic system.** An ML system has a model lifecycle — training, evaluation, deployment, monitoring for drift. An agentic system uses models as reasoning engines at runtime — tool use, planning, memory. A system that fine-tunes a model and deploys it behind an API is an ML system. A system that gives an LLM access to tools and lets it plan multi-step actions is an agentic system. A system that does both is both.

**Event-driven system vs web application.** A web application that uses an event bus internally is both. The web application context covers the request-response surface; the event-driven context covers the asynchronous interior. Apply both when the architecture has both layers.

---

## Common combinations

These multi-context scenarios appear frequently. When you identify one, apply all listed contexts:

| Scenario | Contexts |
|----------|----------|
| Conversational AI product | agentic-system + web-application |
| RAG system | agentic-system + data-pipeline (for indexing) + web-application (for serving) |
| Real-time analytics dashboard | data-pipeline + web-application |
| ML model serving behind an API | ml-system + web-application |
| Event-sourced web application | event-driven-system + web-application |
| Scheduled data processing | batch-processing + data-pipeline |
| Agent with model fine-tuning | agentic-system + ml-system |

These are starting points, not exhaustive. If the task matches a combination not listed here, apply all relevant contexts anyway.

---

## Unmatched tasks

If no context in the signal table matches the task:

1. **Check whether the task is architectural.** Some tasks (refactoring a function, fixing a bug, updating a dependency) don't require architectural pattern selection. Carta may not be needed. Report this and stop.

2. **Check whether a context is missing.** If the task describes a system type not covered by any existing context (e.g., embedded systems, desktop applications, infrastructure-as-code), note the gap. This is a signal that a new context node should be authored. Report the gap and proceed with whatever partial matches exist.

3. **Proceed pattern-by-pattern.** If no context matches but the task is clearly architectural, skip the context layer and go directly to `20-patterns/`. Search by category (communication, data, resilience, scaling, security, agentic, observability) rather than by context. This is less guided but still useful.
