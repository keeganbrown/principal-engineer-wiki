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
| Microservices | Many | Separated by the network (but can still be tangled) |

A modular monolith is one codebase and one deployable, organized into **modules** by domain (e.g., `catalog`, `orders`, `billing`). Each module has a small public API and keeps everything else private — including its own database tables. Other modules may only use that API.

## Why it matters

[[microservices|Microservices]] solve real problems — independent deploys, team autonomy, independent scaling — but they add heavy costs: network failures, [[saga-pattern|multi-service transactions]], [[api-versioning|versioned APIs]], harder debugging, and more infrastructure.

Many teams adopt microservices to get *clean boundaries*. But you can get clean boundaries without a network ([[kiss]]). A modular monolith gives you:

- **Simple operations** — one deploy, one process, in-process calls, real transactions.
- **Clear ownership** — teams own modules.
- **An escape hatch** — a well-bounded module can later be extracted into a service if it truly needs to be.

## How to apply it

- **Group modules by domain.** Not by technical layer ([[domain-driven-design]] shows how to find domains).
- **Make each module's public API explicit.** Expose a single entry file or package; keep everything else internal.
- **Enforce boundaries with tooling.** Use architecture tests, import linters, or language-level visibility. Good intentions decay without enforcement, so bake the checks into your service template ([[paved-roads]]).
- **Give each module its own tables.** Others go through its API ([[coupling-and-cohesion]] explains why shared tables recouple everything).
- **Avoid transactions that span modules.** A single transaction across `orders` and `payments` is convenient today, but it's the hidden coupling that turns a later extraction from weeks into a redesign.
- **Use in-process events for side effects.** "Order placed → send email" keeps modules decoupled.
- **Extract a service only for a reason you can name.** [[microservices]] lists the good ones.

## Example

An e-commerce app starts as a single application. Instead of one giant `models/` folder, the team creates `catalog/`, `orders/`, `payments/`, and `shipping/` modules. `orders` calls `payments.charge(...)` — it never queries the payments tables directly. A continuous integration (CI) check fails any build where one module imports another's internals.

Two years in, `payments` needs payment card industry (PCI) compliance isolation and its own deploy cadence. Its code boundary is already clean, so the code moves quickly. The slow part is the two places where `orders` and `payments` still shared a database transaction: each has to become a small [[saga-pattern|saga]] — a sequence of local steps with undo actions. Because the team had kept those to a minimum, the extraction takes a couple of months instead of a year.

## Common traps

- **Boundaries in name only.** Folders called "modules" with code reaching freely across them is still a ball of mud.
- **Growing a shared "common" module.** It becomes a dumping ground everyone depends on.
- **Shared database tables** — the fastest way to recouple modules.
- **Forgetting shared runtime fate.** One module's memory leak, runaway query, or bad deploy takes down every module. Monitor per module, and keep risky work isolated.
- **Premature extraction.** Moving to services before boundaries are proven usually means redrawing them across a network, which is much harder.

## When it doesn't apply

If parts of your system have very different scaling, reliability, or technology needs — or many teams are truly blocked by a shared deployment — services may be worth the cost. Very large organizations often outgrow a single deployable. The usual advice is "monolith first," not "monolith forever."

## Related

- [[microservices]] — the alternative, and when it's worth it.
- [[coupling-and-cohesion]] — the forces a modular monolith manages.
- [[domain-driven-design]] — bounded contexts are the best guide for drawing module lines.
- [[conways-law]] — align module ownership with teams.
- [[strangler-fig]] — the pattern for later extracting modules into services.
