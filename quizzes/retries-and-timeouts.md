# Quiz: Retries and Timeouts

## Checkout times out after 2 seconds, but payment gives fraud check 10 seconds. What's wrong?

- [x] Fraud check keeps working long after checkout gave up.
- [ ] Nothing; inner services need the longer timeout to finish their work.
- [ ] Checkout should have no timeout so that it waits for payment.
- [ ] Fraud check should retry more times so that it finishes sooner.

**Why:** Work on abandoned requests is wasted load. Propagate deadlines so each hop gives up before its caller does. See [[retries-and-timeouts]].

## Why add jitter to retry backoff?

- [x] So clients that failed together don't all retry at the same moment.
- [ ] So each retry waits a fixed, predictable interval that's easy to tune.
- [ ] So the server can tell retries apart from brand-new requests.
- [ ] So retries happen faster on average than with plain backoff.

**Why:** Fixed, synchronized intervals create retry storms. Randomizing the wait spreads load out. See [[retries-and-timeouts]].

## Three layers of services each retry three times. Why is that dangerous?

- [x] Retries multiply: one request becomes dozens of calls at the bottom.
- [ ] Retries at multiple layers cancel each other out and hide failures.
- [ ] Each layer's retries make the other layers time out instantly.
- [ ] Backoff delays add up until every request misses its deadline.

**Why:** Each layer makes four attempts, so 4 × 4 × 4 = 64 calls can hit the deepest service. Retry at as few layers as possible. See [[retries-and-timeouts]].

## During a wide outage, a service's 10% retry budget runs out. What follows?

- [x] Retryable failures reach users, so their error must be clear.
- [ ] The budget resets every second, so users never notice a thing.
- [ ] Clients switch to unlimited retries until the outage is over.
- [ ] The service stops accepting new requests until the budget refills.

**Why:** A retry budget stops retries from multiplying load when failures are widespread. The price is that some failures you could have retried reach users. See [[retries-and-timeouts]].
