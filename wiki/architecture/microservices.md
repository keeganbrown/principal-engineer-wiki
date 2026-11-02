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

- **Does one business job.** Orders, payments, search.
- **Owns its own data.** No other service reads its database directly.
- **Deploys independently.** It ships on its own schedule.
- **Has one owning team.**

Services talk over the network, through [[api-styles|APIs]] or [[message-brokers|events]].

The promise is **independence**: teams ship without waiting on each other, each service scales on its own, and a failure in one doesn't have to take down the rest. The price is **distribution**: every call between services can be slow, fail, or arrive twice. You no longer have one database transaction, one log file, or one deploy, and data copied between services is [[cap-theorem|eventually consistent]].

James Lewis and Martin Fowler's 2014 article popularized the term.

## Why it matters

Few architecture decisions are as expensive to get wrong. Teams that split too early often end up with a **distributed monolith** — services that must all be deployed together and fail together, with network calls where function calls used to be. They get every cost and none of the benefits.

Teams that never split, at large scale, can end up with one codebase where hundreds of engineers block each other on every release.

## How to apply it

- **Start with a [[modular-monolith]].** Clean module boundaries are the prerequisite; services just put a network between them. Martin Fowler calls this "monolith first."
- **Split only for a reason you can name.** Good reasons: very different scaling needs, a team blocked by a shared release, or stricter security or compliance isolation. Rarely, a genuinely different technology need — every extra stack is one more thing to hire for, patch, and keep on call.
- **Draw service boundaries around domains.** Never around technical layers; a "database service" couples everything to it ([[domain-driven-design]]).
- **Give each database one owner.** Shared databases recreate the monolith's coupling ([[coupling-and-cohesion]]).
- **Prefer async events for side effects.** Use synchronous calls only when you need an answer now ([[event-driven-architecture]]).
- **Invest in the platform first.** That means automated deploys, [[observability]] with trace IDs (one ID that follows a request across services, also called a correlation ID), [[retries-and-timeouts]], and [[contract-testing]]. Without these, microservices are painful.
- **Plan for partial failure.** Patterns like [[circuit-breaker]], [[saga-pattern]], and [[idempotency]] become everyday tools.
- **Measure what you split for.** Track deploys per team, the share of releases that need cross-team coordination, and lead time for changes (from commit to running in production). If they don't improve, stop extracting.

## Example

A company runs one large Rails app with 80 engineers. Deploys happen weekly and often get rolled back because one team's change broke another's.

They don't rewrite into 40 services. They first enforce module boundaries inside the monolith — and that alone takes deploys from weekly to several times a week. Then they extract the two modules with a clear reason: **search** (very different scaling and its own index) and **payments** (payment card industry (PCI) compliance isolation).

The extractions weren't free. Each service needed its own deploy pipeline, tracing, dashboards, and on-call rotation — roughly two engineers' full-time work to build and keep running. Payments was the hardest; [[modular-monolith]] tells that part of the story. Two years later they have three more services, each extracted for a named reason, and deploy daily.

## Common traps

- **Defaulting to microservices on a small team.** Operational overhead swamps the product work.
- **Splitting too fine.** A service per entity (`UserService`, `AddressService`) creates chatty calls and distributed transactions for every feature.
- **Sharing libraries of domain models.** They couple services' releases ([[dry]] explains why knowledge should cross boundaries through contracts instead).
- **Building synchronous call chains.** Five services deep, the slowest link sets everyone's latency and any failure cascades.
- **Ignoring [[conways-law]].** Services that don't match team boundaries need constant cross-team coordination.

## When it doesn't apply

For a small team, an early product, or a domain you don't understand well yet, a monolith is almost always faster and safer — you can't draw good boundaries before you know the domain. Microservices pay off mainly at organizational scale: many teams, a mature platform, and well-understood domains.

## Related

- [[modular-monolith]] — the usual better starting point, and the path to services.
- [[domain-driven-design]] — how to find service boundaries that last.
- [[conways-law]] — service boundaries should match team boundaries.
- [[strangler-fig]] — how to extract services from an existing system safely.
- [[saga-pattern]] — how to handle business processes that span services.
- [[containers-and-kubernetes]] — running many services is the main reason to orchestrate.
