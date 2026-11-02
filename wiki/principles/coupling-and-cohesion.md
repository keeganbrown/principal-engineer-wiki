---
title: Coupling and Cohesion
category: principles
summary: Good modules keep related things together (high cohesion) and depend on each other as little as possible (low coupling).
tags: [design, modularity, architecture]
---

# Coupling and Cohesion

> **In one sentence:** Good modules keep related things together (high cohesion) and depend on each other as little as possible (low coupling).

## The idea

These two words let you judge any design, from a function to a fleet of services.

- **Cohesion** — how strongly the things *inside* a module belong together. A `Billing` module that holds invoices, payments, and refunds is cohesive. A `Utils` module with date math, string padding, and email sending is not.
- **Coupling** — how much one module depends on the *internals* of another. If changing module A forces you to change module B, they're coupled.

You want **high cohesion, low coupling**: each module is a tight, self-contained unit with a small, stable interface to the rest of the world.

Coupling comes in degrees. This classic ranking comes from the structured-design work of Larry Constantine and colleagues (Stevens, Myers, and Constantine, 1974; Yourdon and Constantine, *Structured Design*, 1979):

| Kind | Example | Why it hurts |
| --- | --- | --- |
| Data | A function takes the two numbers it needs. | Barely — this is the goal. |
| Stamp | It takes a whole `User` but only reads `user.id`. | It now breaks if `User` changes shape. |
| Control | A flag argument tells it *how* to behave. | The caller must know the callee's internal branches. |
| Shared global | Both modules read and write the same global or table. | Either can break the other invisibly. |
| Content | One module reaches into another's private fields. | Any internal change breaks the other. |

The table is about **boundaries** between modules. Inside one module, passing a cohesive object is often clearer than unpacking it into many arguments.

## Why it matters

Coupling determines the **blast radius** of change. In a tightly coupled system, a small change ripples outward, so every change needs coordination, testing everywhere, and nervous deploys. In a loosely coupled system, teams can change their part independently.

Cohesion determines **findability**. When related code lives together, you know where to look and where new code belongs.

## How to apply it

- **Hide internals.** Expose a small interface; keep data structures and helpers private.
- **Depend on stable things.** Depend on interfaces and well-defined contracts, not on implementations that change often ([[hexagonal-architecture|dependency inversion]]).
- **Pass plain data across boundaries.** Plain data can't call back into the sender, so the receiver depends only on the data's shape, not the sender's code.
- **Group by domain.** Keep "everything about orders" together rather than scattering it across `models/`, `views/`, `services/`. Code in one domain changes together; code in one technical layer usually doesn't. ([[domain-driven-design]] covers how to find domain boundaries.)
- **Watch the change log.** If two modules are always edited in the same commit, consider merging them. If one module is edited for unrelated reasons, consider splitting it.

## Example

A common, invisible kind is **shared-database coupling**. Two services, `Orders` and `Shipping`, both read and write the same `orders` table. Shipping adds a column; Orders' reports break. They're coupled through shared storage — and nothing in either codebase shows it.

**Fix:** `Orders` owns the table. It publishes an `OrderPlaced` event (or offers an API). `Shipping` keeps its own copy of what it needs.

The coupling doesn't disappear — it **moves** to the `OrderPlaced` contract, which now needs careful [[api-versioning]]. Shipping's copy is also [[cap-theorem|eventually consistent]]: it may lag a few seconds behind. The win is that the coupling is now *explicit and narrow* — one documented message instead of a whole table — not that it's gone.

## Common traps

- **Zero coupling as a goal.** Modules must talk to be useful. The aim is *deliberate* coupling through narrow interfaces.
- **Hidden coupling.** Shared databases, shared config, timing assumptions ("B runs after A"), and implicit data formats are coupling too — just invisible.
- **Distributed monolith.** Splitting code into services without reducing coupling gives you all the pain of distribution and none of the independence ([[distributed-monolith]]).

## When it doesn't apply

These are always useful lenses, but the right *degree* varies. Inside a small module, tight coupling between private helpers is fine. Loosening coupling usually adds indirection — an interface, an event, a copy of data — so don't pay that price where change is rare. Sometimes two pieces genuinely belong together, and merging them is the better fix.

## Related

- [[separation-of-concerns]] — the practice that produces cohesive modules.
- [[modular-monolith]] — strong internal boundaries without network calls.
- [[event-driven-architecture]] — trades runtime coupling for contract coupling.
- [[conways-law]] — team structure shapes coupling in the system.
- [[domain-driven-design]] — how to find boundaries that keep cohesion high.
- [[navigable-codebases]] — grouping by domain also makes code findable by search, for people and agents.
