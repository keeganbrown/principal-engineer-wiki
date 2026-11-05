# Quiz: Big-Bang Rewrite

## Why does a rewrite of an old system so often stall near the end, after its visible features work?

- [x] Old code holds rules nobody wrote down, found one by one.
- [ ] The remaining work is features nobody uses, which teams hesitate to drop.
- [ ] The new framework is slower, so the team spends the time tuning performance.
- [ ] Teams save the bugs the rewrite was meant to fix for the very end.

**Why:** Strange old code is often knowledge: an edge-case fix, a pricing rule, a partner workaround. A rewrite has to rediscover each one, usually in testing or production. See [[big-bang-rewrite]].

## A team wants to run every request through both the old and new engines and compare. When is that safe?

- [x] When the work is a pure calculation with no side effects.
- [ ] When the new engine is faster, so the extra load is small enough to ignore.
- [ ] When customers have agreed to receive a result from each of the two engines.
- [ ] When the old engine is frozen, so its results can no longer change.

**Why:** Computing a quote twice harms nothing; running billing twice charges customers twice. It isn't free: filter rounding and timing noise first, and someone owns the router until the old engine is off. See [[big-bang-rewrite]] and [[strangler-fig]].

## When can a full rewrite be the right call?

- [x] When the system is small, or its platform is shutting down with no incremental path.
- [ ] When the code is ugly and the team would rather work in a newer language.
- [ ] When the new design adds many features that the old one has always lacked.
- [ ] When the old system is more than ten years old and nobody enjoys changing it.

**Why:** Even then, rewrite in slices where you can and plan a reversible cutover. See [[big-bang-rewrite]] and [[strangler-fig]].
