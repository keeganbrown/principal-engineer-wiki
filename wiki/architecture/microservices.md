---
title: Microservices
category: architecture
summary: Split a system into small, independently deployable services only when independent deploys, scaling, or team autonomy are worth the real cost of running a distributed system.
tags: [architecture, distributed-systems, organization]
---

# Microservices

> **In one sentence:** Split a system into small, independently deployable services only when independent deploys, scaling, or team autonomy are worth the real cost of running a distributed system.

## The idea

A microservice architecture builds one product out of many small services. Each service:

- does one business job (orders, payments, search),
- **owns its own data** — no other service reads its database directly,
- is **deployed independently**, on its own schedule,
- is usually owned by one team.

Services talk over the network, through APIs or events.

The promise is **independence**: teams ship without waiting on each other, each service scales on its own, and a failure in one doesn't have to take down the rest.

The price is **distribution**: every call between services can be slow, fail, or arrive twice. You no longer have one database transaction, one log file, or one deploy.

## Why it matters

Few architecture decisions are as expensive to get wrong. Teams that split too early often end up with a **distributed monolith** — services that must all be deployed together and fail together, with network calls where function calls used to be. They get every cost and none of the benefits.

Teams that never split, at large scale, can end up with one codebase where hundreds of engineers block each other on every release.

## How to apply it

- **Start with a [[modular-monolith]]** unless you have a specific reason not to. Clean module boundaries are the prerequisite; services just put a network between them.
- **Split for a reason you can name:** a part with very different scaling needs, a team blocked by a shared release, stricter security or compliance isolation, or a different technology need.
- **Draw service boundaries around business domains** ([[domain-driven-design]]), never around technical layers. A "database service" or "validation service" couples everything to it.
- **One owner per service, one owner per database.** Shared databases recreate the monolith's coupling ([[coupling-and-cohesion]]).
- **Prefer async events for side effects,** sync calls only when you need an answer now ([[event-driven-architecture]]).
- **Invest in the platform first:** automated deploys, [[observability]] with trace IDs across services, [[retries-and-timeouts]], and [[contract-testing]]. Without these, microservices are painful.
- **Expect to handle partial failure** with patterns like [[circuit-breaker]], [[saga-pattern]], and [[idempotency]].

## Example

A company runs one large Rails app with 80 engineers. Deploys happen weekly and often get rolled back because one team's change broke another's.

They don't rewrite into 40 services. They first enforce module boundaries inside the monolith. Then they extract the two modules with a clear reason: **search** (needs very different scaling and its own index) and **payments** (needs PCI — payment card industry — compliance isolation). Everything else stays in the monolith. Two years later they have five services and a healthy monolith, and deploy daily.

## Common traps

- **Microservices as a default** for a small team — operational overhead swamps the product work.
- **Too fine-grained.** A service per entity (`UserService`, `AddressService`) creates chatty calls and distributed transactions for every feature.
- **Shared libraries of domain models** across services, which couple their releases.
- **Synchronous call chains** five services deep — the slowest link sets everyone's latency, and any failure cascades.
- **Ignoring [[conways-law]].** Services that don't match team boundaries need constant cross-team coordination.

## When it doesn't apply

For a small team, an early product, or a domain you don't understand well yet, a monolith is almost always faster and safer — you can't draw good boundaries before you know the domain. Microservices pay off mainly at organizational scale: many teams, a mature platform, and well-understood domains.

## Related

- [[modular-monolith]] — the usual better starting point, and the path to services.
- [[domain-driven-design]] — how to find service boundaries that last.
- [[conways-law]] — service boundaries should match team boundaries.
- [[strangler-fig]] — how to extract services from an existing system safely.
- [[saga-pattern]] — how to handle business processes that span services.
