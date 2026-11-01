---
title: Event-Driven Architecture
category: architecture
summary: Components announce facts ("an order was placed") and others react on their own schedule, which decouples services at the cost of eventual consistency and harder debugging.
tags: [architecture, distributed-systems, messaging]
---

# Event-Driven Architecture

> **In one sentence:** Components announce facts ("an order was placed") and others react on their own schedule, which decouples services at the cost of eventual consistency and harder debugging.

## The idea

In a request-driven system, service A *tells* service B what to do: "send this email." A must know B exists, and if B is down, A fails.

In an event-driven system, A *announces what happened*: `OrderPlaced { orderId: 42 }`. It publishes this **event** to a **broker** — messaging software such as Kafka, RabbitMQ, or Amazon SNS/SQS. Any interested service — email, shipping, analytics — **subscribes** and reacts. A doesn't know or care who's listening.

```
Orders ──publish──► [ OrderPlaced ] ──► Email
                         │         └──► Shipping
                         └────────────► Analytics
```

Events are named in the **past tense**, because they're facts that already happened.

## Why it matters

- **Looser runtime coupling.** Add a new consumer (say, fraud detection) without changing the producer. The coupling doesn't vanish, though: it moves into the event schema and into flows nobody can see in one place. The producer can no longer tell who will break when it changes.
- **Resilience.** If Shipping is down, events wait in the queue. Orders keeps working.
- **Smoothing bursts.** Consumers process at their own pace; short bursts are absorbed by the queue — as long as it's bounded and consumers can catch up ([[backpressure]]).
- **Audit trail.** A stream of events is a natural history of what happened.

The price is **eventual consistency**: consumers' views lag behind the producer by a moment ([[cap-theorem]] covers the consistency models).

## How to apply it

- **Publish facts for broadcast, not disguised commands.** `OrderPlaced`, not `SendConfirmationEmail`. A "command" dressed as an event re-creates the coupling you were avoiding. Commands are fine when one component deliberately owns a workflow — that's an [[saga-pattern|orchestrated saga]].
- **Design events as public contracts.** Version them, document them, and evolve them compatibly ([[api-versioning]]).
- **Make consumers idempotent.** Most brokers deliver *at least once*, so the same event may arrive twice ([[idempotency]]).
- **Use a dead-letter queue** — a holding queue for events that keep failing — and alert on it.
- **Publish reliably with an outbox.** Saving to the database and publishing to the broker are two separate writes. Write the event to an outbox table in the same transaction, and let a separate process relay it ([[transactional-outbox]]).
- **Propagate trace IDs** in event metadata, so you can follow a flow across services ([[observability]]).

## Example

Checkout used to call five services synchronously; if any was slow, checkout was slow. Now `Orders` saves the order, writes `OrderPlaced` to its outbox, and returns immediately. Email, Shipping, Loyalty, and Analytics each consume the event independently. When Loyalty has an outage, its events pile up and are processed when it recovers — customers never notice.

The trade-off: right after checkout, the "My Shipments" page may not show the new order for a few seconds. The team shows "Processing…" instead of an empty list.

## Common traps

- **Assuming instant consistency.** Design the UX for a short lag.
- **Event spaghetti.** Long chains of events triggering events become impossible to follow. Document flows and keep chains short.
- **Getting event size wrong.** Events with only an ID force every consumer to call back for details (re-coupling them). Events carrying everything leak internals. Include what consumers commonly need.
- **Ignoring ordering.** Events can arrive out of order. Design for it, or use a **partitioning key** (e.g., `orderId`) so all events for one order go through the same ordered stream.
- **No observability.** Without tracing, debugging async flows is guesswork.

## When it doesn't apply

When the caller needs an immediate answer — "is this card valid?" — a synchronous call is simpler and correct. Small systems with one team often don't need a broker at all. Event-driven designs add operational weight; adopt them when decoupling or resilience is worth it.

## Related

- [[transactional-outbox]] — how to publish events without losing or inventing them.
- [[idempotency]] — essential for safely handling duplicate events.
- [[saga-pattern]] — coordinating multi-step workflows over events.
- [[cqrs]] — events often keep read models up to date.
- [[backpressure]] — what to do when consumers can't keep up.
- [[cap-theorem]] — why choosing async events means choosing eventual consistency.
- [[circuit-breaker]] — the complementary tool when calls must stay synchronous.
