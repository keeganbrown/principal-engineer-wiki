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

**Backpressure** is that push back, in software. A consumer tells its producer: "I'm full; slow down." The term comes from fluid dynamics — resistance against flow in a pipe. Without it, the only "buffer" is unbounded queues and memory, and they *will* run out.

## Why it matters

Every system has a maximum throughput. When input exceeds it, something has to give. Your choices are:

1. **Buffer** — queue the extra work (only works if the burst is short).
2. **Slow the producer** — backpressure proper.
3. **Drop or reject** — shed load deliberately. Across a network, a fast rejection with a `Retry-After` header is also how a service tells its producer to slow down.
4. **Crash** — what happens if you choose none of the above.

Systems without backpressure fail in the worst way: latency climbs for *everyone*, memory fills, the process dies, and its load shifts to the next node, which also dies. That's a cascading failure.

## How to apply it

- **Bound every queue.** An unbounded queue is a crash waiting to happen. Decide what happens when it's full.
- **Reject early and clearly.** Return `429 Too Many Requests` or `503 Service Unavailable` with a `Retry-After` header. A fast "no" beats a slow timeout.
- **Let consumers pull.** A worker that takes the next job only after finishing the last naturally limits its own load.
- **Limit concurrency per caller.** Cap in-flight requests per client or per dependency, so one noisy caller can't use everything. This is the **bulkhead** pattern, named for the sealed compartments that keep one leak from sinking a ship.
- **Rate-limit at the edge.** Limit per user or per API key, before work reaches expensive layers.
- **Prioritize when shedding.** Drop analytics events before checkout requests. Agree the shedding order with product ahead of time, because shedding means deliberately failing some users, and deciding which ones during an incident is too late.
- **Make clients cooperate.** They should retry with exponential backoff (each wait longer than the last) and **jitter** (a random extra delay, so clients don't all retry at the same moment), and respect `Retry-After`. See [[retries-and-timeouts]].
- **Watch queue depth and wait time.** Treat them as first-class metrics ([[observability]]).

## Example

An image-processing service accepts uploads and resizes them. A marketing campaign triples traffic.

**Without backpressure:** the in-memory job queue grows to millions of items, the service runs out of memory, restarts, loses every queued job, and clients retry all at once — making it worse.

**With backpressure:** accepted jobs go to a bounded, durable queue holding 10,000 items. Workers pull jobs at their own pace. When the queue is full, the upload API returns `503` with `Retry-After: 30`. The autoscaler adds workers based on queue depth — up to what the database behind them can take; past that, more workers just move the overload.

No *accepted* job is lost. But rejection doesn't make the extra work disappear — it hands the waiting back to the client. The mobile app can hold the photo and retry later; a browser upload form fails if the user closes the tab.

So the team decides per client. The mobile app gets rejections. The web form gets a "we'll process this shortly" response, and its uploads go to cheap object storage that can hold far more than the work queue. That store is still a queue, so it has its own cap and an alert on the age of its oldest item; once the backlog is older than users will tolerate, the form stops promising "shortly" and starts rejecting too.

## Common traps

- **"Just add a queue."** A queue absorbs bursts but doesn't fix sustained overload; it just delays the failure.
- **Letting retry and timeout settings amplify load.** Retries without backoff, and callers whose timeout is shorter than the service they call (so it keeps working on requests nobody is waiting for), both add work exactly when you're weakest; see [[retries-and-timeouts]].
- **Backpressure that stops at a boundary.** If the service rejects, but the frontend auto-retries instantly, nothing improved.

## When it doesn't apply

If your load stays predictably below capacity, you'll rarely hit these problems; low-volume internal tools can often get by with simple timeouts. But any system exposed to the public internet, a batch import, or a marketing launch eventually needs a plan for overload.

## Related

- [[circuit-breaker]] — protects callers from a failing dependency; backpressure protects a service from its callers.
- [[retries-and-timeouts]] — how clients should behave when they're pushed back.
- [[event-driven-architecture]] — queues and consumers are where backpressure usually lives.
- [[observability]] — queue depth and rejection rates are key signals.
- [[idempotency]] — rejected work will be retried, so it must be safe to repeat.
