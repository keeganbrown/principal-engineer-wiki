---
title: Hexagonal Architecture (Ports and Adapters)
category: architecture
summary: Put your business logic at the center and connect it to databases, APIs, and UIs only through interfaces it defines, so the outside world can be swapped without touching the core.
tags: [architecture, design, testing]
---

# Hexagonal Architecture (Ports and Adapters)

> **In one sentence:** Put your business logic at the center and connect it to databases, APIs, and UIs only through interfaces it defines, so the outside world can be swapped without touching the core.

## The idea

Alistair Cockburn proposed this pattern in 2005. Picture your application as a hexagon (the number of sides doesn't matter):

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
- **Ports** are interfaces the core defines: "I need a way to save orders" (`OrderRepository`), "I need to charge cards" (`PaymentGateway`).
- **Adapters** are implementations of those ports for specific technology: `PostgresOrderRepository`, `StripePaymentGateway`, or `InMemoryOrderRepository` for tests.

Dependencies always point **inward**: adapters depend on the core, never the reverse. Similar patterns go by the names *Clean Architecture* and *Onion Architecture*.

## Why it matters

- **Testability.** Run every use case against in-memory adapters — fast, deterministic tests with no infrastructure.
- **Replaceability.** Switch payment providers or databases by writing a new adapter.
- **Longevity.** Frameworks come and go; your business logic doesn't need to go with them.
- **Clarity.** It's always obvious where business rules live.

## How to apply it

- Start from the use case: what does the application *do*? Write that as plain code first.
- When the use case needs something from the outside, **define a port in the core's language** (`findOrder(id)`, not `executeSql(...)`).
- Write adapters at the edge. Keep them thin: translate, call, translate back.
- Wire everything together in one place at startup (the "composition root").
- Test the core with fakes; test each adapter with focused integration tests against the real technology.

## Example

A `PlaceOrder` use case needs to save the order and charge the customer:

```
# core
interface OrderRepository { save(order) }
interface PaymentGateway { charge(customerId, amount) -> Receipt }

function placeOrder(cart, repo, payments):
    order = Order.from(cart)            # pure domain rules
    receipt = payments.charge(cart.customerId, order.total)
    repo.save(order.withReceipt(receipt))
    return order

# adapters
class PostgresOrderRepository implements OrderRepository { ... }
class StripeGateway implements PaymentGateway { ... }
class FakeGateway implements PaymentGateway { ... }   # for tests
```

## Common traps

- **Ports shaped like the technology.** A port named `saveRowToOrdersTable` leaks the database into the core.
- **Too many layers.** You don't need a port for every class — only at real external boundaries.
- **Anemic core.** If all the logic ends up in adapters, the hexagon is just ceremony.
- **Mapping fatigue.** Translating between domain and database models has a cost; accept it where the boundary pays off.

## When it doesn't apply

For simple CRUD apps with little business logic, the indirection can outweigh the benefit — a thin layer over the database is fine. Introduce ports where you actually feel pain: hard-to-test logic, or infrastructure likely to change.

## Related

- [[functional-core-imperative-shell]] — a complementary pattern for keeping the core pure.
- [[solid-principles]] — hexagonal is dependency inversion at the system level.
- [[separation-of-concerns]] — the principle behind the inside/outside split.
- [[testing-pyramid]] — hexagonal makes the "many unit tests" base easy to build.
