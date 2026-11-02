# Quiz: Feedback Loops for Agents

## A service's tests take 35 minutes and fail randomly one run in ten. Agents struggle. What helps most?

- [x] A fast unit suite, quarantining flaky tests, and fixing their top causes.
- [ ] A larger, more capable model.
- [ ] Longer prompts explaining which failures to ignore.
- [ ] Letting agents skip tests and relying on human review.

**Why:** Verification, not typing, is the bottleneck. Fast, trustworthy checks let the agent fix its own mistakes. See [[feedback-loops-for-agents]].

## Why is it risky for an agent to write both the code and the only tests for it?

- [x] The tests can share the code's misunderstanding, so green checks prove little.
- [ ] Agents can't write tests in the same language as the code.
- [ ] Tests written by agents always run slower.
- [ ] Agent-written tests can't be checked into the repository.

**Why:** "Trusting green checks too much" is a listed trap. Keep some checks the agent didn't write and can't edit. See [[feedback-loops-for-agents]].

## What makes an error message useful to an agent?

- [x] It's written for a reader with no context: what failed, where, and what to do.
- [ ] It's as short as possible, ideally just an error code.
- [ ] It includes the full stack trace of every thread.
- [ ] It's written in the team's internal shorthand.

**Why:** The agent knows only what the output tells it. The same clear messages help humans too. See [[feedback-loops-for-agents]].
