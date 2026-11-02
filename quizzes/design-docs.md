# Quiz: Design Docs

## What is the main purpose of a design doc?

- [x] Thinking: finding flaws while they cost a paragraph, not a rewrite.
- [ ] Documentation: a permanent manual for the finished system.
- [ ] Approval: a signature required before engineers may start coding.
- [ ] Estimation: a schedule to hold the team to.

**Why:** Writing turns a vague plan into concrete decisions and lets others spot what you can't. Changing a paragraph costs minutes. See [[design-docs]].

## In review, finance says prices must update within one minute for legal reasons. Which option does that rule out?

- [x] Precomputing prices nightly.
- [ ] A local in-memory cache with event-based invalidation.
- [ ] A shared Redis cache cleared on "price changed" events.
- [ ] Reading prices directly from the pricing service.

**Why:** The nightly batch can be up to a day stale. One comment in review prevented a compliance incident after launch. See [[design-docs]].

## When should you skip the design doc?

- [x] A small, reversible, well-understood change; a good PR description is enough.
- [ ] Work that crosses team boundaries but is simple to describe.
- [ ] Work that takes more than a couple of weeks.
- [ ] A change that is hard to undo once data is migrated.

**Why:** Write a doc when work is long, crosses teams, or is hard to undo. Otherwise a pull request description does the job. See [[design-docs]].
