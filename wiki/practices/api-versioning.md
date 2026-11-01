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

- **Backward-compatible (safe):** add a new optional field, a new endpoint, a new optional parameter, a new enum value *that clients are prepared to ignore*.
- **Breaking:** remove or rename a field, change a type, make an optional field required, change meaning or default behavior, tighten validation.

The best versioning strategy is to **need it rarely**: design APIs that can grow through additive changes.

## Why it matters

Breaking changes are among the most expensive mistakes in software because their cost lands on other people, often outside your control. A principal engineer is often the person who notices that an "internal cleanup" is actually a breaking change for 40 downstream consumers.

## How to apply it

- **Be strict in what you send, tolerant in what you accept.** Clients should ignore unknown fields so you can add new ones safely.
- **Never reuse or repurpose a field.** Add a new one and deprecate the old.
- **Use expand-and-contract** for changes:
  1. *Expand* — add the new field/endpoint alongside the old.
  2. *Migrate* — move consumers over; track who's still on the old.
  3. *Contract* — remove the old once usage hits zero.
- **When you must break, version explicitly.** Common approaches:
  - URL: `/v2/orders` — simple and visible.
  - Header: `Accept: application/vnd.example.v2+json` — cleaner URLs.
  - Date-based: `Api-Version: 2026-06-01` — fine-grained, used by Stripe.
- **Publish a deprecation policy** (e.g., "12 months' notice") and use `Deprecation`/`Sunset` headers.
- **Measure usage** per version and per client so you know who to contact.
- **Use contract tests** or schema checks in CI to catch accidental breaking changes.
- **Version events and messages too** — they are APIs.

## Example

An API returns `{ "name": "Ada Lovelace" }`. The team wants separate first and last names.

**Breaking approach:** replace `name` with `firstName` and `lastName`. Every client that reads `name` breaks.

**Evolution approach:** return all three fields. Mark `name` deprecated in the docs and the schema. Watch usage of `name` drop as clients update; contact the stragglers. After the deprecation window, remove it — or keep it forever if it's cheap. No client ever broke.

## Common traps

- **Versioning every change.** Ten versions to maintain is far worse than additive evolution.
- **"It's internal, so it's fine."** Internal consumers break too — and are often harder to find.
- **Hidden breaking changes:** stricter validation, changed sort order, new required headers, different error codes.
- **No usage data**, so you can never safely remove anything.
- **Exhaustive enum handling** in clients that crashes on new values. Document that enums may grow.

## When it doesn't apply

If you control every client and deploy them together (e.g., a backend used only by one web app shipped in the same release), you can change the API in lockstep. Even then, rolling deploys mean old and new versions briefly coexist, so additive changes remain the safer habit.

## Related

- [[event-driven-architecture]] — event schemas need the same compatibility discipline.
- [[coupling-and-cohesion]] — an API is the deliberate coupling point between systems.
- [[feature-flags]] — can gate new API behavior during migration.
- [[architecture-decision-records]] — record versioning policy and major breaking changes.
