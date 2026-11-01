---
title: Contract Testing
category: practices
summary: Check that a service and the clients that call it agree on the shape of their API, in each side's own fast test suite, so breaking changes fail in CI instead of in production.
tags: [testing, api-design, microservices]
---

# Contract Testing

> **In one sentence:** Check that a service and the clients that call it agree on the shape of their API, in each side's own fast test suite, so breaking changes fail in CI instead of in production.

## The idea

When two services talk, there's an implicit agreement — a **contract** — about what requests look like and what responses come back. If the provider renames a field, the consumer breaks. But each team's unit tests only check their own code, so nobody notices until production.

The obvious fix is end-to-end tests that run both services together. They work, but they're slow, flaky, and need a shared environment that's always broken.

A **contract test** checks the agreement without running both sides at once:

- The **consumer** (the client) writes down what it relies on: "When I call `GET /orders/42`, I need a response with `id` (string) and `total` (number)."
- That expectation is saved as a **contract** file and shared.
- The **provider** (the service) runs the contract against its own code in its own CI. If it no longer satisfies a consumer's expectations, its build fails.

This style is called **consumer-driven contracts**. Tools like Pact automate it. A lighter variant is **schema-based**: both sides test against a shared OpenAPI or Protobuf schema, and CI flags breaking schema changes.

## Why it matters

- **Breaking changes are caught before merge,** on the provider side, where they're cheapest to fix.
- **Fast and reliable.** Each side tests alone; no shared environment, no network flakiness.
- **Providers learn what's actually used.** If no contract mentions a field, it can be removed safely.
- **Teams can deploy independently** with real confidence — the main promise of separate services.

## How to apply it

- **Start where it hurts.** Pick the API boundary that breaks most often, or the one between two teams who rarely talk.
- **Consumers specify only what they use.** A contract that asserts every field makes the provider unable to change anything.
- **Run provider verification in CI on every change,** against every consumer's latest contract.
- **Use a contract broker** (a shared store for contracts) so providers can check "is it safe to deploy?" against what's live.
- **Check schema changes automatically.** Even without full consumer-driven contracts, diffing an OpenAPI or Protobuf schema for breaking changes catches most problems.
- **Keep business logic out of contracts.** They test shape and meaning of the interface, not every behavior — that's what the provider's own tests are for.

## Example

The mobile app shows an order's `total`. The orders team, cleaning up, renames it to `totalAmount` and updates their own tests. Everything passes.

With contract testing, the mobile team's contract says "`GET /orders/{id}` returns `total` as a number." The orders team's CI runs that contract and fails: *"Consumer mobile-app expects field `total`."* The orders team adds `totalAmount` alongside `total` instead of replacing it ([[expand-and-contract]]), and nothing breaks for the app users who haven't updated yet.

## Common traps

- **Over-specified contracts** that assert exact values or every field, so any change breaks them.
- **Contracts nobody verifies.** If the provider doesn't run them in CI, they're just documentation.
- **Treating contract tests as end-to-end tests.** They don't check that the whole flow works — keep a few true end-to-end tests for critical journeys.
- **Adopting a heavy tool for two services owned by one team.** The overhead may outweigh the benefit.

## When it doesn't apply

If one team owns both sides and deploys them together, a few integration tests are usually enough. For public APIs with unknown consumers, you can't collect their contracts — use schema checks and a strict [[api-versioning]] policy instead.

## Related

- [[testing-pyramid]] — contract tests replace many slow end-to-end tests between services.
- [[api-versioning]] — contracts tell you when a change is breaking.
- [[expand-and-contract]] — the safe way to make the change a contract test caught.
- [[microservices]] — independent deploys depend on reliable contracts.
