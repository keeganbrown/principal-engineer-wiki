# Quiz: Golden Hammer

## A design doc opens with "we'll use a graph database" and describes the need later. What's the warning sign?

- [x] The tool was named before the problem was.
- [ ] The doc is too short.
- [ ] The doc doesn't list the team's members.
- [ ] Graph databases are always the wrong choice.

**Why:** Write the problem down — access pattern, scale, latency — before naming any product. See [[golden-hammer]].

## Recommendations are computed nightly and looked up by product ID, a day stale is fine. What fits?

- [x] A nightly batch job writing to a table in the existing database.
- [ ] A new graph database, since purchases form a graph.
- [ ] A real-time streaming system that updates on every purchase.
- [ ] A machine learning platform with its own cluster.

**Why:** Key lookups on precomputed results are something any database handles well. The graph need belongs to a later fraud project. See [[golden-hammer]].

## A small team uses Postgres for queues, search, and caching. Is that a golden hammer?

- [x] Not yet; it becomes one when the workarounds cost more each quarter than a fitting tool would.
- [ ] Yes; each job should always get its own specialized tool.
- [ ] Yes, because Postgres was not designed for queues.
- [ ] No, never; one tool for everything is always simplest.

**Why:** One well-understood tool can beat four half-understood ones. The antipattern is choosing without looking at the problem. See [[golden-hammer]] and [[kiss]].
