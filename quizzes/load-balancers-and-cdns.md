# Quiz: Load Balancers and Content Delivery Networks (CDNs)

## A news site caches article pages at the CDN for 60 seconds. What's the trade-off?

- [x] A correction can take up to a minute to appear everywhere.
- [ ] Readers abroad still wait several seconds for each article page.
- [ ] The origin servers still have to handle every single request.
- [ ] Images can no longer be cached for long periods at the edge.

**Why:** Caching dynamic pages trades freshness for load. The team added an instant purge for corrections, but purges are rate-limited, so mass corrections still wait out the window. See [[load-balancers-and-cdns]].

## Which health check is too deep?

- [x] One that fails whenever the optional recommendations service is slow.
- [ ] One that confirms the server can reach the database it needs.
- [ ] One that returns OK without checking the database at all.
- [ ] One that runs on a separate port from user traffic.

**Why:** Check what the server needs to do its job, but not every downstream dependency, or one slow dependency marks every server unhealthy at once. Returning OK with the database unreachable is the opposite mistake: too shallow. See [[load-balancers-and-cdns]].

## How do static assets get long CDN cache lifetimes safely?

- [x] Hashed file names, so a new version gets a new URL.
- [ ] Cache lifetimes of a few seconds on every static file.
- [ ] Sticky sessions that pin each user to one server.
- [ ] Purging the whole CDN on every deploy, automatically.

**Why:** With content hashes in file names, old URLs never change meaning, so they can be cached for a year and never need a purge. See [[load-balancers-and-cdns]].
