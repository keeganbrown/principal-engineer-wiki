---
title: Hexagonal Architecture (Ports and Adapters)
category: architecture
summary: Put your business logic at the center and connect it to databases, APIs, and UIs only through interfaces it defines, so the outside world can be swapped — in tests especially — without touching the core.
tags: [architecture, design, testing]
---

# Hexagonal Architecture (Ports and Adapters)

> **In one sentence:** Put your business logic at the center and connect it to databases, APIs, and UIs only through interfaces it defines, so the outside world can be swapped — in tests especially — without touching the core.

## The idea

Picture your application as a hexagon (the number of sides doesn't matter):

```
        [ Web UI ]      [ CLI ]      [ Tests ]
             \            |            /
          ┌──── driving adapters ─────┐
          │   ports (interfaces in)   │
          │                           │
          │      APPLICATION CORE     │
          │   (domain + use cases)    │
          │                           │
          │  ports (interfaces out)   │
          └──── driven adapters ──────┘
             /            |            \
     [ Postgres ]   [ Stripe API ]   [ Email ]
```

- **Core** — business rules and use cases. It knows nothing about HTTP, SQL, or vendors. The use cases are a thin layer that calls ports (below); the domain rules they call can be a pure [[functional-core-imperative-shell|functional core]] — no I/O, and the same input always gives the same output.
- **Ports** — interfaces the core defines, in its own language: "I need a way to save orders" (`OrderRepository`), "I need to charge cards" (`PaymentGateway`).
- **Driving adapters** — call *into* the core: a web controller, a command-line interface (CLI), a test.
- **Driven adapters** — are called *by* the core: `PostgresOrderRepository`, `StripeGateway`, or an `InMemoryOrderRepository` fake for tests.

Dependencies always point **inward**. That can seem impossible — how does the core save to Postgres without depending on it?

The core calls `OrderRepository`, an interface it *owns*, and `PostgresOrderRepository` implements it. At runtime the call goes outward, but in the code the adapter depends on the core, not the reverse. This is **dependency inversion**: high-level code owns the interface, and low-level code implements it.

Alistair Cockburn proposed the pattern in 2005. *Clean Architecture* and *Onion Architecture* are close relatives.

## Why it matters

- **Use cases are easy to test.** Run every one against in-memory fakes — fast, deterministic tests with no infrastructure. This is the dependable win.
- **Business rules are easy to find.** It's always obvious where they live.
- **Logic outlives frameworks.** Frameworks come and go; your business logic doesn't need to go with them.
- **Adapters can be swapped, partly.** You *can* switch providers by writing a new adapter, but a port designed around one vendor rarely fits the second without reshaping, and database transaction behavior leaks through repository ports. Don't justify a port by a swap you've never planned ([[yagni]]).

## How to apply it

- **Start from the use case.** Write what the application *does* as plain code first.
- **Define ports in the core's language.** `findOrder(id)`, not `executeSql(...)`.
- **Keep adapters thin.** Translate, call, translate back.
- **Wire everything in one place.** At startup, a single *composition root* builds the adapters and passes them in.
- **Test the core with fakes.** Test each adapter separately, with focused integration tests against the real technology.
- **Decide what must succeed or fail together.** That's the **unit of work**, usually one database transaction. If a use case calls two ports and the second fails after the first succeeded, what happens?

## Example

```
# core
interface OrderRepository:
    find(id)
    insertIfAbsent(order)
    completeIfPending(id, receipt)
    cancelIfPending(id)

interface PaymentGateway:
    charge(customerId, amount, idempotencyKey) -> Receipt

function placeOrder(cart, checkoutAttemptId, repo, payments):
    existing = repo.find(checkoutAttemptId)
    if existing and existing.isPaid(): return existing       # retry after success
    if existing and existing.isCancelled(): return Rejected  # never revive it

    order = Order.from(cart, id=checkoutAttemptId)   # pure domain rules
    repo.insertIfAbsent(order.asPending())           # record intent first
    receipt = payments.charge(cart.customerId, order.total,
                              idempotencyKey=checkoutAttemptId)
    repo.completeIfPending(order.id, receipt)        # loses to a cancel
    return order

# adapters
class PostgresOrderRepository implements OrderRepository: ...
class InMemoryOrderRepository implements OrderRepository: ...   # fake, for tests
class StripeGateway implements PaymentGateway: ...
```

The `checkoutAttemptId` comes from the caller, so if the client retries the whole request, both attempts carry the same key and the provider charges once ([[idempotency]]).

Saving the order as pending *before* charging means a crash between the steps leaves a pending order, not a charged customer with no order. A background reconciler finds pending orders older than a few minutes, looks each charge up by the order's own reference, and completes or cancels it. Completing and cancelling are both conditional on the order still being pending, so a late retry and the reconciler can't both win; if a cancelled order turns out to have been charged, cancelling means refunding.

## Common traps

- **Shaping ports like the technology.** A port named `saveRowToOrdersTable` leaks the database into the core.
- **Adding too many layers.** You don't need a port for every class — only at real external boundaries.
- **Leaving the core anemic.** If all the logic ends up in adapters, the hexagon is just ceremony.
- **Underestimating mapping cost.** Translating between domain and database models has a cost; accept it where the boundary pays off.
- **Ignoring partial failure across ports.** See the example.

## When it doesn't apply

For simple CRUD (create, read, update, delete) apps with little business logic, the indirection can outweigh the benefit — a thin layer over the database is fine. Introduce ports where you actually feel pain: hard-to-test logic, or infrastructure that is genuinely likely to change.

## Related

- [[functional-core-imperative-shell]] — goes one level deeper: the use case is a small shell, the domain rules are pure.
- [[solid-principles]] — hexagonal is dependency inversion applied to a whole system.
- [[separation-of-concerns]] — the principle behind the inside/outside split.
- [[testing-pyramid]] — hexagonal makes the "many unit tests" base easy to build.
- [[idempotency]] — how to make calls through driven ports safe to retry.
- [[agent-guardrails]] — ports let tests replace destructive operations with spies.
