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

In an event-driven system, A simply *announces what happened*: `OrderPlaced { orderId: 42 }`. It publishes this **event** to a broker (Kafka, RabbitMQ, SNS/SQS, etc.). Any interested service — email, shipping, analytics — **subscribes** and reacts. A doesn't know or care who's listening.

```
Orders ──publish──► [ OrderPlaced ] ──► Email
                         │         └──► Shipping
                         └────────────► Analytics
```

Events are named in the **past tense**, because they're facts that already happened.

## Why it matters

- **Loose coupling.** Add a new consumer (say, fraud detection) without changing the producer.
- **Resilience.** If Shipping is down, events wait in the queue. Orders keeps working.
- **Scalability.** Consumers process at their own pace; bursts are absorbed by the queue.
- **Audit trail.** A stream of events is a natural history of what happened.

## How to apply it

- **Publish facts, not commands.** `OrderPlaced`, not `SendConfirmationEmail`. Commands re-create the coupling.
- **Design events as public contracts.** Version them, document them, and evolve them compatibly (add fields; don't remove or rename).
- **Make consumers idempotent.** Most brokers deliver *at least once*, so the same event may arrive twice.
- **Use a dead-letter queue** for events that repeatedly fail, and alert on it.
- **Use the outbox pattern** to avoid "saved to DB but failed to publish": write the event to an outbox table in the same transaction, then relay it to the broker.
- **Propagate correlation IDs** in event metadata so you can trace a flow across services.

## Example

Checkout used to call five services synchronously; if any was slow, checkout was slow. Now `Orders` saves the order, writes `OrderPlaced` to its outbox, and returns immediately. Email, Shipping, Loyalty, and Analytics each consume the event independently. When Loyalty has an outage, its events pile up and are processed when it recovers — customers never notice.

## Common traps

- **Assuming instant consistency.** After placing an order, the "My Shipments" page might not show it for a few seconds. Design the UX for this.
- **Event spaghetti.** Long chains of events triggering events become impossible to follow. Document flows and keep chains short.
- **Fat events vs. thin events.** Events with only an ID force consumers to call back (re-coupling). Events with everything leak internals. Include what consumers commonly need.
- **Ignoring ordering.** Events can arrive out of order; design for it or use partitioning keys.
- **No observability.** Without tracing, debugging async flows is guesswork.

## When it doesn't apply

When the caller needs an immediate answer — "is this card valid?" — a synchronous call is simpler and correct. Small systems with one team often don't need a broker at all. Event-driven designs add operational weight; adopt them when decoupling or resilience is worth it.

## Related

- [[idempotency]] — essential for safely handling duplicate events.
- [[cqrs]] — often paired with events to update read models.
- [[observability]] — tracing is critical for async flows.
- [[coupling-and-cohesion]] — events trade runtime coupling for contract coupling.
- [[circuit-breaker]] — the complementary tool when calls must stay synchronous.
- [[cap-theorem]] — why choosing events usually means choosing eventual consistency.
- [[saga-pattern]] — coordinating multi-step workflows over events.
- [[backpressure]] — what to do when consumers can't keep up.
- [[api-versioning]] — event schemas are APIs and need the same care.
