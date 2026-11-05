# Quiz: Caching

## A product page is cached in Redis. Which data should still be read live?

- [x] Price and stock.
- [ ] Product descriptions.
- [ ] Product images.
- [ ] Customer reviews.

**Why:** Decide how stale is acceptable per piece of data. A stale price is a legal and trust problem, and stock at checkout must be current, so both come from the source. See [[caching]].

## One very popular cache entry expires, and hundreds of requests hit the database at once. What prevents this?

- [x] Letting one request refresh it while the others wait or get the stale value.
- [ ] Adding random jitter to the entry's TTL, so it expires at a less busy moment.
- [ ] Shortening the TTL, so the entry is refreshed more often and stays warm.
- [ ] Adding more cache nodes, so the entry is stored in more places.

**Why:** Jitter stops many entries written together from expiring together, but it doesn't help a single hot key. See [[caching]].

## A cache cluster restarts during peak traffic, and the database falls over. What was missing?

- [x] A plan for running with an empty cache.
- [ ] A longer TTL on every cached entry.
- [ ] A second cache in a different region.
- [ ] More memory on each cache node, so fewer entries are evicted.

**Why:** If the database can't survive a cold cache, the cache is quietly carrying capacity. Warm caches before sending traffic, restart nodes gradually, or apply backpressure. See [[caching]] and [[backpressure]].

## Product pages are cached, and the app's edit code deletes the cache entry on save. A bulk import updates 10,000 products directly in the database. What goes wrong?

- [x] It skips the code that deletes cache entries, so stale data stays until the TTL.
- [ ] The cache refreshes itself instantly, because Redis watches the database.
- [ ] The database rejects the import while matching entries still exist in the cache.
- [ ] Nothing; the import's own transaction refreshes the cache.

**Why:** Invalidation tied to one code path misses writes from other paths. Route every write through the same invalidation, and keep the TTL as a backstop. See [[caching]].
