# Quiz: Idempotency

## A payment request succeeds, but the response times out and the app retries. What prevents a double charge?

- [x] One idempotency key per checkout, reused on every retry.
- [ ] A new idempotency key generated for each retry attempt.
- [ ] A trace ID attached to each HTTP request the app sends.
- [ ] A shorter timeout on the mobile client so it gives up sooner.

**Why:** The server sees the same key and returns the stored result. A new key per retry defeats the purpose. See [[idempotency]].

## Which of these operations is naturally idempotent?

- [x] Setting a shipping address to a given value.
- [ ] Adding $10 to an account balance.
- [ ] Appending one line to the audit log.
- [ ] Sending a fresh "verify your email" code.

**Why:** Doing it twice leaves the same result as doing it once. Idempotent isn't order-safe, though: a late retry can overwrite a newer value, so pair concurrent writes with a version check. See [[idempotency]].

## A request arrives with a known idempotency key but a different body. What should the server do?

- [x] Reject it; a key must never be reused for a new request.
- [ ] Process it as a new request and overwrite the stored result for that key.
- [ ] Return the stored response from the first request, without comment.
- [ ] Generate a new key on the server and process the request with that.

**Why:** A reused key with a different payload is a client bug, and `422` says so. Storing a hash of the request lets the server detect it. See [[idempotency]].

## A user clicks "send another verification code" twice in a minute. Should the server deduplicate the second request with an idempotency key?

- [x] No; the action is meant to repeat, though you might rate-limit it.
- [ ] Yes; every request that sends a message must carry an idempotency key.
- [ ] Yes, and keep the key for 24 hours so no second code is ever sent.
- [ ] No; idempotency only matters for requests that move money.

**Why:** Operations that are meant to repeat shouldn't be deduplicated. Rate-limiting stops abuse without blocking a real second request. See [[idempotency]].
