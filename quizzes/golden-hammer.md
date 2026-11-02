# Quiz: Golden Hammer

## A design doc's first section is "Graph database setup", and the requirements are in an appendix. What's the warning sign?

- [x] The tool was chosen before the problem was described.
- [ ] The team hasn't run a graph database in production before.
- [ ] The setup section is too short to cover operations.
- [ ] Graph databases are a poor fit for most product data.

**Why:** Write the problem down (access pattern, scale, latency) before naming any product. An unfamiliar tool is a cost to weigh, but it isn't this sign. See [[golden-hammer]].

## Recommendations are computed nightly, looked up by product ID, and may be a day stale. What fits?

- [x] A nightly batch job that writes to a table in the existing database.
- [ ] A new graph database, since purchases between users form a graph.
- [ ] A real-time streaming system that updates recommendations on every purchase.
- [ ] A machine learning platform running on its own cluster.

**Why:** Key lookups on precomputed results are something any database handles well. The graph need belongs to a later fraud project. See [[golden-hammer]].

## A small team uses Postgres for queues, search, and caching. Is that a golden hammer?

- [x] Not yet; it becomes one when workarounds cost more than a fitting tool.
- [ ] Not yet; it becomes one when the team grows past about ten engineers.
- [ ] Yes; each of those jobs deserves its own specialized tool from the start.
- [ ] Yes, because Postgres was never designed to run queues or search.

**Why:** One well-understood tool can beat four half-understood ones. The antipattern is choosing without looking at the problem, not reuse itself. See [[golden-hammer]] and [[kiss]].
