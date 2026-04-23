---
id: context-batch-processing
title: Batch Processing
type: context
maturity: stable
tags: [context, stable, batch, jobs, scheduled]
signals:
  - "Processes work in scheduled or triggered jobs rather than continuously"
  - "Inputs are bounded — a dataset, a queue drain, an accumulated backlog"
  - "Jobs checkpoint, retry, and are idempotent across re-runs"
  - "Throughput and cost per record dominate over per-request latency"
  - "Execution is the focus — data movement, if any, is incidental"
recommended_patterns:
  - "[[pattern-pipeline]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-idempotency-key]]"
  - "[[pattern-dead-letter-channel]]"
  - "[[pattern-queue-based-load-leveling]]"
  - "[[pattern-competing-consumers]]"
  - "[[pattern-sharding]]"
  - "[[pattern-timeout]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-correlation-id]]"
recommended_standards: []
common_antipatterns:
  - "[[antipattern-silent-failure]]"
related:
  - "[[context-data-pipeline]]"
  - "[[context-event-driven-system]]"
sources:
  - "Designing Data-Intensive Applications (Kleppmann, O'Reilly, 2017) ch. 10 — https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/"
  - "https://learn.microsoft.com/en-us/azure/architecture/data-guide/big-data/batch-processing"
---

## Description

A system that executes work in discrete, bounded jobs — scheduled (nightly rollups, monthly billing) or triggered (drain a queue, reprocess a backfill). The defining shape is the job: a unit of work with a defined input, defined output, and a predictable runtime window. Decisions are dominated by idempotency, checkpointing, failure recovery, and resource efficiency. Distinct from a data pipeline (which is defined by the flow of data *between* systems); a batch-processing system is defined by *how* the work runs, not *what* moves.

## Key concerns

- **Idempotency.** Jobs fail partway and re-run; rerunning must produce the same output as a single clean run.
- **Checkpointing.** Long jobs save progress so recovery doesn't restart from scratch.
- **Resource efficiency.** Cost per job and per record dominates; elastic compute and spot pricing are often load-bearing.
- **Late and poison data.** Late-arriving or malformed records have explicit policies — quarantine, skip, halt.
- **Observability.** Per-job telemetry (duration, records, errors, resource use) is the operational view; correlation IDs tie runs together.

## Typical architecture

- **Scheduled job** — cron, scheduler, or workflow engine (Airflow, Argo, Azure Data Factory) triggers a run.
- **Chunked processing** — input is partitioned; worker instances process partitions in parallel.
- **Workflow DAG** — multiple jobs chained as a directed graph with dependencies and retries.
- **Elastic compute** — jobs provision compute on demand and release when done to minimise idle cost.

## See also

- [[context-data-pipeline]] — many batch jobs move data; the contexts overlap in ETL.
- [[context-event-driven-system]] — queue-backed events often trigger batch runs.
- [[dtree-choose-messaging-style]] — pick sync vs async when jobs interact with other systems.
