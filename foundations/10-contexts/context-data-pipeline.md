---
id: context-data-pipeline
title: Data Pipeline
type: context
maturity: stable
tags: [context, stable, data, batch, streaming]
signals:
  - "Processes bounded or unbounded datasets through a sequence of transformations"
  - "Throughput and cost-per-record dominate design over request-level latency"
  - "Idempotent reprocessing is a baseline expectation"
  - "Schema evolution and data quality are first-class operational concerns"
recommended_patterns:
  - "[[pattern-pipeline]]"
  - "[[pattern-event-driven-architecture]]"
  - "[[pattern-dead-letter-channel]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-sharding]]"
recommended_standards: []
common_antipatterns: []
related:
  - "[[context-event-driven-system]]"
sources:
  - "Designing Data-Intensive Applications (Kleppmann, O'Reilly, 2017) — https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/"
  - "Streaming Systems (Akidau, Chernyak, Lax, O'Reilly, 2018)"
---

## Description

A system that ingests, transforms, and lands data — either in bounded batches or as an unbounded stream. The defining shape is a directed graph of transformations through which records flow. Decisions are dominated by throughput, cost per record, correctness under retry, and schema evolution, not by per-request latency.

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

- [[context-event-driven-system]] — streaming pipelines are the data-flavour specialisation of event-driven.
