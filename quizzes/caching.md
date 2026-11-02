# Quiz: Caching

## A product page is cached in Redis. Which data should still be read live?

- [x] Price and stock, because a stale value is a legal and trust problem.
- [ ] Product descriptions, because they change most often.
- [ ] Product images, because they are large.
- [ ] Nothing; the TTL keeps everything fresh enough.

**Why:** Decide how stale is acceptable per piece of data. Some values must come from the source. See [[caching]].

## Why add random jitter to cache TTLs?

- [x] So many entries don't expire at once and stampede the database.
- [ ] So each user sees a slightly different version of the page.
- [ ] So the cache uses less memory over time.
- [ ] So entries expire sooner after an edit.

**Why:** Entries that expire together all miss together. Jitter spreads expiries out to prevent stampedes. See [[caching]].

## A bulk import updates 10,000 products directly in the database. What goes wrong?

- [x] It bypasses the code that deletes cache entries, so stale data lingers until the TTL expires.
- [ ] The cache refreshes itself instantly because Redis watches the database.
- [ ] The database rejects the import while cache entries exist.
- [ ] Nothing, because cache-aside always reads from the database.

**Why:** Invalidation tied to one code path misses writes from other paths. The TTL is the backstop. See [[caching]].
