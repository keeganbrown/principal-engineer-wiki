# Quiz: Feedback Loops for Agents

## A service's tests take 35 minutes and fail randomly one run in ten. Agents struggle. What helps most?

- [x] A fast unit suite, with flaky tests quarantined and their causes fixed.
- [ ] A larger model, and a longer timeout so the slow suite can finish.
- [ ] Longer prompts that explain which test failures the agent can ignore.
- [ ] Letting agents skip the tests and relying on human review instead.

**Why:** A flaky test makes the agent "fix" code that wasn't broken. Fast, trustworthy checks let it fix its own mistakes. It cost the team two engineers for two weeks, so start where agents work most. See [[feedback-loops-for-agents]].

## Why is it risky for an agent to write both the code and the only tests for it?

- [x] The tests can share the code's misunderstanding.
- [ ] Agents write tests in a style humans can't review.
- [ ] Agent-written tests always run much more slowly.
- [ ] Agent-written tests can't be checked into the repository.

**Why:** Green checks then prove little. Start from tests a human wrote or reviewed, and review test changes closely. See [[feedback-loops-for-agents]] and [[test-driven-development]].

## What makes an error message useful to an agent?

- [x] It says what failed and where, for a reader with no context.
- [ ] It's as short as possible, ideally just a numeric error code.
- [ ] It includes the full stack trace of every running thread.
- [ ] It uses the team's internal shorthand, so it stays brief.

**Why:** "Expected Cents, got float in `refund()`" lets an agent fix the bug; "AssertionError" makes it guess. Clear messages help humans too. See [[feedback-loops-for-agents]].

## A team wants an unattended agent run, nightly, until a migration task is done. What must the run have first?

- [x] A stop condition a machine can check, a spending cap, and a human handoff.
- [ ] A prompt telling the agent to stop running once it believes it's finished.
- [ ] Production credentials, so it can verify each step against live data.
- [ ] A longer test timeout, so slow checks never halt the run partway.

**Why:** Unattended agent runs need a finish line a machine can check, a spending cap, a record of progress, and a point where a human takes over, and they belong in a sandbox. A loose stop condition burns budget repeating the same failure. See [[feedback-loops-for-agents]] and [[agent-guardrails]].

## A team wants a nightly unattended agent run to iterate on a visual redesign that has no automated checks. Should they set it up?

- [x] Not yet; with nothing a machine can check, keep agents to drafts.
- [ ] Yes, since the agent can judge for itself when the design looks done.
- [ ] Yes, as long as it runs in a sandbox with a spending cap on it.
- [ ] Yes, once the prompt describes the finished design in great detail.

**Why:** No checkable stop condition, no unattended run. Work like visual design has no fast automated check, so keep agents to drafts and exploration with a human in the loop. A sandbox limits the damage but doesn't tell the run when to stop. See [[feedback-loops-for-agents]].
