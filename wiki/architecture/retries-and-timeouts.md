---
title: Retries and Timeouts
category: architecture
summary: Give every remote call a deadline, retry only failures that might succeed next time, and space retries out with backoff and jitter so recovery doesn't turn into a retry storm.
tags: [resilience, distributed-systems, reliability]
---

# Retries and Timeouts

> **In one sentence:** Give every remote call a deadline, retry only failures that might succeed next time, and space retries out with backoff and jitter so recovery doesn't turn into a retry storm.

## The idea

Networks drop packets, servers restart, and databases have bad seconds. Many failures are **transient**: try again a moment later and it works. Retrying hides these blips from users.

But retries are dangerous when done naively. If a service is struggling and every caller instantly retries three times, its load quadruples at the worst possible moment. That's a **retry storm**, and it turns a hiccup into an outage.

Two tools work together:

- **Timeout** — how long you'll wait for a response before giving up. Without one, a hung call can hold a thread or connection forever.
- **Retry policy** — which failures to retry, how many times, and how long to wait between attempts.

## Why it matters

Almost every outage in a distributed system involves timeouts set wrong or retries that amplified load. Getting these two settings right is one of the cheapest reliability wins available — and one of the most commonly skipped.

## How to apply it

- **Set a timeout on every remote call.** Library defaults are often minutes, or infinite. Pick a value from real latency data (e.g., a bit above the p99, the latency 99% of requests beat).
- **Retry only what's retryable.** Timeouts, connection resets, `503 Service Unavailable`, and `429 Too Many Requests` usually are. `400 Bad Request` or `404 Not Found` never are — the same request will fail the same way.
- **Retry only safe operations.** Reads are safe. Writes are safe only if they are idempotent — repeating them has no extra effect (see [[idempotency]]).
- **Back off exponentially.** Wait 100ms, then 200ms, then 400ms… so a struggling service gets breathing room.
- **Add jitter.** Jitter is a random amount added to each wait. Without it, a thousand clients that failed together retry together, in synchronized waves.
- **Cap attempts and total time.** Two or three retries is typical. Respect a `Retry-After` header when the server sends one.
- **Use a retry budget.** Limit retries to a fraction of normal traffic (say 10%). When failures are widespread, retries stop instead of multiplying.
- **Propagate deadlines.** Pass the remaining time budget down the call chain. Each hop should give up *before* its caller does, so no service keeps working on a request nobody is waiting for.
- **Retry at one layer only.** If the browser, the gateway, and three services each retry three times, one failure becomes 3⁵ = 243 attempts.

## Example

A checkout service calls a payment service, which calls a fraud-check service.

**Before:** checkout has a 2s timeout. Payment has a 10s timeout on fraud check and retries three times with no delay. Fraud check slows down. Checkout gives up after 2s and the user clicks "Pay" again — but payment is still retrying fraud check for up to 40 seconds on the *first* request. Fraud check's load climbs fivefold and it falls over.

**After:** checkout sets a 2s deadline and passes it along. Payment gives fraud check 1.5s, retries once with jittered backoff only if time remains, and returns a clear error otherwise. Only payment retries; checkout doesn't. Load on fraud check during the slowdown rises by at most 10% instead of 400%.

## Common traps

- **No timeout at all.** The most common mistake, and the most expensive.
- **Callers that give up before callees.** If the upstream timeout is shorter than the downstream one, downstream keeps doing work nobody will use — and the caller's retry adds more.
- **Retrying non-idempotent writes.** This is how customers get charged twice.
- **Fixed, synchronized retry intervals.** Every client hits the server at the same instant.
- **Retries hiding a real problem.** Track retry rates; a rising rate is an early warning.

## When it doesn't apply

Inside one process, there's nothing to time out or retry. For long-running background work, a durable queue with redelivery is usually better than in-process retries. And when a dependency is clearly down, stop retrying altogether — that's the job of a [[circuit-breaker]].

## Related

- [[circuit-breaker]] — stops retries entirely when a dependency is clearly unhealthy.
- [[backpressure]] — what the server should do when retries arrive faster than it can cope.
- [[idempotency]] — the property that makes retrying a write safe.
- [[observability]] — retry and timeout rates are early warning signals.
