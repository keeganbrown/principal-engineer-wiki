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

It happens when a system is split along the wrong lines — by technical layer, or by noun, or before anyone understood the domain. The coupling that existed inside the monolith is still there. It now crosses the network, where calls are slower, can fail halfway, and are harder to debug.

## Why it matters

- **You pay every cost of distribution.** Network latency, partial failures, distributed tracing, and service-to-service authentication are all real work.
- **You get none of the benefits.** Teams still coordinate releases, so delivery speed doesn't improve.
- **Failures cascade.** If service A calls B, which calls C, synchronously, the chain is only as available as all three together. Three services at 99.9% availability give about 99.7%.
- **It's harder to fix than the original monolith.** Moving code back across service boundaries means migrating data and APIs, not just moving functions.

## How to apply it

Spotting it:

- **Releases need a runbook with an order.** "Deploy users, then orders, then billing" means the services aren't independent.
- **Shared libraries hold business logic.** A `common-models` package that every service must upgrade together is a monolith's internals, shipped as a dependency.
- **Services share a database.** Two services reading the same tables are coupled through the schema ([[coupling-and-cohesion]]).
- **One request fans out into long synchronous chains.** A trace that shows five services called in series for one page load is a warning sign ([[observability]]).
- **Most features need changes in several services.** Check the last 20 features: if most touched three or more services, the boundaries are wrong.

Getting out:

- **Redraw boundaries around business capabilities.** Find where the domain splits naturally ([[domain-driven-design]]), and accept that some services should merge.
- **Merge services that always change together.** Two services that are always released together are one service. Merging is a valid fix, not a failure.
- **Replace synchronous chains with events where staleness is acceptable.** A service that keeps its own copy of the data it needs doesn't call out at request time ([[event-driven-architecture]]).
- **Version contracts so services can deploy separately.** Backward-compatible APIs and contract tests break the lockstep release ([[api-versioning]], [[contract-testing]]).

## Example

A team split their monolith into `user-service`, `product-service`, `order-service`, and `pricing-service`. Placing an order calls all four synchronously. A shared `domain-models` library defines `Order`, and every change to it requires redeploying all four in order.

Adding a "gift message" field took three weeks: a library change, four service releases, and a coordinated deploy night. Then `pricing-service` had a bad deploy, and nobody could place orders, because order-service blocks on it.

They merge `pricing` back into `order-service`, since prices only matter at order time. The hard part is data: pricing had its own database, so merging means a migration with both writing for a while ([[expand-and-contract]]). They also delete `domain-models` and let each service define its own `Order` shape. That causes some duplication, which is the price of independence.

## Common traps

- **Splitting before the domain is understood.** Early boundaries are guesses, and wrong guesses are cheap inside a monolith and expensive across a network. Start with a [[modular-monolith]].
- **Splitting by technical layer.** A "data service," a "logic service," and an "API service" will always change together.
- **Treating merge as defeat.** Teams keep a bad split because merging feels like admitting a mistake. The cost of that pride compounds every sprint.
- **Adding a service mesh to manage the pain.** Tooling can make a distributed monolith observable, but it doesn't make it independent.

## When it doesn't apply

Some coupling between services is unavoidable and fine. A checkout flow that needs a payment service to answer synchronously is a reasonable design choice, as long as you plan for that service being down ([[circuit-breaker]]). And a system where two services deploy together a few times a year isn't a distributed monolith; it's one with a known, rare coordination cost. The problem is coupling as the *normal* case, not the exception.

## Related

- [[microservices]] — what independence is supposed to look like.
- [[modular-monolith]] — enforce boundaries before adding a network.
- [[coupling-and-cohesion]] — shared databases and shared models.
- [[conways-law]] — services drift toward the shape of the teams.
- [[big-ball-of-mud]] — what a distributed monolith usually started as.
