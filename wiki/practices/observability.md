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

A system is observable when you can understand its internal state from the data it emits. The three main kinds of data, often called the "three pillars":

- **Logs** — timestamped records of events. Best when **structured** (JSON with fields), not free text.
- **Metrics** — numbers over time: request rate, error rate, latency, queue depth. Cheap to store, great for dashboards and alerts.
- **Traces** — the path of a single request across services, showing where time was spent.

## Why it matters

In a distributed system, failures are rarely simple. A slow response might come from a database lock three services away. Without good telemetry, debugging means guessing, adding log lines, redeploying, and waiting — while users suffer.

Good observability shortens incidents from hours to minutes and lets you deploy with confidence because you'll *see* if something goes wrong.

## How to apply it

- **Use structured logs** with consistent fields: `request_id`, `user_id`, `service`, `duration_ms`.
- **Propagate a trace/correlation ID** through every call so you can follow one request everywhere. OpenTelemetry is the common standard.
- **Measure the golden signals** for each service: **latency, traffic, errors, saturation**.
- **Define SLOs** (service level objectives) — e.g., "99.9% of checkouts succeed in under 1s" — and alert on burning through that budget, not on every blip.
- **Alert on symptoms users feel**, not on causes. "Checkout is failing" pages someone; "CPU at 80%" goes to a dashboard.
- **Add context at the edges.** Log what came in and what went out at system boundaries.

## Example

Users report checkout is slow. With observability:

1. The checkout latency dashboard shows p99 jumped from 400ms to 3s at 14:05.
2. Filtering traces by slow requests shows 2.5s spent in the `inventory` service.
3. `inventory` logs for those trace IDs show a new query added in the 14:03 deploy is doing a full table scan.
4. Roll back, add an index, done. Twenty minutes, no guessing.

## Common traps

- **Logging everything.** Huge, noisy logs are expensive and hide the signal. Log meaningful events with context.
- **Alert fatigue.** Too many non-actionable alerts teach people to ignore pages. Every alert should require a human action.
- **High-cardinality metrics.** Putting `user_id` as a metric label can explode costs; put it in logs and traces instead.
- **Logging secrets or personal data.** Scrub tokens, passwords, and PII at the source.
- **Adding telemetry only after an incident.** Make it part of "done" for every feature.

## When it doesn't apply

A small internal tool or batch script needs little more than basic logs and a failure alert. Scale your investment to the system's criticality and complexity — but almost everything in production deserves *some*.

## Related

- [[circuit-breaker]] — breaker state changes are key signals to monitor.
- [[event-driven-architecture]] — async flows are especially hard to debug without tracing.
- [[feature-flags]] — pair flag rollouts with metrics to see their impact.
- [[idempotency]] — request IDs serve both deduplication and tracing.
