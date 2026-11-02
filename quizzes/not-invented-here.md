# Quiz: Not Invented Here (NIH)

## An engineer offers to write a job queue in "about a week." What does the estimate usually miss?

- [x] Years of maintenance, on-call, security fixes, and docs.
- [ ] The time to wire it into all the services that will need to use it.
- [ ] The cost of the servers it will run on in production.
- [ ] The time to write tests for the first version.

**Why:** The first version is the cheap part. Price the whole lifetime of owning it. See [[not-invented-here]].

## What should a team almost never build itself?

- [x] Security primitives such as cryptography and password hashing.
- [ ] The parts of the product that make it different from competitors.
- [ ] A 10-line helper that a large dependency would otherwise provide.
- [ ] Internal tools that pay off across hundreds of teams.

**Why:** Homegrown security is where NIH does the most damage. Build your differentiators; adopt the plumbing. See [[not-invented-here]].

## A homegrown job queue loses jobs when a deploy kills a worker mid-job. What was it missing?

- [x] A visibility timeout that returns an unfinished job to the queue.
- [ ] Exponential backoff on retries to failing partner services.
- [ ] A bigger worker pool, so fewer jobs run on each worker.
- [ ] A dashboard showing how many jobs are waiting in the queue, so someone notices.

**Why:** A visibility timeout is a lease: it hides a job from other workers while one runs it, and returns it if that worker dies. A widely used library has it, but it means a job can occasionally run twice, so jobs must be idempotent. See [[not-invented-here]] and [[idempotency]].
