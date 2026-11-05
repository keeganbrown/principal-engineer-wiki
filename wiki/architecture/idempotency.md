---
title: Idempotency
category: architecture
summary: Design operations so doing them twice has the same effect as doing them once, which makes retries and duplicate messages safe in an unreliable network.
tags: [distributed-systems, reliability, api-design]
---

# Idempotency

> **In one sentence:** Design operations so doing them twice has the same effect as doing them once, which makes retries and duplicate messages safe in an unreliable network.

## The idea

An operation is **idempotent** if repeating it doesn't change the result beyond the first time. Pressing an elevator's call button five times is idempotent — the elevator still comes once. Adding $10 to an account balance is not — do it twice and you've added $20.

This matters because networks are unreliable. When a client sends a request and the response never arrives, it can't tell whether:

- the request never reached the server, or
- the server did the work but the response was lost.

The usual move is to retry (or to check the operation's status first) — and retrying is only safe if the operation is idempotent. Similarly, most message queues deliver messages *at least once*, so consumers will see duplicates.

## Why it matters

Without idempotency, normal network hiccups cause real damage: customers charged twice, duplicate orders, emails sent three times, inventory counted wrong. These bugs are rare, hard to reproduce, and expensive — exactly the kind that erode trust.

## How to apply it

- **Prefer naturally idempotent operations.** "Set status to SHIPPED" is idempotent; "toggle status" is not. "Set balance to 50" is idempotent; "add 10" is not. Idempotent isn't order-safe, though: a delayed retry of "set address to A" that lands after "set address to B" overwrites B, so pair concurrent writes with a version check.
- **Use idempotency keys for operations that aren't naturally idempotent.** The client generates a unique ID per *intended action* and sends it with every retry. The server remembers each key and its result; if it sees the key again, it returns the stored result instead of redoing the work.
- **Claim the key before doing the work.** Insert the key with status `IN_PROGRESS` under a unique index *first*. A concurrent duplicate fails that insert and backs off.
- **Pass idempotency downstream.** Most real effects — charging a card, sending an email — happen in *other* systems, outside your database transaction. You can't make them succeed or fail together with your write. Instead, pass your key to the downstream service as *its* idempotency key, so a repeated call has no extra effect there either.
- **Choose a fallback when downstream takes no key.** Many email and legacy systems don't accept one. Either query the status by your own reference before retrying, or don't retry at all (*at-most-once*: the effect may be lost, never doubled). Either way, run a periodic check that finds and repairs misses, and choose by which hurts more: a duplicate or a miss.
- **Deduplicate messages in consumers.** Record each processed message ID in the same transaction as the effect it guards; recorded separately, a crash between the two loses or repeats the effect. Keep IDs at least as long as the broker can redeliver a message.
- **Use database constraints as a last line of defense.** Unique indexes catch duplicates everything else missed.
- **Know your HTTP semantics.** `GET`, `PUT`, and `DELETE` are meant to be idempotent; `POST` is not, unless you add a key.

## Example

A mobile app calls `POST /payments` to charge $50. The request succeeds but the response times out on a flaky connection, so the app retries.

**Without a key:** the customer is charged $100.

**With a key:**

```
POST /payments
Idempotency-Key: 7f3c9a2e-...      # generated once per checkout attempt
{ "amount": 50, "customer": "c_123" }

server:
    existing = requests.find(key)
    if existing and existing.requestHash != hash(body): return 422   # same key, different request
    if existing and existing.status == DONE: return existing.response
    if existing: return 409 Conflict                                 # still in progress; retry later

    if not requests.tryInsert(key, status=IN_PROGRESS,
                              request=body, requestHash=hash(body)):
        return 409 Conflict                                          # lost the race to a duplicate
    response = paymentProvider.charge(body.amount, body.customer, idempotencyKey=key)
    requests.update(key, status=DONE, response=response)
    return response
```

The hard case is a crash *after* the provider charges the card but *before* the result is saved. The key is stuck in `IN_PROGRESS`. Because the same key was passed to the provider, retrying the charge is safe: the provider recognizes the key and returns the original result instead of charging again.

A background sweeper finds keys stuck in progress for more than a few minutes — after a crash *or* a provider timeout — and re-runs the *stored* request with the same key. It must finish well inside the provider's key-retention window (Stripe keeps keys for about 24 hours). Past that window, it looks the charge up by your own order reference instead of re-sending, and alerts a person about any key that old.

Stripe's API works this way: it accepts an `Idempotency-Key` header on requests that create or change things.

## Common traps

- **Generating a new key on each retry.** The key must identify the *intent*, so it's created once and reused.
- **Assuming one transaction covers everything.** It only covers your own database. External calls need downstream idempotency or an [[transactional-outbox|outbox]].
- **Keys with no expiry.** Store them long enough to cover realistic retries (often 24 hours or more), then clean them up.
- **Same key, different payload.** If a client reuses a key with a different request body, reject it rather than silently returning the old result.
- **Confusing keys with trace IDs.** A trace ID (also called a correlation ID) follows one *request*; an idempotency key follows one *intended action* across many requests. Log both.

## When it doesn't apply

Pure reads are already idempotent. Operations that are meant to repeat — like "send another verification code" — shouldn't be deduplicated, though you might still rate-limit them. In a single process with no retries or queues, you rarely need explicit idempotency machinery.

## Related

- [[retries-and-timeouts]] — idempotency is what makes retrying a write safe.
- [[event-driven-architecture]] — at-least-once delivery makes idempotent consumers essential.
- [[transactional-outbox]] — the outbox relay can publish duplicates; consumers must cope.
- [[saga-pattern]] — every saga step and compensation must be idempotent.
- [[observability]] — log the idempotency key alongside the trace ID.
- [[message-brokers]] — why most brokers deliver at least once.
