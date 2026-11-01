---
title: Modular Monolith
category: architecture
summary: Build one deployable application divided into well-bounded modules, getting most of the organizational benefits of microservices without the cost of a distributed system.
tags: [architecture, modularity, microservices]
---

# Modular Monolith

> **In one sentence:** Build one deployable application divided into well-bounded modules, getting most of the organizational benefits of microservices without the cost of a distributed system.

## The idea

There's a spectrum of how to structure a system:

| Style | Deploy units | Internal boundaries |
| --- | --- | --- |
| Big ball of mud | One | None — everything calls everything |
| **Modular monolith** | One | Strong — modules talk through public interfaces |
| Microservices | Many | Enforced by the network |

A modular monolith is one codebase and one deployable, but organized into **modules** around business domains (e.g., `catalog`, `orders`, `billing`). Each module has a small public API and keeps everything else private — including its own database tables. Other modules may only use that API.

## Why it matters

Microservices solve real problems — independent deploys, team autonomy, independent scaling — but they add heavy costs: network failures, distributed transactions, versioned APIs, complex debugging, and more infrastructure.

Many teams adopt microservices to get *clean boundaries*, but you can get clean boundaries without a network. A modular monolith gives you:

- **Simple operations** — one deploy, one process, in-process calls, real transactions.
- **Clear ownership** — teams own modules.
- **An escape hatch** — a well-bounded module can later be extracted into a service if it truly needs to be.

## How to apply it

- **Draw modules around business capabilities,** not technical layers.
- **Make each module's public API explicit** — a single entry file or package; everything else internal.
- **Enforce boundaries with tooling**: architecture tests, import linters, or language-level visibility. Good intentions decay without enforcement.
- **No shared tables.** Each module owns its data; others go through its API.
- **Communicate via calls or in-process events.** Use events for side effects ("order placed → send email") to keep modules decoupled.
- **Extract a service only with a reason:** different scaling needs, a different release cadence, or a team that's blocked by the shared deploy.

## Example

An e-commerce app starts as a single Rails or Spring app. Instead of one giant `models/` folder, the team creates `catalog/`, `orders/`, `payments/`, and `shipping/` modules. `orders` calls `payments.charge(...)` — never `PaymentRecord.where(...)`. A CI check fails any build where one module imports another's internals.

Two years in, `payments` needs PCI isolation and its own deploy cadence. Because its boundary is already clean, extracting it into a service takes weeks, not a year-long untangling project.

## Common traps

- **Boundaries in name only.** Folders called "modules" with code reaching freely across them is still a ball of mud.
- **A shared "common" module** that grows into a dumping ground everyone depends on.
- **Shared database tables** — the fastest way to recouple modules.
- **Premature extraction.** Moving to services before the boundaries are proven usually means redrawing them across a network, which is much harder.

## When it doesn't apply

If parts of your system have very different scaling, reliability, or technology needs — or you have many teams that are truly blocked by a shared deployment — services may be worth the cost. Very large organizations often outgrow a single deployable. The usual advice is "monolith first," not "monolith forever."

## Related

- [[coupling-and-cohesion]] — the forces a modular monolith manages.
- [[conways-law]] — align module ownership with teams.
- [[strangler-fig]] — the pattern for later extracting modules into services.
- [[event-driven-architecture]] — in-process events keep modules loosely coupled.
