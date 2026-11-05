---
title: Distributed Monolith
category: antipatterns
summary: Services that are split across the network but still have to change, deploy, and fail together, so you pay for distribution and get none of the independence.
tags: [microservices, coupling, architecture]
---

# Distributed Monolith

> **In one sentence:** Services that are split across the network but still have to change, deploy, and fail together, so you pay for distribution and get none of the independence.

## The idea

Microservices promise independence: each team changes, deploys, and scales its service on its own ([[microservices]]). A distributed monolith has the services but not the independence. Changing one feature still means editing four services, releasing them in a fixed order, and hoping none of them is down.

It happens when a system is split along the wrong lines: by technical layer, by entity (a `user-service`, a `product-service`) instead of by what changes together, or before anyone understood the domain. The coupling that existed inside the monolith is still there. It now crosses the network, where calls are slower, can fail halfway, and are harder to debug.

## Why it matters

- **You pay every cost of distribution.** Network latency, partial failures, distributed tracing, and service-to-service authentication are all real work.
- **You get none of the benefits.** Teams still coordinate releases, so delivery speed doesn't improve.
- **Failures cascade.** If service A calls B, which calls C, synchronously, the chain is only as available as all three together. Three services at 99.9% availability give about 99.7% if their failures are independent ([[service-level-objectives]]). A shared dependency, such as one database, is one more link in the chain, and when it fails, every service fails at once.
- **It's harder to fix than the original monolith.** Moving code back across service boundaries means migrating data and APIs, not just moving functions.

## How to apply it

Spotting it:

- **Releases need a runbook with an order.** "Deploy users, then orders, then billing" means the services aren't independent.
- **Shared libraries hold business logic.** A `common-models` package that every service must upgrade together is a monolith's internals, shipped as a dependency.
- **Services share a database.** Two services reading the same tables are coupled through the schema ([[coupling-and-cohesion]]).
- **One request fans out into long synchronous chains.** A trace that shows five services called in series for one page load is a warning sign ([[observability]]).
- **Most features need changes in several services.** Check the last 20 features: if most touched three or more services, the boundaries are wrong.

Climbing out:

- **Redraw boundaries by domain.** Find where the domain splits naturally ([[domain-driven-design]]), and accept that some services should merge.
- **Merge services that always change together.** Two services that are always released together are one service. If different teams own them, merging the code means merging or reassigning ownership too; settle that first, or the result is a [[god-object|god service]].
- **Replace synchronous chains with events where staleness is acceptable.** A service that keeps its own copy of the data it needs doesn't call out at request time ([[event-driven-architecture]]). The cost: copies go stale, a new consumer must first be loaded with existing data (a *backfill*), and publishing reliably needs an outbox, a table the event is saved to in the same transaction as the change ([[transactional-outbox]]). Use it for the hottest chains, not everywhere.
- **Version contracts so services can deploy separately.** Backward-compatible APIs and contract tests (tests that check a service still sends and accepts what its consumers expect) break the lockstep release ([[api-versioning]], [[contract-testing]]).

## Example

A team split their monolith into `user-service`, `product-service`, `order-service`, and `pricing-service`. Placing an order called all four synchronously. A shared `domain-models` library defined `Order`, and every change to it required redeploying all four in order.

Adding a "gift message" field took three weeks: a library change, four service releases, and a coordinated deploy night. Then `pricing-service` had a bad deploy, and nobody could place orders, because `order-service` blocked on it.

They merged `pricing-service` back into `order-service`, since pricing rules (discounts, tax) only run at checkout; the catalog shows a list price it already stores. The hard part was data: pricing had its own database, so merging meant migrating its data into the orders database, with both databases receiving writes until the move was verified ([[expand-and-contract]]). They also deleted `domain-models` and let each service define its own `Order` shape, with contract tests to catch drift between the shapes. That duplication is the price of independence.

## Common traps

- **Splitting before the domain is understood.** Early boundaries are guesses, and wrong guesses are cheap inside a monolith and expensive across a network. Start with a [[modular-monolith]].
- **Splitting by technical layer.** A "data service," a "logic service," and an "API service" will always change together.
- **Treating merge as defeat.** Teams keep a bad split because merging feels like admitting a mistake. Every sprint spent on the split costs more than the merge would.
- **Adding a service mesh to manage the pain.** A service mesh is infrastructure that handles retries, encryption, and tracing between services. It can make a distributed monolith observable, but it doesn't make it independent.

## When it doesn't apply

Some coupling between services is unavoidable and fine. A checkout flow that needs a payment service to answer synchronously is a reasonable design choice, as long as you plan for that service being down ([[circuit-breaker]]). And two services that deploy together a few times a year have a known, rare coordination cost, not a distributed monolith.

Lockstep deploys can also be the right call for a while, mid-migration, as a temporary state with an end date. The problem is coupling as the *normal* case, not the exception.

## Related

- [[microservices]] — what independence is supposed to look like.
- [[modular-monolith]] — enforce boundaries before adding a network.
- [[coupling-and-cohesion]] — why shared databases and shared models couple services that look separate.
- [[conways-law]] — services drift toward the shape of the teams.
- [[big-ball-of-mud]] — what a distributed monolith usually started as.
