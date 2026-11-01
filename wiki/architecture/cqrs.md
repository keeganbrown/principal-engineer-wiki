---
title: Command Query Responsibility Segregation (CQRS)
category: architecture
summary: Use separate models for changing data (commands) and reading data (queries), so each can be optimized for its own job when they pull in different directions.
tags: [architecture, data, performance]
---

# Command Query Responsibility Segregation (CQRS)

> **In one sentence:** Use separate models for changing data (commands) and reading data (queries), so each can be optimized for its own job when they pull in different directions.

## The idea

Most apps use one model for everything: the same `Order` class and table handles both "place an order" and "show my order history." That works until reads and writes start needing very different things.

- **Writes (commands)** — a command is *a request to change state*. Writes must enforce business rules and stay consistent: "you can't ship an order that hasn't been paid."
- **Reads (queries)** — must be fast and shaped for screens: "show the last 20 orders with product names, thumbnails, and shipping status."

CQRS splits these into two sides:

```
           ┌─► Command model ──► Write store (normalized, rules enforced)
  User ────┤                           │
           │                     changes / events
           │                           ▼
           └─► Query model  ◄── Read store (denormalized, screen-shaped)
```

The code that listens for changes and updates the read store is called a **projector**. When the read side is updated asynchronously, it lags slightly behind — this is **eventual consistency**.

Greg Young described CQRS around 2010, building on Bertrand Meyer's *command–query separation* principle from 1988.

## Why it matters

- **Each side gets simpler.** The write model enforces rules; the read model serves fast lookups.
- **Performance.** Read views can be pre-joined and cached — no expensive queries at request time.
- **Independent scaling.** Many systems read far more than they write; scale each side separately. Try read replicas and caching first — a separate read model is for when the *shape* of reads differs, not just the volume.
- **Multiple views.** Build several read models (search index, dashboard, mobile feed) from the same writes.

## How to apply it

- **Start small.** Even in one database, separating command handlers from query handlers in code is a light form of CQRS.
- **Keep it in one transaction while you can.** If the read model lives in the same database, update it in the same transaction as the write. That's simplest and stays fully consistent.
- **Use events or CDC once stores are separate.** For a separate read store, update it from events or **change-data-capture (CDC)** — streaming the database's own change log to other systems ([[transactional-outbox]]). Don't have the write path write to both stores directly; if one write fails, they drift apart.
- **Make projectors idempotent and rebuildable.** You should be able to regenerate a read model — by replaying events if you keep them, or by re-projecting from the write store.
- **Set expectations for staleness.** How far behind may the read side be? Design the UI accordingly ([[cap-theorem]] covers the patterns).

## Example

A marketplace's product page needs data from inventory, pricing, reviews, and seller ratings. Assembling it on each request takes 800ms.

Here the write side is four services, and each publishes change events. A `ProductPageView` projector listens and keeps one pre-built document per product in a fast key-value store. The page now loads with a single lookup in 10ms. Writes still go through each service's own rules.

The trade-off: the price or stock level shown on the page can lag by a few seconds. So checkout doesn't trust the page — it re-checks price and stock with the owning services before charging.

## Common traps

- **Applying it everywhere.** CQRS for a simple CRUD (create, read, update, delete) form adds two models, sync logic, and eventual consistency for no gain.
- **Confusing CQRS with event sourcing.** Event sourcing stores the history of events as the source of truth. It pairs well with CQRS, but they're separate ideas.
- **Forgetting read-your-writes.** A user who just updated their profile expects to see the change. Read from the write side right after a change ([[cap-theorem]]).
- **No rebuild path.** If a read model gets corrupted and can't be regenerated, your only fix is a manual data repair.

## When it doesn't apply

Most systems — and most parts of any system — don't need CQRS. Use it for specific areas where read and write needs genuinely diverge: heavy read traffic, complex reporting, or very different shapes. Keep the rest simple.

## Related

- [[event-driven-architecture]] — the usual mechanism for keeping read models updated.
- [[transactional-outbox]] — how change events get out of the write store reliably.
- [[idempotency]] — projectors must handle duplicate events safely.
- [[cap-theorem]] — the consistency trade-off behind stale read models.
- [[kiss]] — the strongest argument against using CQRS where it isn't needed.
