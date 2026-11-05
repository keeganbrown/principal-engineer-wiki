# Quiz: Microservices

## An 80-engineer monolith has weekly deploys that often roll back. What should the team try first?

- [x] Enforce module boundaries inside the monolith.
- [ ] Rewrite it into 40 microservices over the next year.
- [ ] Split it into one service for each database table.
- [ ] Freeze all deploys until test quality improves.

**Why:** In the example, module boundaries alone took deploys from weekly to several times a week. Extract services only for a reason you can name, and stop extracting if the numbers don't improve. See [[microservices]] and [[modular-monolith]].

## Which is a good, nameable reason to extract a service?

- [x] Payments needs compliance isolation and its own deploy cadence.
- [ ] Microservices are the industry standard for modern applications.
- [ ] The team wants to try a language that's popular this year.
- [ ] The module is large and has more files than any other.

**Why:** Different scaling needs, isolation, or a team blocked by a shared release can justify the cost. Fashion and file count can't. A genuinely different technology need is a rare, costly reason. See [[microservices]].

## What is a hidden cost of each extracted service?

- [x] Its own deploy pipeline, tracing, dashboards, and on-call.
- [ ] Slower function calls between the classes inside the service itself.
- [ ] Rewriting all of its tests from scratch.
- [ ] Losing the ability to use a relational database.

**Why:** Every service needs its own pipeline, monitoring, and on-call; across a few extracted services, that platform work can cost roughly two full-time engineers. See [[microservices]].

## A six-person startup with an early product wants to build on microservices from day one, to be ready for scale. Should it?

- [x] Not yet; a monolith is faster until the domain and team size call for services.
- [ ] Yes; starting with services avoids a painful migration later on.
- [ ] Yes, as long as each service is kept small enough for one person.
- [ ] No; microservices only make sense for companies with thousands of engineers.

**Why:** For a small team and a domain you don't understand well yet, you can't draw good boundaries, and a monolith is almost always faster and safer. See [[microservices]] and [[modular-monolith]].
