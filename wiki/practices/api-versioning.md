---
title: API Versioning and Evolution
category: practices
summary: Treat an API as a promise to its callers — evolve it with backward-compatible changes by default, and when you must break it, version it and give people time to move.
tags: [api-design, compatibility, contracts]
---

# API Versioning and Evolution

> **In one sentence:** Treat an API as a promise to its callers — evolve it with backward-compatible changes by default, and when you must break it, version it and give people time to move.

## The idea

Once someone depends on your API — a mobile app, a partner, another team's service — you can't change it freely. Old mobile app versions stay installed for years. Partners update on their own schedule. Breaking them breaks *their* product.

Changes come in two kinds:

- **Backward-compatible (safe)** — add a new optional field, a new endpoint, a new optional parameter, or a new enum value *that clients are prepared to ignore*.
- **Breaking** — remove or rename a field, change a type, make an optional field required, change meaning or default behavior, or tighten validation.

The best versioning strategy is to **need it rarely**: design APIs that can grow through additive changes, using [[expand-and-contract]] for anything else.

## Why it matters

Breaking changes are among the most expensive mistakes in software because their cost lands on other people, often outside your control. A principal engineer is often the person who notices that an "internal cleanup" is actually a breaking change for 40 downstream consumers. A published API is a classic [[reversible-decisions|one-way door]].

## How to apply it

- **Make clients tolerant readers.** Clients should ignore fields they don't recognize, so you can add new ones safely. (Martin Fowler calls this the *Tolerant Reader* pattern.)
- **Make servers strict from day one.** Anything you tolerate becomes behavior someone depends on, and tightening it later is a breaking change. This is why the old robustness principle — "be liberal in what you accept" (Jon Postel) — is now treated with caution; RFC 9413 explains why. (An RFC — "request for comments" — is one of the Internet's standards documents; this one is from the Internet Architecture Board, 2023.)
- **Never reuse or repurpose a field.** Add a new one and deprecate the old.
- **Evolve additively.** Add the new alongside the old, migrate consumers, then remove the old ([[expand-and-contract]]).
- **Version explicitly when you must break.** Common approaches:
  - URL — `/v2/orders`. Simple and visible.
  - Header — `Accept: application/vnd.example.v2+json`, a custom media type that names the version. Keeps URLs clean.
  - Date-based — e.g. Stripe's `Stripe-Version: 2024-09-30.acacia` or GitHub's `X-GitHub-Api-Version: 2022-11-28`. Very fine-grained, but you must maintain a translation layer that converts responses for every past version — worth it mainly for large public APIs.
- **Publish a deprecation policy.** For example, 12 months' notice, announced with the standard `Deprecation` (RFC 9745) and `Sunset` (RFC 8594) response headers.
- **Track usage per version and per client.** Without it, you can never safely remove anything or know whom to contact.
- **Catch accidental breaks in continuous integration (CI).** Use schema diffs or [[contract-testing|contract tests]].
- **Version events and messages too.** They are APIs.

## Example

An orders API returns money as a float: `"total": 19.99`. Rounding errors are causing billing disputes, and the team needs integer cents with an explicit currency: `"total": {"amountCents": 1999, "currency": "USD"}`. The *type* of `total` changes, so this can't be done additively under the same name.

The team ships `/v2/orders` with the new shape and leaves `/v1` unchanged. `/v1` responses start carrying `Deprecation` and `Sunset: Sun, 31 Oct 2027 00:00:00 GMT` headers. Per-client usage dashboards show which partners still call `/v1`; the team emails each one twice and offers migration help.

A year later, two partners still haven't moved. Rather than break them on the sunset date, the team extends the date by three months for those two and switches `/v1` off afterward — a decision recorded in an [[architecture-decision-records|ADR (architecture decision record)]].

## Common traps

- **Versioning every change.** Ten versions to maintain is far worse than additive evolution.
- **Assuming internal APIs are safe to break.** Internal consumers break too — and are often harder to find.
- **Missing hidden breaking changes.** Stricter validation, changed sort order, new required headers, and different error codes all break clients.
- **Crashing on new enum values.** Clients that handle enums exhaustively break when you add one. Document that enums may grow.

## When it doesn't apply

If you control every client and deploy them together (e.g., a backend used only by one web app shipped in the same release), you can change the API in lockstep. Even then, **rolling deploys** — updating servers a few at a time — mean old and new versions briefly coexist, so additive changes remain the safer habit.

## Related

- [[expand-and-contract]] — the step-by-step technique for non-breaking change.
- [[contract-testing]] — tells you when a change would break a consumer.
- [[event-driven-architecture]] — event schemas need the same compatibility discipline.
- [[coupling-and-cohesion]] — an API is the deliberate coupling point between systems.
- [[architecture-decision-records]] — record versioning policy and major breaking changes.
- [[api-styles]] — REST, gRPC, GraphQL: the style shapes how versioning works.
