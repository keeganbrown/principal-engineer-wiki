# Quiz: Load Balancers and Content Delivery Networks (CDNs)

## A news site caches article pages at the CDN for 60 seconds. What's the trade-off?

- [x] A correction can take up to a minute to appear worldwide unless the page is purged.
- [ ] Every reader sees a different version of the page.
- [ ] The origin servers must handle every request anyway.
- [ ] Images can no longer be cached for long periods.

**Why:** Caching dynamic pages trades freshness for load. The team added an instant purge for corrections. See [[load-balancers-and-cdns]].

## What makes a health check too deep?

- [x] It checks every dependency, so one slow database marks every server unhealthy at once.
- [ ] It runs more often than once a minute.
- [ ] It returns a JSON body instead of plain text.
- [ ] It runs on a separate port from user traffic.

**Why:** Health checks should be meaningful but not cascade a shared dependency's failure into removing every server. See [[load-balancers-and-cdns]].

## How do static assets get long CDN cache lifetimes safely?

- [x] Hashed file names, so a new version gets a new URL.
- [ ] Short TTLs of a few seconds on every file.
- [ ] Sticky sessions that pin users to one server.
- [ ] Purging the whole CDN on every deploy.

**Why:** With content hashes in file names, old URLs never change meaning, so they can be cached for a year. See [[load-balancers-and-cdns]].
