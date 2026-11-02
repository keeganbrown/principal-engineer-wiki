---
title: API Styles (REST, gRPC, GraphQL)
category: technology
summary: REST, gRPC, and GraphQL are different ways for software to talk over a network; pick by who the callers are and what they need, and use one style consistently rather than mixing by taste.
tags: [api, rest, grpc, graphql, integration]
---

# API Styles (REST, gRPC, GraphQL)

> **In one sentence:** REST, gRPC, and GraphQL are different ways for software to talk over a network; pick by who the callers are and what they need, and use one style consistently rather than mixing by taste.

## The idea

An **API** is the contract one piece of software offers another. Over a network, three styles dominate:

- **REST** — resources at URLs (`/orders/42`), acted on with HTTP methods (`GET`, `POST`, `PUT`, `DELETE`), usually with JSON bodies. Roy Fielding described the architectural style in his 2000 dissertation; in practice "REST" usually means "resource-oriented JSON over HTTP." Works everywhere, readable with any tool, cacheable by the web's existing infrastructure.
- **gRPC** — call functions on a remote service as if they were local (`GetOrder(id: 42)`). Contracts are written in Protocol Buffers, a compact binary format, and client code is generated from them. Fast and strongly typed; best between services you control. Google open-sourced it in 2015.
- **GraphQL** — one endpoint where the client sends a query describing exactly the fields it wants, across related data, in one request. Facebook released it in 2015 for mobile apps that needed flexible data with few round trips.

## Why it matters

- **APIs are long-lived promises.** Once others depend on an API, changing its style or shape is a project ([[api-versioning]]).
- **The style shapes performance and tooling.** Caching, streaming, type safety, and debugging all differ by style.
- **Inconsistency is expensive.** Five teams with five conventions means every integration is a fresh learning exercise.

## How to apply it

- **Public or partner APIs: default to REST.** Every language and tool speaks it, and it's easiest to document, debug, and cache. Describe it with an OpenAPI specification.
- **Internal service-to-service calls: consider gRPC.** Generated clients and strict contracts catch mismatches at build time, and it supports streaming. The cost is binary payloads that are harder to inspect and limited browser support.
- **Many clients with different data needs: consider GraphQL.** It suits a product with web and mobile apps that each want different slices of the same data. The cost is server complexity — query cost limits, caching, and authorization on every field.
- **Write the contract first.** Agree on the OpenAPI, Protocol Buffers, or GraphQL schema before building, and check it in CI (continuous integration) with [[contract-testing]].
- **Design for evolution.** Add optional fields; never change the meaning of an existing one ([[expand-and-contract]]).
- **Pick one convention per context and write it down.** Naming, errors, pagination, and authentication should look the same across a company's APIs ([[paved-roads]]).

## Example

A company has a public REST API for partners, a mobile app, and 20 internal services. The mobile team complains that one screen makes seven REST calls, and slow phone networks make it sluggish.

Options considered:

- **Convert everything to GraphQL.** Rejected — partners are happy with REST, and a rewrite breaks them.
- **Add GraphQL as a gateway for the apps only.** Accepted — one query fetches what a screen needs, and the gateway calls internal services.
- **Use gRPC between internal services.** Accepted for new services; existing ones migrate when touched.

The screen now loads in one round trip. The cost: a GraphQL gateway to run, query cost limits to prevent a client from requesting the whole database, and authorization checks that now happen per field rather than per endpoint.

## Common traps

- **Choosing by fashion.** GraphQL for a simple service with one client, or gRPC for a public API, adds cost without benefit.
- **"REST" that's really remote procedure calls** — `POST /doThing` for everything — gets neither REST's caching nor gRPC's typing.
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
