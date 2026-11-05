---
title: Caching
category: technology
summary: Keep copies of expensive results closer to where they're needed so reads get faster and cheaper — and decide up front how stale a copy may be and how it gets refreshed.
tags: [performance, caching, scalability, consistency]
---

# Caching

> **In one sentence:** Keep copies of expensive results closer to where they're needed so reads get faster and cheaper — and decide up front how stale a copy may be and how it gets refreshed.

## The idea

A **cache** is a fast, temporary copy of data whose real home is somewhere slower: a database, another service, a computation. Reading from the cache skips the slow work.

Caches appear at every layer: the browser, a **CDN** (content delivery network — servers around the world that keep copies of your content close to users), an in-memory store like Redis or Memcached, and memory inside your own process.

The catch is that a copy can be out of date. Every cache is a deliberate decision to sometimes serve **stale** data in exchange for speed. The old joke — "there are only two hard things in computer science: cache invalidation and naming things," credited to Phil Karlton — makes the point.

## Why it matters

- **Users feel the speed.** In-process memory reads take nanoseconds and a networked cache well under a millisecond; a database query or remote call takes milliseconds or more.
- **The slow system is protected.** A cache absorbs repeated reads so the database handles only misses and writes.
- **Serving gets cheaper.** Serving popular content from a CDN is far cheaper than serving it from your servers.

Each benefit comes with a new failure mode: stale data, a cold cache after restart, and a *stampede* (also called a thundering herd), when many requests miss at once and all hit the database.

## How to apply it

- **Measure first.** Cache what is both slow *and* read often. Caching a fast query adds complexity for nothing.
- **Give every entry a time-to-live (TTL).** A **TTL** is how long an entry may live before it expires. Even with explicit invalidation, a TTL bounds how long a bug can serve wrong data.
- **Use cache-aside as the default.** Read the cache; on a miss, read the source, store the result, return it. On writes, update the source and delete the cache entry; deleting is safer than updating, because two concurrent writes can leave the cache holding the older value. A reader that fetched the old value just before the write can still store it just after the delete, and the TTL bounds how long it survives.
- **Decide how stale is acceptable, per use.** A product description can be minutes old; a bank balance on the payment screen cannot ([[cap-theorem]]).
- **Prevent stampedes.** When a hot entry expires, hundreds of requests may hit the database at once. Let one request refresh (for example, the one that wins a short lock on the key) while others wait or get the stale value, and add a few random seconds (*jitter*) to each TTL so entries written together don't all expire together.
- **Design for an empty cache.** Caches restart and evict. If the system can't survive a cold cache — at high read volume it often can't — plan for that: warm caches before sending traffic, restart cache nodes gradually, and run the cache as a critical tier with its own capacity planning.
- **Never cache per-user data under a shared key.** Include everything that changes the answer — user, permissions, language — in the cache key.

## Example

A product page makes five database queries and takes 400 milliseconds. During a sale, the database's processors hit 100% and pages time out. The queries are already indexed; the load is simply the same hot products read over and over.

The team caches the assembled product data in Redis with a 5-minute TTL plus up to 30 seconds of random jitter, and deletes the entry whenever the product is edited. Price and stock are *not* cached: the page fetches them live, because a stale price is a legal and customer-trust problem.

Page time drops to 40 milliseconds and database load falls by 80%. The hard part shows up a month later: a bulk import updates 10,000 products directly in the database, bypassing the code that deletes cache entries, and stale descriptions linger for up to five and a half minutes. The TTL limited the damage; the team routes bulk imports through the same invalidation path.

## Common traps

- **Caching to hide a slow query.** If an index would fix it, fix the query first.
- **Invalidation scattered everywhere.** If ten code paths write the data, all ten must invalidate. Centralize writes, or drive invalidation from change-data-capture (CDC) events ([[transactional-outbox]]).
- **Caching errors for too long.** A cached error or empty result turns a brief outage into a long one.
- **Leaking data across users.** Forgetting a component of the cache key is a security bug, not a performance bug.

## When it doesn't apply

Data that must always be current — balances during payment, stock at checkout, permissions — should be read from the source, or cached only with strict invalidation and short TTLs. And data that's rarely re-read gains nothing from a cache except a new way to be wrong.

## Related

- [[cap-theorem]] — staleness is a consistency choice; decide it explicitly.
- [[relational-databases]] — fix queries and add replicas before caching.
- [[load-balancers-and-cdns]] — CDNs are caches at the network edge.
- [[backpressure]] — what to do when a cold cache sends a flood to the database.
- [[observability]] — watch hit rate, latency, and evictions.
