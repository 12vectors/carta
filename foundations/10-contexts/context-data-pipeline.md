---
id: context-data-pipeline
title: Data Pipeline
type: context
maturity: stable
tags: [context, stable, data, batch, streaming, etl]
signals:
  - "Processes bounded or unbounded datasets through a sequence of transformations"
  - "Throughput and cost-per-record dominate design over request-level latency"
  - "Idempotent reprocessing and replay are baseline expectations"
  - "Schema evolution and data quality are first-class operational concerns"
  - "Lineage — where data came from and how it was transformed — matters to downstream consumers"
recommended_patterns:
  - "[[pattern-pipeline]]"
  - "[[pattern-event-driven-architecture]]"
  - "[[pattern-dead-letter-channel]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-message-translator]]"
  - "[[pattern-transactional-outbox]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-idempotency-key]]"
  - "[[pattern-sharding]]"
  - "[[pattern-read-replica]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-correlation-id]]"
  - "[[pattern-circuit-breaker]]"
recommended_standards: []
common_antipatterns: []
related:
  - "[[context-event-driven-system]]"
  - "[[context-batch-processing]]"
  - "[[context-ml-system]]"
sources:
  - "Designing Data-Intensive Applications (Kleppmann, O'Reilly, 2017) ch. 10-11 — https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/"
  - "Streaming Systems (Akidau, Chernyak, Lax, O'Reilly, 2018)"
  - "Fundamentals of Data Engineering (Reis & Housley, O'Reilly, 2022)"
  - "https://learn.microsoft.com/en-us/azure/architecture/data-guide/"
---

## Description

A system that ingests, transforms, and lands data — either in bounded batches or as an unbounded stream. The defining shape is a directed graph of transformations through which records flow. Decisions are dominated by throughput, cost per record, correctness under retry, schema evolution, and lineage. Unlike a request-oriented system, per-request latency is rarely the operative metric; records-per-second and dollars-per-terabyte are. Pipelines commonly straddle batch and streaming — ingest is often streaming, reporting often batch, and both must reconcile against the same source of truth.

## Key concerns

- **Throughput and cost.** Records per second and cost per record are the operative metrics.
- **Idempotence.** Reprocessing the same input must produce the same output; pipelines fail and retry constantly.
- **Schema evolution.** Upstream schemas change; pipelines must handle additive and sometimes breaking changes gracefully.
- **Data quality.** Garbage-in garbage-out is a first-class failure mode — validation and quarantine at each boundary.
- **Backfill and replay.** Re-running history against new logic is a routine operation, not an exception.

## Typical architecture

- **Batch** — scheduled runs over bounded datasets; high throughput, hours-to-days latency.
- **Streaming** — unbounded event stream; seconds-to-minutes latency, continuous operation.
- **Lambda** — batch + streaming in parallel; reconcile at query time.
- **Kappa** — streaming only; reprocess by replaying the log through new logic.

## See also

- [[context-event-driven-system]] — streaming pipelines specialise event-driven for bulk data movement.
- [[context-batch-processing]] — many pipelines run as scheduled batch jobs; the contexts overlap in ETL.
- [[context-ml-system]] — training pipelines are data pipelines with extra ceremony.
- [[dtree-choose-data-access]] — pick the read-access strategy for downstream consumers.
- [[dtree-choose-messaging-style]] — pick the transport between pipeline stages.
