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

- **It stops cascading failures.** Callers stop wasting threads and connections on a dead dependency.
- **The dependency gets room to recover.** It isn't hammered by retries.
- **Users get a faster answer.** An instant fallback beats a 30-second timeout.
- **State changes are a precise health signal.** A breaker opening tells you exactly which dependency is failing ([[observability]]).

## How to apply it

- **Use breakers where they pay off.** That means calls with a meaningful fallback, or calls whose hangs threaten the caller's thread or connection pools. Elsewhere, a timeout and a bounded retry are often enough ([[retries-and-timeouts]]). A database call with a tight timeout and no fallback is the typical case: the timeout already makes its errors fast, so a breaker adds code and tuning but changes little.
- **Always pair breakers with timeouts.** A call without a timeout can hang forever and never count as a failure.
- **Decide on a fallback for each call.** Options are [[caching|cached data]], a default value, a degraded feature, or a clear error.
- **Tune thresholds from real traffic.** For example: open after 50% failures over at least 20 calls in 10 seconds; try again after 30 seconds. Breakers usually live in each instance, so check the minimum call count against per-instance traffic, not the fleet's total.
- **Use one breaker per dependency or endpoint.** One bad API shouldn't block healthy ones.
- **Emit metrics on state changes.** Show them on a dashboard, and page someone only if the fallback hurts something users notice.
- **Don't write your own.** Use a well-tested library (for example resilience4j for Java, Polly for .NET) or a **service mesh** — infrastructure that manages calls between services for you. A mesh can fail fast, but it can't choose a fallback; that part stays in your code.

## Example

A product page calls a recommendations service. One day the recommendations service starts timing out after 5 seconds. Without a breaker, every product page takes 5+ seconds and web servers run out of threads — the whole site goes down.

With a breaker: after a burst of failures, the breaker opens. Product pages instantly render with a generic "Popular items" list instead. The site stays up; the breaker's state change shows on the dashboard, and nobody is paged because users still see a working page. When recommendations recovers, the half-open trial calls succeed and personalized results return automatically.

## Common traps

- **No decided fallback.** An open breaker that throws an unplanned error everywhere only moves the failure; a deliberate, clear, fast error *is* a fallback.
- **Retrying inside the breaker without backoff.** It multiplies load on a struggling service ([[retries-and-timeouts]]).
- **Counting the wrong errors.** A `404 Not Found` or validation error isn't a sign the service is unhealthy; don't let it trip the breaker.
- **Thresholds set once and forgotten.** Traffic patterns change; revisit settings.
- **Never exercised.** Breaker code paths only run during incidents, so they're often broken when finally needed. Test open and half-open behavior with fault injection (deliberately making a dependency fail or slow down) or game days (planned failure drills).

## When it doesn't apply

In-process function calls don't need breakers. For background jobs where waiting is fine, a queue with retries and backoff may be simpler. When a call has no fallback, a breaker earns its place only if hung calls threaten the caller's pools — payment calls often qualify. Then the right response is a clear, fast failure to the user, not a fake success.

## Related

- [[retries-and-timeouts]] — the first line of defense; breakers take over when retrying is pointless.
- [[backpressure]] — the mirror image: protecting a service from overload by its callers.
- [[observability]] — monitor breaker state as a key health signal.
- [[event-driven-architecture]] — an alternative that removes the synchronous dependency entirely.
- [[idempotency]] — needed so that retries after recovery are safe.
