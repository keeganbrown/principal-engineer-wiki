---
title: Domain-Driven Design (DDD)
category: architecture
summary: Shape your software around the real business domain and the language experts use, and split large systems into bounded contexts where each word has one clear meaning.
tags: [architecture, modeling, boundaries]
---

# Domain-Driven Design (DDD)

> **In one sentence:** Shape your software around the real business domain and the language experts use, and split large systems into bounded contexts where each word has one clear meaning.

## The idea

Eric Evans introduced DDD in his 2003 book. Its core claim: the hardest part of most software isn't the technology — it's understanding the business. So put the business model at the center of the design, and build it together with the people who know the domain best.

DDD has two halves:

- **Strategic design** — how to divide a big system into parts. This is where most of the value is.
- **Tactical design** — building blocks for the code inside each part (entities, value objects, aggregates).

Three ideas carry most of the weight:

1. **Ubiquitous language.** Developers and domain experts use the *same* words for the same things — in meetings, in docs, and in code. If the business says "policy holder," the class isn't called `CustomerRecord`.
2. **Bounded context.** A boundary inside which a model and its language are consistent. "Customer" in *Sales* (a lead with a pipeline stage) is different from "Customer" in *Support* (someone with tickets). Don't force one model to serve both.
3. **Context map.** A picture of how bounded contexts relate and translate between each other.

## Why it matters

Big systems fail when one giant model tries to mean everything to everyone. The `Customer` class grows 80 fields, every team edits it, and every change breaks someone. Bounded contexts give you natural boundaries for modules, services, and teams — boundaries that follow the business, so they stay stable as the code changes.

A shared language also cuts down on translation errors: fewer "oh, *that's* what you meant" moments after a feature ships.

## How to apply it

- **Talk to domain experts early and often.** Run workshops (e.g., *Event Storming*: map business events on a wall with sticky notes).
- **Write a glossary** of key terms per context and use those exact words in code.
- **Look for language shifts.** When the same word means different things to different groups, you've found a context boundary.
- **Give each bounded context one owning team** and its own data.
- **Translate at the edges** with an *anti-corruption layer* when talking to another context or a legacy system, so its model doesn't leak into yours.
- **Use tactical patterns where the logic is rich:**
  - *Entity* — has an identity that persists (an `Order` #42).
  - *Value object* — defined only by its values, immutable (`Money(10, "USD")`).
  - *Aggregate* — a cluster of objects changed together through one root, guarding its rules (an `Order` with its `LineItems`).

## Example

An insurance company has one `Policy` table used by underwriting, billing, and claims. Each team keeps adding columns; changes require three-team sign-off.

Using DDD, they map three bounded contexts. *Underwriting* models a policy as a risk assessment. *Billing* models it as a payment schedule. *Claims* models it as a coverage contract. Each context owns its own model and data, linked by a shared `policyId`, and they communicate through events like `PolicyIssued`. Teams now ship independently.

## Common traps

- **Tactical-only DDD.** Adding "repositories" and "aggregates" to code without doing the strategic work misses the point.
- **Contexts drawn around tech** (a "database context") instead of business capabilities.
- **One canonical enterprise model.** The urge to create a single "true" `Customer` for the whole company is exactly what DDD warns against.
- **Huge aggregates.** Keep aggregates small; large ones cause lock contention and slow writes.

## When it doesn't apply

For simple CRUD apps, data pipelines, or domains with little business logic, full DDD is overkill. The strategic ideas — shared language and clear boundaries — are still cheap and useful almost everywhere; the tactical patterns pay off only where the rules are genuinely complex.

## Related

- [[modular-monolith]] — bounded contexts make natural module boundaries.
- [[conways-law]] — align teams with bounded contexts.
- [[hexagonal-architecture]] — a good way to structure the code inside one context.
- [[event-driven-architecture]] — a common way for contexts to communicate.
- [[coupling-and-cohesion]] — contexts maximize cohesion within and limit coupling between.
