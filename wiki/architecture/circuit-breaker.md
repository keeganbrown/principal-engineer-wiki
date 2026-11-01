---
title: Circuit Breaker
category: architecture
summary: Stop calling a dependency that keeps failing, fail fast instead, and test it again after a pause — so one broken service doesn't drag down everything that depends on it.
tags: [resilience, distributed-systems, reliability]
---

# Circuit Breaker

> **In one sentence:** Stop calling a dependency that keeps failing, fail fast instead, and test it again after a pause — so one broken service doesn't drag down everything that depends on it.

## The idea

When a downstream service is slow or down, callers keep sending requests, each waiting for a timeout. Threads and connections pile up, the caller runs out of resources, and now *it* is down too. Failures cascade across the system.

A circuit breaker works like the electrical one in your house. It wraps calls to a dependency and has three states:

```
 CLOSED ──(too many failures)──► OPEN ──(cooldown ends)──► HALF-OPEN
   ▲                              ▲                            │
   │                              └───(trial call fails)───────┤
   └──────────────────(trial call succeeds)────────────────────┘
```

- **Closed** — normal. Calls go through; failures are counted.
- **Open** — the dependency is considered broken. Calls fail **immediately** without trying.
- **Half-open** — after a cooldown, a few trial calls are let through. Success closes the circuit; failure reopens it.

Michael Nygard popularized the pattern in *Release It!* (2007).

## Why it matters

- **Prevents cascading failures.** Callers stop wasting threads and connections on a dead dependency.
- **Gives the dependency room to recover** instead of being hammered by retries.
- **Faster user experience.** An instant fallback beats a 30-second timeout.
- **Clear signal.** A breaker opening is a precise, actionable alert.

## How to apply it

- **Use breakers where they pay off:** on calls with a meaningful fallback, or where hung calls threaten the caller's thread or connection pools. Elsewhere — for example, your primary database with no fallback — a good timeout and a bounded retry are often enough ([[retries-and-timeouts]]); a breaker there just turns slow errors into fast ones.
- **Always pair breakers with timeouts.** A call without a timeout can hang forever and never count as a failure.
- **Decide on a fallback** for each call: cached data, a default value, a degraded feature, or a clear error.
- **Tune thresholds from real traffic.** For example: open after 50% failures over at least 20 calls in 10 seconds; try again after 30 seconds.
- **Use one breaker per dependency** (or per endpoint), so one bad API doesn't block healthy ones.
- **Emit metrics on state changes** and dashboard them ([[observability]]).
- **Use a well-tested library** (resilience4j, Polly) or your **service mesh** — infrastructure that manages calls between services for you — rather than writing your own.

## Example

A product page calls a recommendations service. One day the recommendations service starts timing out after 5 seconds. Without a breaker, every product page takes 5+ seconds and web servers run out of threads — the whole site goes down.

With a breaker: after a burst of failures, the breaker opens. Product pages instantly render with a generic "Popular items" list instead. The site stays up and an alert fires. When recommendations recovers, the half-open trial calls succeed and personalized results return automatically.

## Common traps

- **No fallback.** An open breaker that just throws an error everywhere only moves the failure.
- **Retries without backoff** inside the breaker, multiplying load on a struggling service.
- **Counting the wrong errors.** A `404 Not Found` or validation error isn't a sign the service is unhealthy; don't let it trip the breaker.
- **Thresholds set once and forgotten.** Traffic patterns change; revisit settings.
- **Never exercised.** Breaker code paths only run during incidents, so they're often broken when finally needed. Test open and half-open behavior with fault injection or game days (planned failure drills).

## When it doesn't apply

In-process function calls don't need breakers. For background jobs where waiting is fine, a queue with retries and backoff may be simpler. When a call is absolutely required (e.g., charging a payment with no fallback), a breaker still helps — but the right response is a clear, fast failure to the user, not a fake success.

## Related

- [[retries-and-timeouts]] — the first line of defense; breakers take over when retrying is pointless.
- [[backpressure]] — the mirror image: protecting a service from overload by its callers.
- [[observability]] — monitor breaker state as a key health signal.
- [[event-driven-architecture]] — an alternative that removes the synchronous dependency entirely.
- [[idempotency]] — needed so that retries after recovery are safe.
