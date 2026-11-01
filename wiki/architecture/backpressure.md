---
title: Backpressure
category: architecture
summary: When a component receives work faster than it can handle, it should signal upstream to slow down or shed load, instead of silently piling up work until it collapses.
tags: [resilience, performance, distributed-systems]
---

# Backpressure

> **In one sentence:** When a component receives work faster than it can handle, it should signal upstream to slow down or shed load, instead of silently piling up work until it collapses.

## The idea

Picture a kitchen during a rush. Orders arrive faster than the chefs can cook. If the servers keep pinning tickets to the rail, the queue grows, every meal is late, and eventually food goes out cold or not at all. A good kitchen pushes back: "we're 40 minutes behind — stop seating new tables for a bit."

**Backpressure** is that push back, in software. A consumer tells its producer: "I'm full; slow down." The term comes from fluid dynamics — resistance against flow in a pipe.

Without it, the only "buffer" is unbounded queues and memory, and they *will* run out.

## Why it matters

Every system has a maximum throughput. When input exceeds it, something has to give. Your choices are:

1. **Buffer** — queue the extra work (only works if the burst is short).
2. **Slow the producer** — backpressure proper.
3. **Drop or reject** — shed load deliberately.
4. **Crash** — what happens if you choose none of the above.

Systems without backpressure fail in the worst way: latency climbs for *everyone*, memory fills, the process dies, and its load shifts to the next node, which also dies. That's a cascading failure.

## How to apply it

- **Bound every queue.** An unbounded queue is a crash waiting to happen. Decide what happens when it's full.
- **Reject early and clearly.** Return `429 Too Many Requests` or `503 Service Unavailable` with a `Retry-After` header. A fast "no" beats a slow timeout.
- **Use pull, not push, where possible.** Consumers that fetch work when ready (Kafka consumers, worker pools) naturally limit their own load.
- **Limit concurrency.** Cap in-flight requests per service or per client (bulkheads), so one noisy caller can't consume everything.
- **Rate-limit at the edge** — per user, per API key — before work reaches expensive layers.
- **Prioritize when shedding.** Drop analytics events before checkout requests.
- **Clients must cooperate:** retry with exponential backoff and jitter, and respect `Retry-After`.
- **Watch queue depth and wait time** as first-class metrics.

## Example

An image-processing service accepts uploads and resizes them. A marketing campaign triples traffic.

**Without backpressure:** the in-memory job queue grows to millions of items, the service runs out of memory, restarts, loses every queued job, and clients retry all at once — making it worse.

**With backpressure:** jobs go to a bounded queue holding 10,000 items. Workers pull jobs at their own pace. When the queue is full, the upload API returns `503` with `Retry-After: 30`. Clients back off with jitter. Throughput stays at the service's maximum, nothing is lost, and the autoscaler adds workers based on queue depth.

## Common traps

- **"Just add a queue."** A queue absorbs bursts but doesn't fix sustained overload; it just delays the failure.
- **Retries without backoff** that multiply load exactly when the system is weakest (a "retry storm").
- **Timeouts longer upstream than downstream**, so callers keep waiting for work that's already been abandoned.
- **Backpressure that stops at a boundary.** If the service rejects, but the frontend auto-retries instantly, nothing improved.

## When it doesn't apply

Systems with load that's comfortably and predictably below capacity rarely hit these problems. Low-volume internal tools can often get by with simple timeouts. But any system exposed to the public internet, a batch import, or a marketing launch eventually needs a plan for overload.

## Related

- [[circuit-breaker]] — protects callers from a failing dependency; backpressure protects a service from its callers.
- [[event-driven-architecture]] — queues and consumers are where backpressure usually lives.
- [[observability]] — queue depth and rejection rates are key signals.
- [[idempotency]] — rejected work will be retried, so it must be safe to repeat.
