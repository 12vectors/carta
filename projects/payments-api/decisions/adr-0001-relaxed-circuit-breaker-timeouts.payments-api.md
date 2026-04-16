---
id: adr-0001-relaxed-circuit-breaker-timeouts
title: Relaxed Circuit Breaker Timeouts for Payment Processors
type: adr
maturity: stable
tags: [adr, stable]
status: accepted
date: 2025-06-10
supersedes: ""
superseded_by: ""
affects:
  - "[[pattern-circuit-breaker]]"
related:
  - "[[pattern-retry-with-backoff]]"
  - "[[adr-0001-fastapi-as-default.org]]"
sources:
  - "Stripe API documentation — https://docs.stripe.com/api/timeouts"
  - "Internal incident report: INC-2025-0342 (false circuit trips during 3D Secure peak)"
---

## Context

The payments-api integrates with external payment processors (currently Stripe, with Adyen planned). The foundation circuit breaker pattern recommends a 5-second timeout and 50% failure threshold over 10 requests.

During load testing and early production traffic, we observed:

1. **3D Secure verification flows routinely take 10-20 seconds.** These are not failures — they're the processor waiting for the cardholder's bank to respond. A 5-second timeout treats these as failures and trips the circuit.
2. **Cross-border transactions take 8-15 seconds.** Payment processors route these through multiple banking networks. Again, slow but not failing.
3. **Incident INC-2025-0342:** during a Friday evening peak, 3D Secure volume spiked. The 5-second timeout caused the circuit to open, rejecting all payment attempts for 30 seconds. Revenue impact was significant.

The foundation default is correct for most service-to-service calls. Payment processors are a specific case where latency is inherently high but reliability is also high — the slowness is a feature of the banking system, not a failure signal.

## Decision

Override the circuit breaker configuration for payment processor calls in the payments-api:

- **Timeout: 30 seconds** (up from 5 seconds). Accommodates 3D Secure and cross-border transaction latency.
- **Failure threshold: 40% over 20 requests** (relaxed from 50% over 10 requests). Larger window and lower threshold reduce false trips from isolated slow requests.
- **Half-open probe interval: 60 seconds** (up from 30 seconds). Payment processor recovery is usually at the infrastructure level — give it time.
- **Fallback: async queue** rather than immediate failure. Payments are high-value, high-intent operations.

The foundation defaults (5s timeout, 50%/10 threshold) remain in effect for all other dependencies within the payments-api (internal services, cache, database).

## Consequences

**Positive:**
- Eliminates false circuit trips during normal 3D Secure and cross-border flows.
- Async fallback preserves payment intent — users see "processing" not "failed."
- Per-processor circuit isolation means a Stripe issue doesn't affect Adyen traffic.

**Negative:**
- 30-second timeout means a genuinely failed request ties up resources longer before being recognised.
- Async retry queue introduces eventual consistency — the user doesn't know immediately if payment succeeded.
- More complex monitoring: two circuit configurations (30s for processors, 5s for everything else) instead of one.
- Genuine processor outages take longer to detect (larger window, lower threshold).

**Neutral:**
- This override is specific to payment processor calls. If we add new external dependencies (e.g. fraud scoring, identity verification), we'll need to evaluate their timeout characteristics separately.

## Alternatives considered

**Keep foundation defaults (5s / 50% / 10 requests)**
Rejected. The data from load testing and INC-2025-0342 clearly shows these defaults cause false trips during normal payment flows. The cost of false trips (lost revenue, degraded user experience) exceeds the cost of slower failure detection.

**Increase timeout to 15s instead of 30s**
Rejected. 15 seconds covers most 3D Secure flows but not cross-border transactions. We'd still see false trips for international payments, which are a significant portion of volume.

**Remove circuit breaker for payment processor calls entirely**
Rejected. When a processor genuinely goes down, the circuit breaker is essential for preventing cascading failures. The goal is to tune it, not remove it.
