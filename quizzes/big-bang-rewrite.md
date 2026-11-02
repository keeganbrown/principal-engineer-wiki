# Quiz: Big-Bang Rewrite

## Nine months into a rewrite, the new quoting engine handles 80% of policies. What's in the other 20%?

- [x] Edge cases like multi-car discounts and broker terms that existed only as `if` statements in the old code.
- [ ] Features nobody uses, which can be dropped.
- [ ] Performance optimizations the new engine doesn't need.
- [ ] Bugs the rewrite was meant to remove.

**Why:** The old system's strange code is often knowledge nobody wrote down. Rewrites rediscover it slowly. See [[big-bang-rewrite]].

## Why could the insurer safely run every quote through both engines?

- [x] A quote is a calculation with no side effects, so computing it twice harms nothing.
- [ ] The new engine was faster, so it added no load.
- [ ] Customers agreed to receive two quotes.
- [ ] The old engine was being frozen anyway.

**Why:** Compare outputs before switching — but only where running both has no side effects. Running two billing systems would charge customers twice. See [[big-bang-rewrite]].

## When can a rewrite be the right call?

- [x] For a small system, or one on a platform being shut down with no incremental path.
- [ ] Whenever the code is ugly and the team dislikes the language.
- [ ] Whenever the new design adds many features the old one lacks.
- [ ] Whenever the old system is more than ten years old.

**Why:** Even then, rewrite in slices where you can and plan a reversible cutover. See [[big-bang-rewrite]] and [[strangler-fig]].
