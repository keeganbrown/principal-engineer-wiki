# Quiz: Circuit Breaker

## A recommendations service starts timing out. What does an open breaker let the product page do?

- [x] Fail fast and show a generic "Popular items" list instead.
- [ ] Wait the full timeout on every call, then show an error page.
- [ ] Retry the call three times in a row before giving up.
- [ ] Queue the requests until the recommendations service recovers.

**Why:** The breaker stops calls to a failing dependency, so threads aren't tied up and the page renders with a fallback. See [[circuit-breaker]].

## What happens in the half-open state?

- [x] A few trial calls go through; success closes the breaker, failure opens it again.
- [ ] All calls go through, but their errors are ignored.
- [ ] No calls go through until an engineer resets the breaker.
- [ ] Calls go through to a backup copy of the dependency.

**Why:** Half-open tests whether the dependency has recovered, so normal service returns automatically. See [[circuit-breaker]].

## A payment call has no sensible fallback. When is a breaker still worth it?

- [x] When hung calls threaten the caller's thread or connection pools; then fail fast and clearly.
- [ ] Never; breakers are only useful when there's a fallback to show.
- [ ] Always, and the breaker should return a fake success to the user.
- [ ] Only for in-process function calls in the same service.

**Why:** Without a fallback, the right response is a clear, fast failure — never a fake success. The breaker protects the caller's resources. See [[circuit-breaker]].
