---
title: Observability
category: practices
summary: Build systems that explain themselves through logs, metrics, and traces, so you can answer new questions about production without shipping new code.
tags: [operations, reliability, debugging]
---

# Observability

> **In one sentence:** Build systems that explain themselves through logs, metrics, and traces, so you can answer new questions about production without shipping new code.

## The idea

**Monitoring** tells you *whether* something is wrong: "error rate is above 2%." **Observability** lets you figure out *why*: "errors are only from Android users on version 4.2 hitting the EU region, and they started after the 14:05 deploy."

A system is observable when you can understand its internal state from the data it emits — its **telemetry**. The three main kinds:

- **Logs** — timestamped records of events. Best when **structured** (JSON with named fields), not free text.
- **Metrics** — numbers over time: request rate, error rate, latency, queue depth. They're often tagged with **labels** like `region=eu` or `status=500`. Cheap to store, great for dashboards and alerts.
- **Traces** — the path of a single request across services, showing where time was spent. A trace is made of **spans**: one timed step each, such as a service call or a database query.

## Why it matters

In a distributed system, failures are rarely simple. A slow response might come from a database lock three services away. Without good telemetry, debugging means guessing, adding log lines, redeploying, and waiting — while users suffer.

Good observability can shorten incidents from hours to minutes, and lets you deploy with confidence because you'll *see* if something goes wrong. To know whether yours is working, track time-to-diagnose in your [[blameless-postmortems|postmortems]].

## How to apply it

- **Use structured logs with consistent fields.** At minimum: `traceId`, `userId`, `service`, `durationMs`.
- **Propagate a trace ID through every call.** A trace ID (also called a correlation ID) lets you follow one request everywhere. OpenTelemetry is the common standard.
- **Measure the four golden signals for each service.** They are latency, traffic, errors, and **saturation** — how full the service is: CPU, memory, connection pools, queue depth ([[backpressure]]). The list comes from Google's *Site Reliability Engineering* book (2016).
- **Define SLOs (service level objectives).** For example: "99.9% of checkouts succeed in under 1s." The 0.1% allowed to fail is your **error budget**. Alert when you're burning through it faster than planned, not on every blip.
- **Alert on symptoms users feel, not on causes.** "Checkout is failing" pages someone; "CPU at 80%" or "a circuit breaker opened" goes to a dashboard ([[circuit-breaker]]). The exception is a near-certain failure that will hurt users before any symptom shows, like a disk about to fill or a certificate about to expire; page on those.
- **Add context at the edges.** Log what came in and what went out at system boundaries.
- **Budget for telemetry.** It can become a large share of infrastructure spend. Sample traces deliberately — keep all errors and slow requests, sample the rest.

## Example

Users report checkout is slow:

1. The checkout latency dashboard shows p99 (the latency 99% of requests beat) jumped from 400ms to 3s at 14:05.
2. Filtering traces to slow requests shows 2.5s spent in the `inventory` service.
3. In those traces, `inventory`'s database span shows a query added in the 14:03 deploy. Running `EXPLAIN` on it confirms a full table scan.
4. Roll back, add an index, done. Twenty minutes, no guessing.

## Common traps

- **Logging everything.** Huge, noisy logs are expensive and hide the signal. Log meaningful events with context.
- **Alert fatigue.** Too many non-actionable alerts teach people to ignore pages. Every alert should require a human action.
- **High-cardinality metric labels.** Each unique label value creates a separate time series; a `userId` label with millions of values creates millions of series and explodes costs. Put high-cardinality fields like user ID, app version, and region on **traces and structured logs** instead — that's exactly the data that answers questions like the Android example above.
- **Sampling away what you need.** Random sampling can drop the one failing request you're looking for. Keep errors and slow requests.
- **Logging secrets or personal data.** Scrub tokens, passwords, and personally identifiable information (PII) at the source.
- **Adding telemetry only after an incident.** Make it part of "done" for every feature.

## When it doesn't apply

A small internal tool or batch script needs little more than basic logs and a failure alert. A reasonable progression: start every service with structured logs and the four golden signals, and add distributed tracing once a typical request crosses more than two or three services.

## Related

- [[blameless-postmortems]] — turning what telemetry reveals into lasting fixes.
- [[circuit-breaker]] — breaker state changes are key signals to monitor.
- [[event-driven-architecture]] — async flows are especially hard to debug without tracing.
- [[feature-flags]] — pair flag rollouts with metrics to see their impact.
- [[idempotency]] — log the idempotency key alongside the trace ID to see which retries belong to one action.
- [[paved-roads]] — bake telemetry into service templates so every team gets it for free.
