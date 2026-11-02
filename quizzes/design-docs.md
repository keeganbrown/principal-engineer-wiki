# Quiz: Design Docs

## What is the main purpose of a design doc?

- [x] Thinking: finding flaws while they cost a paragraph, not a rewrite.
- [ ] Documentation: a permanent manual for the finished system.
- [ ] Approval: a signature required before engineers may start coding.
- [ ] Estimation: a schedule to hold the team to.

**Why:** Writing turns a vague plan into concrete decisions and lets others spot what you can't. See [[design-docs]].

## A design doc weighs ways to cache pricing results. Finance says prices must update within one minute of a change. Which alternative does that rule out?

- [x] Precomputing every price in a nightly batch job.
- [ ] A local in-memory cache with event-based invalidation.
- [ ] A shared Redis cache cleared on "price changed" events.
- [ ] Reading prices directly from the pricing service.

**Why:** A nightly batch can be up to a day stale. Listing alternatives and reviewing early surfaces requirements engineering didn't know. See [[design-docs]].

## Doc review now routinely takes longer than the work it gates. What should change?

- [x] Shrink the template or the list of reviewers.
- [ ] Require docs only from the most junior engineers.
- [ ] Add a deadline after which docs approve themselves.
- [ ] Drop design docs entirely, since review is too slow.

**Why:** A doc process that outweighs the work has turned into bureaucracy. Keep the thinking, cut the ceremony. See [[design-docs]].

## When should you skip the design doc?

- [x] A small, reversible, well-understood change.
- [ ] Work that crosses team boundaries but is simple to describe.
- [ ] Work that takes more than a couple of weeks to complete.
- [ ] A change that is hard to undo once data has been migrated.

**Why:** Write a doc when work is long, crosses teams, or is hard to undo. Otherwise a pull request description does the job. See [[design-docs]].
