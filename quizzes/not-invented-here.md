# Quiz: Not Invented Here (NIH)

## An engineer offers to write a job queue in "about a week." What does the estimate usually miss?

- [x] Years of maintenance, on-call, security fixes, and documentation.
- [ ] The time to choose a name for the queue.
- [ ] The cost of the servers it runs on.
- [ ] The time to write the first version's tests.

**Why:** The first version is the cheap part. Price the whole lifetime of owning it. See [[not-invented-here]].

## What should a team almost never build itself?

- [x] Security primitives such as cryptography and password hashing.
- [ ] The parts of the product that make it different from competitors.
- [ ] A 10-line helper function.
- [ ] Internal tools that pay off across hundreds of teams.

**Why:** Homegrown security is where NIH does the most damage. Build your differentiators; adopt the plumbing. See [[not-invented-here]].

## The team moves to a widely used job library behind an adapter. What new cost appears?

- [x] Running Redis, and making jobs idempotent because a job can occasionally run twice.
- [ ] None; adopting a library removes all operational work.
- [ ] Rewriting every job in a new programming language.
- [ ] Paying the original author to maintain the library.

**Why:** Adopting has costs too, and an adapter doesn't hide semantics like delivery guarantees. The swap gets cheaper, not free. See [[not-invented-here]] and [[idempotency]].
