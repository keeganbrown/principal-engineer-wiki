---
title: Contract Testing
category: practices
summary: Check that a service and the clients that call it agree on the shape of their API, in each side's own fast test suite, so breaking changes fail before release instead of in production.
tags: [testing, api-design, microservices]
---

# Contract Testing

> **In one sentence:** Check that a service and the clients that call it agree on the shape of their API, in each side's own fast test suite, so breaking changes fail before release instead of in production.

## The idea

When two services talk, there's an implicit agreement — a **contract** — about what requests look like and what responses come back. If the provider renames a field, the consumer breaks. But each team's unit tests only check their own code, so nobody notices until production.

The obvious fix is end-to-end tests that run both services together. They work, but they're slow, flaky, and need a shared environment that's always broken.

A **contract test** checks the agreement without running both sides at once:

- The **consumer** (the client) writes down what it relies on: "When I call `GET /orders/42`, I need a response with `id` (string) and `total` (number)."
- That expectation is saved as a contract file and shared.
- The **provider** (the service) runs the contract against its own code in its **continuous integration (CI)** pipeline — the automated build and tests that run on every change. If it no longer satisfies a consumer, its build fails.

This style is called **consumer-driven contracts**; tools like Pact automate it. A lighter variant is schema-based: both sides test against a shared API description (an OpenAPI spec for HTTP, or a Protobuf schema for gRPC), and CI flags breaking schema changes.

Ian Robinson named consumer-driven contracts in a 2006 article on martinfowler.com.

## Why it matters

- **Breaks surface before merge.** The provider's build fails, where the fix is cheapest.
- **Tests stay fast and reliable.** Each side tests alone; no shared environment, no network flakiness.
- **Providers see what's used.** A field no contract mentions is a strong signal it's unused — but only consumers that publish contracts are counted. Confirm with usage metrics before removing anything ([[expand-and-contract]]).
- **Teams can deploy independently.** That's the main promise of separate services, and contracts make it real.

## How to apply it

- **Start where it hurts.** Pick the API boundary that breaks most often, or the one between two teams who rarely talk.
- **Have consumers specify only what they use.** A contract that asserts every field leaves the provider unable to change anything.
- **Verify against every consumer version still in production.** For a mobile app, that's every supported release, not just the latest. Old app versions stay installed for years.
- **Run a contract broker.** A broker is a shared store for contracts; it answers "is it safe to deploy?" against what's actually live.
- **Diff schemas automatically.** Even without consumer-driven contracts, checking an OpenAPI or Protobuf schema for breaking changes catches structural breaks cheaply.
- **Remember contracts check shape, not meaning.** Changed sort order, stricter validation, or different error codes still pass. Those need review ([[api-versioning]] lists them).
- **Budget for the organizational cost.** Consumers write contracts that mostly protect them; providers maintain test fixtures that put the service into each contract's assumed state; someone runs the broker. Adoption stalls when only one side sees the payoff, so start where both teams feel the pain.

## Example

The mobile app shows an order's `total`. The orders team, cleaning up, renames it to `totalAmount` and updates their own tests. Everything passes.

With contract testing, the mobile team's contract — for every app version still supported — says "`GET /orders/{id}` returns `total` as a number." The orders team's CI runs those contracts and fails: *"Consumer mobile-app 4.2 expects field `total`."* The team adds `totalAmount` alongside `total` instead of replacing it, and nothing breaks for users who haven't updated.

## Common traps

- **Over-specified contracts.** Asserting exact values or every field means any change breaks them.
- **Leaving contracts unverified.** If the provider doesn't run them in CI, they're just documentation.
- **Treating contract tests as end-to-end tests.** They don't check that the whole flow works; keep a few true end-to-end tests for critical journeys.
- **Adopting a heavy tool for two services owned by one team.** The overhead may outweigh the benefit.

## When it doesn't apply

If one team owns both sides and deploys them together, a few integration tests are usually enough. For public APIs with unknown consumers, you can't collect their contracts — use schema checks and a strict [[api-versioning]] policy instead.

## Related

- [[testing-pyramid]] — contract tests replace many slow end-to-end tests between services.
- [[api-versioning]] — contracts tell you when a change is breaking.
- [[expand-and-contract]] — the safe way to make the change a contract test caught.
- [[microservices]] — independent deploys depend on reliable contracts.
