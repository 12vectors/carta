---
id: pattern-pipeline
title: Pipeline (Pipes and Filters)
type: pattern
category: style
maturity: stable
pillars:
  - "[[pillar-performance]]"
  - "[[pillar-operational-excellence]]"
tags: [pattern, stable, style, data-processing, streaming]
applies_to:
  - "[[context-web-application]]"
  - "[[context-data-pipeline]]"
prerequisites: []
related:
  - "[[pattern-event-driven-architecture]]"
conflicts_with: []
contradicted_by: []
sources:
  - "Fundamentals of Software Architecture (Richards & Ford, O'Reilly, 2020) ch. 11"
  - "https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/"
---

## When to use

- Data transformation workloads — ETL, log processing, media encoding, compilation.
- Workflows that decompose naturally into ordered, single-purpose steps.
- Systems where each stage has different scaling or resource needs.
- Pipelines where stages can be reused across multiple flows.

## When NOT to use

- Highly interactive request/response workloads with tight latency bounds.
- Workflows with heavy cross-stage state or back-edges — pipeline shape breaks down.
- Small transformations where a single function is simpler than a multi-stage topology.
- Systems needing transactional consistency across stages.

## Decision inputs

- Stage fan-out/fan-in topology (linear, branching, merging).
- Per-stage throughput and back-pressure behaviour.
- Failure semantics — replay, skip, dead-letter.
- Data contract between stages (schema, serialisation).
- Orchestrator: stream processor, workflow engine, or plain queues.

## Solution sketch

Decompose work into **filters** (stateless processing units) connected by **pipes** (channels carrying data). Each filter reads input, transforms, emits output. Filters are independent and composable. Pipes provide buffering and decoupling — often a queue or stream.

```
[ source ] -> [ filter A ] -> [ filter B ] -> [ filter C ] -> [ sink ]
```

Four filter types per Richards & Ford: producer, transformer, tester, consumer. Stages scale independently. See ch. 11 (linked) for topology variants and performance guidance.

## Trade-offs

| Gain | Cost |
|------|------|
| Stages scale and deploy independently | Orchestration, monitoring, and schema versioning overhead |
| Strong composability and reuse | Cross-stage debugging spans multiple logs and queues |
| Back-pressure and buffering via pipes | End-to-end latency = sum of stage latencies + queue dwell |
| Natural fit for streaming and batch | Poor fit for request/response or transactional flows |

## Implementation checklist

- [ ] Define stage boundaries with explicit input/output schemas.
- [ ] Keep filters stateless where possible; externalise state.
- [ ] Choose a pipe technology (Kafka, SQS, Flink, Airflow) per durability needs.
- [ ] Define replay and dead-letter behaviour per stage.
- [ ] Emit per-stage metrics (lag, throughput, error rate).
- [ ] Version schemas and plan for backward-compatible evolution.
- [ ] Load-test each stage independently before end-to-end.

## See also

- [[pattern-event-driven-architecture]] — pipelines often run over event buses.
- [[pattern-queue-based-load-leveling]] — pipe-level mechanism for smoothing load.
- [[pattern-dead-letter-channel]] — standard failure-handling for filter stages.
