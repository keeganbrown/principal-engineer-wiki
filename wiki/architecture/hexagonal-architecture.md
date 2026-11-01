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

- **The core** holds business rules and use cases. It knows nothing about HTTP, SQL, or vendors.
- **Ports** are interfaces the core defines, in its own language: "I need a way to save orders" (`OrderRepository`), "I need to charge cards" (`PaymentGateway`).
- **Adapters** implement ports for specific technology.
  - **Driving adapters** *call into* the core: a web controller, a command-line tool, a test.
  - **Driven adapters** *are called by* the core: `PostgresOrderRepository`, `StripeGateway`, or an `InMemoryOrderRepository` fake for tests.

Dependencies always point **inward**. That can seem impossible — how does the core save to Postgres without depending on it? The trick: the core calls `OrderRepository`, an interface it *owns*. `PostgresOrderRepository` implements that interface. So at runtime the call goes outward, but in the code, the adapter depends on the core, not the reverse. This is dependency inversion; this article owns it for the wiki.

Alistair Cockburn proposed the pattern in 2005. *Clean Architecture* and *Onion Architecture* are close relatives.

## Why it matters

- **Testability.** Run every use case against in-memory fakes — fast, deterministic tests with no infrastructure. This is the dependable win.
- **Clarity.** It's always obvious where business rules live.
- **Longevity.** Frameworks come and go; your business logic doesn't need to go with them.
- **Partial replaceability.** You *can* switch providers by writing a new adapter, but be honest: a port designed around one vendor rarely fits the second without reshaping, and database transaction behavior leaks through repository ports. Don't justify a port by a swap you've never planned ([[yagni]]).

## How to apply it

- **Start from the use case.** What does the application *do*? Write that as plain code first.
- **Define ports in the core's language** when the use case needs the outside world: `findOrder(id)`, not `executeSql(...)`.
- **Keep adapters thin:** translate, call, translate back.
- **Wire everything together in one place at startup** (the "composition root").
- **Test the core with fakes,** and test each adapter with focused integration tests against the real technology.
- **Decide where the unit of work lives.** If a use case calls two ports, what happens when the second fails after the first succeeded?

## Example

```
# core
interface OrderRepository:
    save(order)

interface PaymentGateway:
    charge(customerId, amount, idempotencyKey) -> Receipt

function placeOrder(cart, repo, payments):
    order = Order.from(cart)                 # pure domain rules (a functional core)
    repo.save(order.asPending())             # record intent first
    receipt = payments.charge(cart.customerId, order.total, idempotencyKey=order.id)
    repo.save(order.withReceipt(receipt))
    return order

# adapters
class PostgresOrderRepository implements OrderRepository: ...
class InMemoryOrderRepository implements OrderRepository: ...   # fake, for tests
class StripeGateway implements PaymentGateway: ...
```

Saving the order as pending *before* charging, and passing an idempotency key, means a crash between the two steps leaves a recoverable pending order — not a charged customer with no order ([[idempotency]]).

## Common traps

- **Ports shaped like the technology.** A port named `saveRowToOrdersTable` leaks the database into the core.
- **Too many layers.** You don't need a port for every class — only at real external boundaries.
- **An anemic core.** If all the logic ends up in adapters, the hexagon is just ceremony.
- **Mapping fatigue.** Translating between domain and database models has a cost; accept it where the boundary pays off.
- **Ignoring partial failure across ports,** as the example shows.

## When it doesn't apply

For simple CRUD (create-read-update-delete) apps with little business logic, the indirection can outweigh the benefit — a thin layer over the database is fine. Introduce ports where you actually feel pain: hard-to-test logic, or infrastructure that is genuinely likely to change.

## Related

- [[functional-core-imperative-shell]] — goes one level deeper: the use case is a small shell, the domain rules are pure.
- [[solid-principles]] — hexagonal is dependency inversion applied to a whole system.
- [[separation-of-concerns]] — the principle behind the inside/outside split.
- [[testing-pyramid]] — hexagonal makes the "many unit tests" base easy to build.
- [[idempotency]] — how to make calls through driven ports safe to retry.
