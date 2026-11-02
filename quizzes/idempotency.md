# Quiz: Idempotency

## A payment request succeeds, but the response times out and the app retries. What prevents a double charge?

- [x] An idempotency key generated once per checkout attempt and reused on every retry.
- [ ] A new idempotency key generated for each retry.
- [ ] A trace ID attached to each HTTP request.
- [ ] A shorter timeout on the mobile client.

**Why:** The server sees the same key and returns the stored result. A new key per retry defeats the purpose. See [[idempotency]].

## Which of these operations is naturally idempotent?

- [x] Setting a shipping address to a given value.
- [ ] Adding $10 to an account balance.
- [ ] Appending a line to an audit log.
- [ ] Sending a "verify your email" code.

**Why:** Doing it twice leaves the same result as doing it once. Prefer naturally idempotent operations where you can. See [[idempotency]].

## A request arrives with a known key but a different body. What should the server do?

- [x] Reject it, for example with `422`, because the same key was used for a different request.
- [ ] Process it as a new request and overwrite the stored result.
- [ ] Return the stored response from the first request silently.
- [ ] Generate a new key on the server and process it.

**Why:** Same key, different payload is a listed trap. Storing a hash of the request lets the server detect it. See [[idempotency]].
