---
title: CQRS — Command Query Responsibility Segregation
category: architecture
summary: Use separate models for changing data (commands) and reading data (queries), so each can be optimized for its own job when they pull in different directions.
tags: [architecture, data, performance]
---

# CQRS — Command Query Responsibility Segregation

> **In one sentence:** Use separate models for changing data (commands) and reading data (queries), so each can be optimized for its own job when they pull in different directions.

## The idea

Most apps use one model for everything: the same `Order` class and table handles both "place an order" and "show me my order history page." That works until reads and writes start needing very different things.

- **Writes (commands)** need to enforce business rules and stay consistent: "you can't ship an order that hasn't been paid."
- **Reads (queries)** need to be fast and shaped for screens: "show the last 20 orders with product names, thumbnails, and shipping status."

CQRS, described by Greg Young, splits these into two sides:

```
           ┌─► Command model ──► Write store (normalized, rules enforced)
  User ────┤                           │
           │                     changes / events
           │                           ▼
           └─► Query model  ◄── Read store (denormalized, screen-shaped)
```

The read side is often updated from the write side via events, so it may lag slightly behind.

## Why it matters

- **Each side gets simpler.** The write model focuses purely on rules; the read model is just fast lookups.
- **Performance.** Read views can be pre-joined and cached — no expensive queries at request time.
- **Independent scaling.** Many systems read far more than they write; scale each side separately.
- **Multiple views.** Build several read models (search index, dashboard, mobile feed) from the same writes.

## How to apply it

- Start small: even in one database, separating **command handlers** from **query handlers** in code is a light form of CQRS.
- Introduce a separate read store only when queries are clearly suffering.
- Update read models from **events** or change-data-capture, not by having the write path write to both stores.
- Make read model updates **idempotent** and **rebuildable** — you should be able to replay history to regenerate them.
- Set expectations for **staleness**: how far behind may the read side be? Design the UI accordingly.

## Example

A marketplace's product page needs data from inventory, pricing, reviews, and seller ratings. Assembling it on each request takes 800ms.

With CQRS, each of those services publishes change events. A `ProductPageView` projector listens and maintains one pre-built document per product in a fast key-value store. The page now loads with a single lookup in 10ms. Writes still go through each service's own rules.

## Common traps

- **Applying it everywhere.** CQRS for a simple CRUD form adds two models, sync logic, and eventual consistency for no gain.
- **Confusing CQRS with event sourcing.** They pair well, but are separate ideas. You can do CQRS without storing events as your source of truth.
- **Forgetting read-your-own-writes.** A user who just updated their profile expects to see the change. Handle this, e.g., by reading from the write side right after a change.
- **No rebuild path.** If a read model gets corrupted and you can't regenerate it, you have a serious problem.

## When it doesn't apply

Most systems — and most parts of any system — don't need CQRS. Use it for specific areas where read and write needs genuinely diverge: heavy read traffic, complex reporting, or very different shapes. Keep the rest simple.

## Related

- [[event-driven-architecture]] — the usual mechanism for keeping read models updated.
- [[idempotency]] — projectors must handle duplicate events safely.
- [[kiss]] — the strongest argument against using CQRS where it isn't needed.
- [[separation-of-concerns]] — CQRS separates the concern of deciding from the concern of displaying.
