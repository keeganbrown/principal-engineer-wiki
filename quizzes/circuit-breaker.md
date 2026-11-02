# Quiz: Circuit Breaker

## A recommendations service starts timing out. What does an open breaker let the product page do?

- [x] Fail fast and show a generic "Popular items" list instead.
- [ ] Wait the full timeout on every call, then show an error page.
- [ ] Retry the call three times in a row before giving up on it.
- [ ] Queue the requests until the recommendations service recovers.

**Why:** The breaker stops calls to a failing dependency, so threads aren't tied up and the page renders with a fallback. See [[circuit-breaker]].

## A database call has a tight timeout, no fallback, and can't exhaust the caller's pools. Does it need a breaker?

- [x] Usually not; a timeout and a bounded retry are enough.
- [ ] Yes; every remote call should have a breaker for consistency.
- [ ] Yes, with a cached fake result returned whenever it opens.
- [ ] Only once the database has had its first serious outage.

**Why:** Use breakers where they pay off: a meaningful fallback, or hangs that threaten the caller's resources. Elsewhere a breaker just turns slow errors into fast ones. See [[circuit-breaker]] and [[retries-and-timeouts]].

## A payment call has no sensible fallback. When is a breaker still worth it?

- [x] When hung calls could exhaust the caller's threads or connections.
- [ ] Only when a cached response can stand in for the real payment result.
- [ ] When it can return a fake success, so checkout still completes.
- [ ] Only for in-process function calls made within the same service.

**Why:** Without a fallback, the right response is a clear, fast failure, never a fake success. The breaker protects the caller's resources. See [[circuit-breaker]].

## What happens in a circuit breaker's half-open state?

- [x] A few trial calls go through; success closes it, failure reopens it.
- [ ] All calls go through as normal, but any errors they return are ignored.
- [ ] No calls go through until an engineer resets the breaker by hand.
- [ ] Calls go through to a backup copy of the failing dependency instead.

**Why:** Half-open tests whether the dependency has recovered, so normal service returns automatically. See [[circuit-breaker]].
