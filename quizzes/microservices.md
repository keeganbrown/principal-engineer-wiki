# Quiz: Microservices

## An 80-engineer monolith has weekly deploys that often roll back. What should the team try first?

- [x] Enforce module boundaries inside the monolith.
- [ ] Rewrite it into 40 microservices over the next year.
- [ ] Split it into one service per database table.
- [ ] Freeze all deploys until quality improves.

**Why:** Module boundaries alone took deploys from weekly to several times a week. Extract services only for a reason you can name. See [[microservices]] and [[modular-monolith]].

## Which is a good, nameable reason to extract a service?

- [x] Payments needs compliance isolation and its own deploy cadence.
- [ ] Microservices are the industry standard for modern apps.
- [ ] The team wants to try a new programming language.
- [ ] The module is large and has many files.

**Why:** Independent scaling, isolation, or team autonomy can justify the cost. Fashion and file count can't. See [[microservices]].

## What is a hidden cost of each extracted service?

- [x] Its own deploy pipeline, tracing, dashboards, and on-call rotation.
- [ ] A separate source-code license for each service.
- [ ] A requirement to rewrite all of its tests from scratch.
- [ ] Losing the ability to use a relational database.

**Why:** In the example, the platform work for the extracted services took roughly two engineers full time to build and keep running. See [[microservices]].
