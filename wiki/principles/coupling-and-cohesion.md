---
title: Coupling and Cohesion
category: principles
summary: Good modules keep related things together (high cohesion) and depend on each other as little as possible (low coupling).
tags: [design, modularity, architecture]
---

# Coupling and Cohesion

> **In one sentence:** Good modules keep related things together (high cohesion) and depend on each other as little as possible (low coupling).

## The idea

These two words are the most useful vocabulary for judging any design, from a function to a fleet of services.

- **Cohesion** — how strongly the things *inside* a module belong together. A `Billing` module that holds invoices, payments, and refunds is cohesive. A `Utils` module with date math, string padding, and email sending is not.
- **Coupling** — how much one module depends on the *internals* of another. If changing module A forces you to change module B, they're coupled.

You want **high cohesion, low coupling**: each module is a tight, self-contained unit with a small, stable interface to the rest of the world.

## Why it matters

Coupling determines the **blast radius** of change. In a tightly coupled system, a small change ripples outward, so every change needs coordination, testing everywhere, and nervous deploys. In a loosely coupled system, teams can change their part independently.

Cohesion determines **findability**. When related code lives together, you know where to look and where new code belongs.

## How to apply it

- **Hide internals.** Expose a small interface; keep data structures and helpers private.
- **Depend on stable things.** Depend on interfaces and well-defined contracts, not concrete implementations that change often.
- **Pass data, not objects with behavior,** across boundaries when you can.
- **Group by domain, not by technical type.** Keep "everything about orders" together rather than scattering it across `models/`, `views/`, `services/`.
- **Watch the change log.** If two modules are always edited in the same commit, consider merging them. If one module is edited for unrelated reasons, consider splitting it.

Common forms of coupling, from mildest to worst:

| Kind | Example |
| --- | --- |
| Data | A function takes the two numbers it needs. |
| Stamp | It takes a whole `User` object but only reads `user.id`. |
| Control | A flag argument tells it *how* to behave. |
| Shared global | Both modules read and write the same global or table. |
| Content | One module reaches into another's private fields. |

## Example

Two services, `Orders` and `Shipping`, both read and write the same `orders` database table. Shipping adds a column; Orders' reports break. They're coupled through shared storage.

**Fix:** `Orders` owns the table. It publishes an `OrderPlaced` event (or offers an API). `Shipping` keeps its own data. Now each can change its schema freely.

## Common traps

- **Zero coupling as a goal.** Modules must talk to each other to be useful. The aim is *deliberate* coupling through narrow interfaces.
- **Hidden coupling.** Shared databases, shared config, temporal assumptions ("B runs after A"), and implicit data formats are coupling too — just invisible.
- **Distributed monolith.** Splitting code into services without reducing coupling gives you all the pain of distribution and none of the independence.

## When it doesn't apply

These are always useful lenses, but the right *degree* varies. Inside a small module, tight coupling between private helpers is fine. Loosening coupling usually adds indirection; don't pay that price where change is rare.

## Related

- [[separation-of-concerns]] — the practice that produces cohesive modules.
- [[modular-monolith]] — strong internal boundaries without network calls.
- [[event-driven-architecture]] — a way to reduce runtime coupling between services.
- [[conways-law]] — team structure shapes coupling in the system.
