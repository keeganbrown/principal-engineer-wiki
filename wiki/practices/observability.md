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

Good observability can shorten incidents from hours to minutes ([[incident-response]]), and lets you deploy with confidence because you'll *see* if something goes wrong. It only answers the questions your telemetry can answer, though, and the bill grows whether or not anyone looks. To know whether yours is working, track time-to-diagnose in your [[blameless-postmortems|postmortems]].

## How to apply it

- **Use structured logs with consistent fields.** At minimum: `traceId`, `userId`, `service`, `durationMs`.
- **Propagate a trace ID through every call.** A trace ID (the standardized form of what's also called a correlation ID) lets you follow one request everywhere. OpenTelemetry, an open standard and set of libraries for emitting traces, metrics, and logs, is the common choice.
- **Measure the four golden signals for each service.** They are latency, traffic, errors, and **saturation** — how full the service is: CPU, memory, connection pools, queue depth ([[backpressure]]). The list comes from Google's *Site Reliability Engineering* book (2016).
- **Alert on service level objectives (SLOs).** Page when the failures a target allows are being used up faster than planned, not on every blip ([[service-level-objectives]] covers targets and burn-rate alerts).
- **Alert on symptoms users feel, not on causes.** "Checkout is failing" pages someone; "CPU at 80%" or "a circuit breaker opened" (a guard that stops calling a failing dependency) goes to a dashboard ([[circuit-breaker]]). The exception is a near-certain failure that will hurt users before any symptom shows, like a disk about to fill or a certificate about to expire; page on those.
- **Add context at the edges.** Log what came in and what went out at system boundaries.
- **Budget for telemetry.** It can become a large share of infrastructure spend. Sample traces deliberately — keep all errors and slow requests, sample the rest.

## Example

Users report checkout is slow:

1. The checkout latency dashboard shows p99 (the latency 99% of requests beat) jumped from 400ms to 3s at 14:05.
2. Filtering traces to slow requests shows 2.5s spent in the `inventory` service.
3. In those traces, `inventory`'s database span shows a query added in the 14:03 deploy. The database's query plan (`EXPLAIN`) shows it reading every row of the table.
4. Roll back, add an index. Twenty minutes, no guessing.

It worked because the sampler keeps every slow trace. Under the team's old 1% random sampling, most of those slow traces would have been dropped, and step 2 would have found almost nothing.

## Common traps

- **Logging everything.** Huge, noisy logs are expensive and hide the signal. Log meaningful events with context.
- **Alert fatigue.** Too many non-actionable alerts teach people to ignore pages. Every alert should require a human action.
- **High-cardinality metric labels.** Each unique label value creates a separate time series; a `userId` label with millions of values creates millions of series and explodes costs. Put high-cardinality fields like user ID, app version, and region on **traces and structured logs** instead, where they can answer questions like "only Android 4.2 users in the EU."
- **Sampling away what you need.** Random sampling can drop the one failing request you're looking for. Keep errors and slow requests.
- **Logging secrets or personal data.** Scrub tokens, passwords, and personally identifiable information (PII) at the source ([[secrets-management]]).
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
- [[service-level-objectives]] — the targets and burn-rate alerts built on this telemetry.
- [[incident-response]] — what the team does once an alert fires.
