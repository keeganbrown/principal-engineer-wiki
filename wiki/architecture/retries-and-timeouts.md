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

But retries are dangerous when done naively. If a service is struggling and every caller instantly retries three times, each request becomes four attempts and the service's load quadruples at the worst possible moment. That's a **retry storm**, and it turns a hiccup into an outage.

Two tools work together:

- **Timeout** — how long you'll wait for a response before giving up. Without one, a hung call can hold a thread or connection forever.
- **Retry policy** — which failures to retry, how many times, and how long to wait between attempts.

## Why it matters

Timeouts set wrong and retries that amplify load turn up in many outage write-ups — sometimes as the cause, more often as what turned a small problem into a big one. Getting these two settings right is cheap compared with almost any other reliability work.

## How to apply it

- **Set a timeout on every remote call.** Library defaults are often minutes, or infinite. Pick a value from real latency data, e.g. a bit above the p99 (the latency 99% of requests beat).
- **Retry only what's retryable.** Timeouts, connection resets, `503 Service Unavailable`, and `429 Too Many Requests` usually are. `400 Bad Request` almost never is — the same request fails the same way. A `404 Not Found` read just after a write to an eventually consistent store (one where a new write takes a moment to become visible to reads) is the rare exception.
- **Retry only safe operations.** Reads are safe. Writes are safe only if they are idempotent — repeating them has no extra effect ([[idempotency]]).
- **Back off exponentially.** Wait 100ms, then 200ms, then 400ms… so a struggling service gets breathing room.
- **Add jitter.** Jitter is a random amount added to each wait. Without it, a thousand clients that failed together retry together, in synchronized waves.
- **Cap attempts and total time.** One to three retries is typical. Respect a `Retry-After` header when the server sends one.
- **Use a retry budget.** Allow retries only up to a fraction of normal traffic (say 10%). When failures are widespread, retries stop instead of multiplying. The cost: during a wide outage, failures you could have retried reach users — so make sure the error they see is clear.
- **Propagate deadlines.** Pass the remaining time budget down the call chain. Each hop should give up *before* its caller does, so no service keeps working on a request nobody is waiting for.
- **Retry at as few layers as possible.** Ideally that's one service layer — usually the one closest to the user that can still reuse an **idempotency key** (a unique ID sent with every attempt of the same action, so the server can spot repeats) — plus the user, whom you can't stop. Every other layer fails fast. If the browser, the gateway, and three services each retry three times (four attempts each), one failure becomes 4⁵ = 1,024 attempts on the bottom service.

## Example

A checkout service calls a payment service, which calls a fraud-check service.

**Before:** checkout has a 2s timeout. Payment gives fraud check 10s and retries three times with no delay, so each request can become four attempts over 40 seconds. Fraud check slows down; checkout gives up after 2s and the user clicks "Pay" again, starting a second chain. Fraud check's load roughly quadruples — more as users keep clicking — and it falls over.

**After:** checkout sets a 2s deadline and passes it along. Checkout is the one service layer that retries: once, with jittered backoff, only if time remains *and* its 10% retry budget allows. Payment and fraud check fail fast. Load on fraud check during the slowdown rises by at most 10% instead of 300% or more.

The user's second click is still a retry — you can't remove that layer. Checkout sends the same idempotency key for both attempts, so the payment service recognizes the duplicate and can't charge twice.

## Common traps

- **Leaving calls with no timeout.** The most common mistake, and the most expensive.
- **Letting callers give up before callees.** If the upstream timeout is shorter than the downstream one, downstream keeps doing work nobody will use — and the caller's retry adds more.
- **Retrying non-idempotent writes.** This is how customers get charged twice.
- **Using fixed, synchronized retry intervals.** Every client hits the server at the same instant.
- **Letting retries hide a real problem.** Track retry rates; a rising rate is an early warning.

## When it doesn't apply

Inside one process, there's nothing to time out or retry. For long-running background work, a durable queue with redelivery is usually better than in-process retries. And when a dependency is clearly down, stop retrying altogether — that's the job of a [[circuit-breaker]].

## Related

- [[circuit-breaker]] — stops retries entirely when a dependency is clearly unhealthy.
- [[backpressure]] — what a server does when work arrives faster than it can cope; clients respond with the backoff described here.
- [[idempotency]] — the property that makes retrying a write safe.
- [[observability]] — retry and timeout rates are early warning signals.
