---
title: API Styles (REST, gRPC, GraphQL)
category: technology
summary: REST, gRPC, and GraphQL are different ways for software to talk over a network; pick by who the callers are and what they need, and keep one convention per context rather than mixing by taste.
tags: [api, rest, grpc, graphql, integration]
---

# API Styles (REST, gRPC, GraphQL)

> **In one sentence:** REST, gRPC, and GraphQL are different ways for software to talk over a network; pick by who the callers are and what they need, and keep one convention per context rather than mixing by taste.

## The idea

An **API** is the contract one piece of software offers another. Over a network, three styles dominate:

- **REST** — representational state transfer: resources at URLs (`/orders/42`), acted on with HTTP methods (`GET`, `POST`, `PUT`, `DELETE`). In practice it means resource-oriented JSON over HTTP. It works everywhere, is readable with any tool, and is cacheable by the web's existing infrastructure.
- **gRPC** — call functions on a remote service as if they were local (`GetOrder(id: 42)`). Contracts are written in Protocol Buffers, a compact binary format, and client code is generated from them. Fast and strongly typed; best between services you control.
- **GraphQL** — one endpoint where the client sends a query describing exactly the fields it wants, across related data, in one request. It was built for mobile apps that needed flexible data with few round trips.

Roy Fielding described REST in his 2000 dissertation; Google open-sourced gRPC and Facebook released GraphQL, both in 2015.

## Why it matters

- **APIs are long-lived promises.** Once others depend on an API, changing its style or shape is a project ([[api-versioning]]).
- **The style shapes performance and tooling.** Caching, streaming, type safety, and debugging all differ by style.
- **Inconsistency is expensive.** Five teams with five conventions means every integration is a fresh learning exercise.

## How to apply it

- **Public or partner APIs: default to REST.** Every language and tool speaks it, and it's easiest to document, debug, and cache. Describe it with an OpenAPI specification (a machine-readable file listing every endpoint, parameter, and response shape).
- **Internal service-to-service calls: consider gRPC.** Generated clients and strict contracts catch mismatches at build time, and it supports streaming. The cost is binary payloads that are harder to inspect, limited browser support, and the need for request-level load balancing. A Layer 4 balancer, which forwards connections without reading them, assigns each *connection* to one server; gRPC keeps one connection open, so all its calls land on that server. Use a Layer 7 balancer, which reads each request and spreads individual calls ([[load-balancers-and-cdns]]).
- **Many clients with different data needs: consider GraphQL.** It suits a product with web and mobile apps that each want different slices of the same data. The cost is server complexity — query cost limits, authorization on every field, and harder caching, because every query goes to one URL, usually as a POST, so ordinary HTTP caches can't tell queries apart.
- **Write the contract first.** Agree on the OpenAPI, Protocol Buffers, or GraphQL schema before building, and check it in CI (continuous integration) with [[contract-testing]].
- **Design for evolution.** Add optional fields; never change the meaning of an existing one ([[expand-and-contract]]).
- **Pick one convention per context and write it down.** Naming, errors, pagination, and authentication should look the same across a company's APIs ([[paved-roads]]).

## Example

A company has a public REST API for partners, a mobile app, and 20 internal services, which have had repeated outages from one service changing a JSON field another relied on. The mobile team complains that one screen makes seven REST calls, and slow phone networks make it sluggish.

Options considered:

- **Convert everything to GraphQL.** Rejected — partners are happy with REST, and a rewrite breaks them.
- **Add one mobile-only REST endpoint that bundles the seven calls.** Rejected — it fixes this screen, but each new screen would need its own custom endpoint.
- **Add GraphQL as a gateway for the apps only.** Accepted — one query fetches what a screen needs, and the gateway calls internal services.
- **Use gRPC between internal services.** Accepted for new services, because generated clients catch those field mismatches at build time; existing ones migrate when touched. Rarely touched services never migrate, so the team accepts two internal styles for years and keeps its REST conventions documented.

The seven calls still happen, but between the gateway and services inside the data center, where they're fast; the phone makes one. The cost: a GraphQL gateway to run, query cost limits to prevent a client from requesting the whole database, and authorization checks that now happen per field rather than per endpoint.

## Common traps

- **Choosing by fashion.** GraphQL for a simple service with one client, or gRPC for a public API, adds cost without benefit.
- **Fake REST.** `POST /doThing` for everything is remote procedure calls in disguise; it gets neither REST's caching nor gRPC's typing.
- **Chatty APIs.** Designing endpoints around database tables forces clients into many round trips.
- **Leaking internals.** Exposing database columns or internal IDs as the contract makes every refactor a breaking change.
- **No pagination or limits.** An endpoint or query that can return everything eventually will.

## When it doesn't apply

Not every integration needs a request–response API. If the caller doesn't need an answer right away, events through a broker may fit better ([[message-brokers]]). And inside one deployable application, plain function calls between modules beat any network API ([[modular-monolith]]).

## Related

- [[api-versioning]] — how to evolve an API once others depend on it.
- [[contract-testing]] — catching breaking changes before deploy.
- [[message-brokers]] — the asynchronous alternative.
- [[expand-and-contract]] — safely changing fields.
- [[microservices]] — where API style decisions multiply.
