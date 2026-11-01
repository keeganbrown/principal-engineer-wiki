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

Breaking changes are among the most expensive mistakes in software because their cost lands on other people, often outside your control. A principal engineer is often the person who notices that an "internal cleanup" is actually a breaking change for 40 downstream consumers. A published API is a classic [[reversible-decisions|one-way door]].

## How to apply it

- **Make clients tolerant readers.** Clients should ignore fields they don't recognize, so you can add new ones safely. (Martin Fowler calls this the *Tolerant Reader* pattern.)
- **Make servers strict from day one.** Validate input strictly. Anything you tolerate becomes behavior someone depends on, and tightening it later is a breaking change. This is why the old robustness principle — "be liberal in what you accept" (Jon Postel) — is now treated with caution; the IETF's RFC 9413 (2023) explains why.
- **Never reuse or repurpose a field.** Add a new one and deprecate the old.
- **Change things with [[expand-and-contract]]:** add the new alongside the old, migrate consumers, then remove the old.
- **When you must break, version explicitly.** Common approaches:
  - URL: `/v2/orders` — simple and visible.
  - Header: `Accept: application/vnd.example.v2+json` — a custom media type that names the version; keeps URLs clean.
  - Date-based: e.g. Stripe's `Stripe-Version: 2024-09-30.acacia` or GitHub's `X-GitHub-Api-Version: 2022-11-28`. Very fine-grained, but it requires a translation layer that converts responses for every past version — worth it mainly for large public APIs.
- **Publish a deprecation policy** (e.g., "12 months' notice"), and use the standard `Deprecation` and `Sunset` response headers.
- **Measure usage** per version and per client, so you know who to contact.
- **Catch accidental breaks in CI** with schema diffs or [[contract-testing|contract tests]].
- **Version events and messages too** — they are APIs.

## Example

An API returns `{ "name": "Ada Lovelace" }`. The team wants separate first and last names.

**Breaking approach:** replace `name` with `firstName` and `lastName`. Every client that reads `name` breaks.

**Evolution approach:** return all three fields. Mark `name` deprecated in the docs and the schema. Watch usage of `name` drop as clients update; contact the stragglers. After the deprecation window, remove it — or keep it forever if it's cheap. No client ever broke.

## Common traps

- **Versioning every change.** Ten versions to maintain is far worse than additive evolution.
- **"It's internal, so it's fine."** Internal consumers break too — and are often harder to find.
- **Hidden breaking changes:** stricter validation, changed sort order, new required headers, different error codes.
- **No usage data,** so you can never safely remove anything.
- **Exhaustive enum handling** in clients that crashes on new values. Document that enums may grow.

## When it doesn't apply

If you control every client and deploy them together (e.g., a backend used only by one web app shipped in the same release), you can change the API in lockstep. Even then, **rolling deploys** — updating servers a few at a time — mean old and new versions briefly coexist, so additive changes remain the safer habit.

## Related

- [[expand-and-contract]] — the step-by-step technique for non-breaking change.
- [[contract-testing]] — tells you when a change would break a consumer.
- [[event-driven-architecture]] — event schemas need the same compatibility discipline.
- [[coupling-and-cohesion]] — an API is the deliberate coupling point between systems.
- [[architecture-decision-records]] — record versioning policy and major breaking changes.
