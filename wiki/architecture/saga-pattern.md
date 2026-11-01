---
title: Sagas
category: architecture
summary: Run a business process that spans several services as a sequence of local steps, each with an "undo" action, instead of one distributed transaction.
tags: [distributed-systems, transactions, microservices]
---

# Sagas

> **In one sentence:** Run a business process that spans several services as a sequence of local steps, each with an "undo" action, instead of one distributed transaction.

## The idea

Booking a trip means reserving a flight, a hotel, and a car. In a single database, you'd wrap all three in a transaction: either everything succeeds, or nothing does. But when flights, hotels, and cars are separate services with separate databases, there's no shared transaction to lean on. (Distributed transactions like two-phase commit exist, but they're slow, fragile, and poorly supported across modern services.)

A **saga** breaks the process into steps. Each step is a local transaction in one service. If a later step fails, the saga runs **compensating actions** to undo the earlier steps:

```
Reserve flight ✔ → Reserve hotel ✔ → Reserve car ✘
                                          │
          Cancel flight ◄── Cancel hotel ◄┘   (compensate in reverse)
```

What you give up is **isolation**: other processes can see the half-finished state until the saga completes or compensates. You also lose *instant* all-or-nothing — it's restored only eventually, by running compensations. Across services, the end state is eventually consistent ([[cap-theorem]]).

The idea comes from a 1987 paper by Hector Garcia-Molina and Kenneth Salem.

## Why it matters

Without a plan for partial failure, multi-service workflows leave messes: a customer charged for a trip with no hotel, or inventory reserved for an order that was never paid. Sagas make the failure path explicit and designed, rather than an afterthought.

## How to apply it

There are two ways to coordinate a saga:

| Style | How it works | Good for |
| --- | --- | --- |
| **Choreography** | Each service listens for events and reacts (`FlightReserved` → hotel service reserves). | Short sagas with few steps. |
| **Orchestration** | A central orchestrator sends each service a command — a direct request to one service, unlike the broadcast facts of [[event-driven-architecture]] — and tracks state. | Longer sagas, complex logic, easier debugging. |

Guidelines:
- **Design compensations with the business.** "Undo" is often not a true rollback — it's a refund, a cancellation email, a credit.
- **Order steps by how easy they are to undo.** Put cheap, invisible compensations (releasing a reservation) early, and costly or customer-visible ones (a refund) late. Put steps that can't be undone at all — like sending a confirmation email — last. This is [[reversible-decisions|two-way-door]] thinking applied to one workflow.
- **Make every step and compensation idempotent.** Messages get [[retries-and-timeouts|retried]] and duplicated ([[idempotency]]).
- **Persist saga state.** A crash mid-saga should resume, not restart.
- **Mark records as pending.** A status field like `PENDING` acts as a **semantic lock**: other processes see it and avoid acting on the record until the saga finishes.
- **Consider a workflow engine for orchestration.** Temporal or AWS Step Functions usually beat building your own.

## Example

An online store's checkout saga, orchestrated:

1. `Orders`: create the order as `PENDING`.
2. `Inventory`: reserve the items. *Compensation: release them (invisible to the customer).*
3. `Payments`: *authorize* the card — place a hold, without taking money yet. *Compensation: void the hold.*
4. `Payments`: *capture* the payment. *Compensation: refund (slow and visible, so it comes late).*
5. `Orders`: mark the order `CONFIRMED`; send the confirmation email (last, since it can't be undone).

If inventory is out of stock at step 2, nothing has touched the customer's card — the orchestrator just marks the order `CANCELLED` and tells the customer. If authorization fails at step 3, it releases the reservation. Every outcome is planned, logged, and traceable.

## Common traps

- **Assuming isolation.** Unlike a database transaction, other processes can see intermediate states. Design for it.
- **Compensations that can fail.** A failed refund with no retry or alert needs a human escalation path.
- **Choreography sprawl.** With many steps, event chains become impossible to follow. Switch to orchestration.
- **Unordered irreversible steps.** Sending an email or shipping a parcel early means a failed saga can't take it back.

## When it doesn't apply

If the steps live in one database or one service, use an ordinary transaction — it's far simpler. If you find a single business action regularly needs a saga across many services, consider whether the service boundaries are wrong ([[domain-driven-design]]).

## Related

- [[event-driven-architecture]] — choreographed sagas are built on events.
- [[idempotency]] — every saga step and compensation must tolerate retries.
- [[transactional-outbox]] — each step publishes its result reliably.
- [[microservices]] — sagas are a cost of splitting data across services.
- [[observability]] — trace IDs across steps make sagas debuggable.
