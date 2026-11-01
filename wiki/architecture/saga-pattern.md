---
title: Saga Pattern
category: architecture
summary: Run a business process that spans several services as a sequence of local steps, each with an "undo" action, instead of one distributed transaction.
tags: [distributed-systems, transactions, microservices]
---

# Saga Pattern

> **In one sentence:** Run a business process that spans several services as a sequence of local steps, each with an "undo" action, instead of one distributed transaction.

## The idea

Booking a trip means reserving a flight, a hotel, and a car. In a single database, you'd wrap all three in a transaction: either everything succeeds, or nothing does. But when flights, hotels, and cars are separate services with separate databases, there's no shared transaction to lean on. (Distributed transactions like two-phase commit exist, but they're slow, fragile, and poorly supported across modern services.)

A **saga** breaks the process into steps. Each step is a local transaction in one service. If a later step fails, the saga runs **compensating actions** to undo the earlier steps:

```
Reserve flight ✔ → Reserve hotel ✔ → Reserve car ✘
                                          │
          Cancel flight ◄── Cancel hotel ◄┘   (compensate in reverse)
```

The idea dates to a 1987 paper by Hector Garcia-Molina and Kenneth Salem.

## Why it matters

Without a plan for partial failure, multi-service workflows leave messes: a customer charged for a trip with no hotel, or inventory reserved for an order that was never paid. Sagas make the failure path explicit and designed, rather than an afterthought.

## How to apply it

There are two ways to coordinate a saga:

| Style | How it works | Good for |
| --- | --- | --- |
| **Choreography** | Each service listens for events and reacts (`FlightReserved` → hotel service reserves). | Short sagas with few steps. |
| **Orchestration** | A central orchestrator tells each service what to do next and tracks state. | Longer sagas, complex logic, easier debugging. |

Guidelines:
- **Design compensations with the business.** "Undo" is often not a true rollback — a refund, a cancellation email, a credit. Some things can't be undone (an email already sent); order steps so those come last.
- **Make every step and compensation idempotent.** Messages get retried and duplicated.
- **Persist saga state** so a crash mid-saga can resume, not restart.
- **Use semantic locks or pending states** ("reservation: PENDING") so other processes know the data is mid-flight.
- **Consider a workflow engine** (e.g., Temporal, AWS Step Functions) for orchestration instead of building your own.

## Example

An online store's checkout saga, orchestrated:

1. `Orders`: create order as `PENDING`.
2. `Payments`: charge card. *Compensation: refund.*
3. `Inventory`: reserve items. *Compensation: release items.*
4. `Orders`: mark order `CONFIRMED`; send confirmation email (last, since it can't be undone).

If inventory fails at step 3 (out of stock), the orchestrator refunds the payment and marks the order `CANCELLED`, then tells the customer. Every outcome is planned, logged, and traceable.

## Common traps

- **Assuming isolation.** Unlike a database transaction, other processes can see intermediate states. Design for it.
- **Compensations that can fail** with no retry or alert. A failed refund needs a human escalation path.
- **Choreography sprawl.** With many steps, event chains become impossible to follow. Switch to orchestration.
- **Using sagas when one service would do.** If all the data could live in one database, a plain transaction is far simpler.

## When it doesn't apply

If the steps live in one database or one service, use an ordinary transaction. If you're drawing service boundaries so that a single business action regularly needs a saga across many services, consider whether the boundaries are wrong.

## Related

- [[event-driven-architecture]] — choreographed sagas are built on events.
- [[idempotency]] — every saga step and compensation must tolerate retries.
- [[cap-theorem]] — sagas accept eventual consistency in exchange for availability.
- [[domain-driven-design]] — good bounded contexts reduce how many sagas you need.
- [[observability]] — trace IDs across steps make sagas debuggable.
