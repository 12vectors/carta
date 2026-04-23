---
id: context-ml-system
title: Machine Learning System
type: context
maturity: stable
tags: [context, stable, ml, mlops]
signals:
  - "Trains, fine-tunes, evaluates, or deploys machine learning models"
  - "Has a model lifecycle (train → validate → deploy → monitor → retrain)"
  - "Monitors for data drift, concept drift, or model performance degradation"
  - "Maintains feature pipelines, feature stores, or training datasets as first-class artefacts"
  - "Reproducibility of experiments, models, and data is a first-class requirement"
recommended_patterns:
  - "[[pattern-pipeline]]"
  - "[[pattern-async-request-reply]]"
  - "[[pattern-cache-aside]]"
  - "[[pattern-read-replica]]"
  - "[[pattern-structured-logging]]"
  - "[[pattern-distributed-tracing]]"
  - "[[pattern-rate-limiting]]"
  - "[[pattern-health-check-endpoint]]"
  - "[[pattern-deployment-stamps]]"
  - "[[pattern-circuit-breaker]]"
  - "[[pattern-retry-with-backoff]]"
  - "[[pattern-feature-flag]]"
recommended_standards: []
common_antipatterns:
  - "[[antipattern-silent-failure]]"
  - "[[antipattern-self-judging-llm]]"
related:
  - "[[context-data-pipeline]]"
  - "[[context-agentic-system]]"
  - "[[context-web-application]]"
sources:
  - "Designing Machine Learning Systems (Huyen, O'Reilly, 2022)"
  - "Machine Learning Design Patterns (Lakshmanan, Robinson, Munn, O'Reilly, 2020)"
  - "Hidden Technical Debt in Machine Learning Systems (Sculley et al., NeurIPS 2015)"
  - "https://learn.microsoft.com/en-us/azure/architecture/ai-ml/"
---

## Description

A system whose core function is training, evaluating, deploying, or monitoring machine learning models. The defining shape is the model lifecycle — training pipelines produce models, serving infrastructure exposes them, monitoring detects drift, and feedback loops trigger retraining. Decisions are dominated by reproducibility, experiment tracking, feature management, drift, and the cost-latency profile of inference. Inference itself may be online (per-request, latency-bound) or batch (throughput-bound), and most real systems do both.

## Key concerns

- **Reproducibility.** Data, features, code, hyperparameters, and random seeds must all be captured to reconstruct a model.
- **Drift.** Input distributions and ground truth shift over time; drift monitoring is continuous, not one-shot.
- **Feature consistency.** Training-serving skew is the classic silent bug — point-in-time correct feature retrieval is required.
- **Inference mode.** Online, batch, and streaming inference have different latency, throughput, and cost shapes.
- **Governance.** Model cards, bias testing, versioning, and rollback are first-class, not optional.

## Typical architecture

- **Training pipeline** — data extraction, feature engineering, training, evaluation, registration as a pipeline of jobs.
- **Online serving** — low-latency HTTP or gRPC endpoint backed by a model artefact, often with caching and autoscaling.
- **Batch inference** — scheduled jobs scoring large datasets; output to a table or file.
- **Feature store + model registry** — managed stores for features and models that training and serving both read.

## See also

- [[context-data-pipeline]] — training pipelines are data pipelines with extra ceremony.
- [[context-agentic-system]] — systems where models are used for reasoning at runtime, not just prediction.
- [[context-web-application]] — model-serving endpoints usually live behind a web API.
- [[dtree-choose-service-boundary]] — split training, serving, and monitoring into separate services or fold them into one.
- [[dtree-choose-data-access]] — pick the feature-read strategy for serving latency.
