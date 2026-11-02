# Quiz: Retries and Timeouts

## Checkout times out after 2 seconds, but it gives payment 10 seconds to call fraud check. What's wrong?

- [x] Callees keep working long after the caller gave up, wasting load on abandoned requests.
- [ ] Nothing; inner services should always have the longer timeout.
- [ ] Checkout should have no timeout so it waits for payment.
- [ ] Fraud check should retry more times to finish faster.

**Why:** Propagate deadlines so downstream work stops when the caller stops waiting. See [[retries-and-timeouts]].

## Why add jitter to retry backoff?

- [x] So clients that failed together don't all retry at the same moment.
- [ ] So each retry waits a fixed, predictable interval.
- [ ] So the server can tell retries from new requests.
- [ ] So retries happen faster on average.

**Why:** Fixed, synchronized intervals create retry storms. Randomizing the wait spreads load out. See [[retries-and-timeouts]].

## Three layers each retry three times. Why is that dangerous?

- [x] Retries multiply: one user request can become dozens of calls on the deepest service.
- [ ] Retries at multiple layers cancel each other out.
- [ ] Each layer's retries make the others time out instantly.
- [ ] It's safe as long as every layer uses backoff.

**Why:** Retry at as few layers as possible, and use a retry budget. In the example, one layer retries and the rest fail fast. See [[retries-and-timeouts]].
