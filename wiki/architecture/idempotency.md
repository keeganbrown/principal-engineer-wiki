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

The only safe move is to **retry** — and retrying is only safe if the operation is idempotent. Similarly, most message queues deliver messages *at least once*, so consumers will see duplicates.

## Why it matters

Without idempotency, normal network hiccups cause real damage: customers charged twice, duplicate orders, emails sent three times, inventory counted wrong. These bugs are rare, hard to reproduce, and expensive — exactly the kind that erode trust.

## How to apply it

- **Prefer naturally idempotent operations.** "Set status to SHIPPED" is idempotent; "toggle status" is not. "Set balance to 50" is idempotent; "add 10" is not.
- **Use idempotency keys** for operations that aren't naturally idempotent. The client generates a unique ID per *intended* action and sends it with every retry. The server stores the key with the result; if it sees the key again, it returns the stored result instead of redoing the work.
- **Deduplicate messages** in consumers by tracking processed message IDs.
- **Use database constraints** (unique indexes) as a last line of defense against duplicates.
- **Make the check and the work atomic** — store the key in the same transaction as the effect, or two concurrent retries can both slip through.
- Know your HTTP semantics: `GET`, `PUT`, and `DELETE` are meant to be idempotent; `POST` is not, unless you add a key.

## Example

A mobile app calls `POST /payments` to charge $50. The request succeeds but the response times out on a flaky connection, so the app retries.

**Without a key:** the customer is charged $100.

**With a key:**

```
POST /payments
Idempotency-Key: 7f3c9a2e-...      # generated once per checkout attempt
{ "amount": 50, "customer": "c_123" }

server:
  if key exists in payments_requests: return the saved response
  else, in one transaction:
       charge card; save (key, response)
       return response
```

The retry returns the original success response. One charge, happy customer. Payment APIs such as Stripe use exactly this approach.

## Common traps

- **Generating a new key on each retry.** The key must identify the *intent*, so it's created once and reused.
- **Keys with no expiry.** Store them long enough to cover realistic retries (often 24 hours or more), then clean them up.
- **Same key, different payload.** If a client reuses a key with a different request body, reject it rather than silently returning the old result.
- **Side effects outside the transaction**, like sending an email before recording the key.

## When it doesn't apply

Pure reads are already idempotent. Operations that are inherently "do it again" — like "send another verification code" — are meant to repeat, though you might still rate-limit them. In a single process with no retries or queues, you rarely need explicit idempotency machinery.

## Related

- [[event-driven-architecture]] — at-least-once delivery makes idempotent consumers essential.
- [[circuit-breaker]] — retries after recovery must be safe.
- [[cqrs]] — read model projectors must handle replayed events.
- [[observability]] — request and idempotency IDs double as tracing aids.
