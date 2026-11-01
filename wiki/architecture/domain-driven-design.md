---
title: Domain-Driven Design (DDD)
category: architecture
summary: Shape your software around the real business domain and the language experts use, and split large systems into bounded contexts where each word has one clear meaning.
tags: [architecture, modeling, boundaries]
---

# Domain-Driven Design (DDD)

> **In one sentence:** Shape your software around the real business domain and the language experts use, and split large systems into bounded contexts where each word has one clear meaning.

## The idea

The hardest part of most software isn't the technology — it's understanding the business. So put the business model at the center of the design, and build it together with the people who know the domain best.

DDD has two halves:

- **Strategic design** — how to divide a big system into parts. This is where most of the value is.
- **Tactical design** — building blocks for the code inside each part.

Three strategic ideas carry most of the weight:

1. **Ubiquitous language.** Developers and domain experts use the *same* words for the same things — in meetings, docs, and code. If the business says "policy holder," the class isn't called `CustomerRecord`.
2. **Bounded context.** A boundary inside which a model and its language are consistent. "Customer" in *Sales* (a lead with a pipeline stage) is different from "Customer" in *Support* (someone with tickets). Don't force one model to serve both.
3. **Context map.** A picture of how bounded contexts relate and translate between each other.

Eric Evans introduced DDD in his 2003 book *Domain-Driven Design*.

## Why it matters

Big systems fail when one giant model tries to mean everything to everyone. The `Customer` class grows 80 fields, every team edits it, and every change breaks someone. Bounded contexts give you natural boundaries for modules, services, and teams — boundaries that follow the business, so they stay stable as the code changes.

For *why* grouping by domain reduces coupling, see [[coupling-and-cohesion]]; the rest of this article is about *how* to find the boundaries.

## How to apply it

- **Classify your subdomains first.** The **core domain** is what makes your business different — invest deep modeling there. **Supporting** subdomains are needed but not special. **Generic** subdomains (authentication, invoicing engines) are solved problems — buy them or keep them simple. Applying DDD evenly everywhere is the most common way it gets expensive.
- **Talk to domain experts early and often.** Try *Event Storming*, Alberto Brandolini's workshop format: map business events on a wall with sticky notes.
- **Write a glossary per context.** Use those exact words in code.
- **Look for language shifts.** When the same word means different things to different groups, you've found a context boundary.
- **Give each bounded context one owning team.** The context also owns its data.
- **Translate at the edges.** When talking to another context or a legacy system, use an **anti-corruption layer** — a small translation module — so its model doesn't leak into yours ([[strangler-fig]] uses this heavily).
- **Use tactical patterns only where the logic is rich.** The main ones:
  - *Entity* — has an identity that persists (order #42).
  - *Value object* — defined only by its values, immutable (`Money(10, "USD")`).
  - *Aggregate* — a cluster of objects changed as a unit through one **root**. Outside code may only change an order's `LineItems` by calling methods on `Order` (the root), so `Order` can enforce rules like "the total can't be negative."
  - *Repository* — loads and saves whole aggregates, hiding the database.

## Example

An insurance company has one `Policy` table used by underwriting, billing, and claims. Each team keeps adding columns; changes require three-team sign-off.

Using DDD, they map three bounded contexts: *Underwriting* models a policy as a risk assessment, *Billing* as a payment schedule, and *Claims* as a coverage contract. Their context map shows Underwriting publishing a `PolicyIssued` event that Billing and Claims consume, linked by a shared `policyId`.

The split takes several quarters. The hardest part isn't code — it's agreeing which context owns fields everyone touches, like policy status, and migrating data without downtime. Once done, the teams ship independently.

## Common traps

- **Tactical-only DDD.** Adding "repositories" and "aggregates" without doing the strategic work misses the point.
- **Drawing contexts around technology.** A "database context" isn't a domain.
- **One canonical enterprise model.** The urge to create a single "true" `Customer` for the whole company is exactly what DDD warns against. ([[dry]] makes the same point from the other side: don't share domain-model libraries across services.)
- **Huge aggregates.** Keep aggregates small. Because an aggregate is saved as one unit, two edits anywhere inside it conflict — and a large one is edited by many users at once.

## When it doesn't apply

For simple CRUD (create, read, update, delete) apps, data pipelines, or domains with little business logic, full DDD is overkill. The strategic ideas — shared language and clear boundaries — are cheap and useful almost everywhere; the tactical patterns pay off only where the rules are genuinely complex.

## Related

- [[modular-monolith]] — bounded contexts make natural module boundaries.
- [[microservices]] — bounded contexts make natural service boundaries.
- [[conways-law]] — align teams with bounded contexts.
- [[hexagonal-architecture]] — a good way to structure the code inside one context.
- [[event-driven-architecture]] — a common way for contexts to communicate.
- [[strangler-fig]] — anti-corruption layers protect new code from legacy models.
