# Quiz: Code Review

## Which review comment is most useful?

- [x] "blocking: this loop runs `retryCount - 1` times, so with 1 it never sends. `range(retryCount)`? A test would lock it down."
- [ ] "This is wrong, please fix before merging."
- [ ] "I would have written this differently, but it's fine I guess."
- [ ] "Looks good to me!" on a 2,000-line change after five minutes.

**Why:** A helpful comment names the problem, explains the impact, suggests a fix, and points to a test. Labeling its weight ("blocking") helps too. See [[code-review]].

## Pull requests on a team wait three days for review. What does the wiki suggest?

- [x] Measure the wait; if it's days, the gate may cost more than it catches — consider ship/show/ask or pairing.
- [ ] Add more required reviewers so problems are caught before merge.
- [ ] Batch changes into larger pull requests so there are fewer to review.
- [ ] Skip review entirely for every change to restore speed.

**Why:** Review is a policy choice with a cost. Ship/show/ask, small changes, and fast responses keep the gate worth having. See [[code-review]].

## What is the main value of code review, beyond catching bugs?

- [x] Spreading knowledge of the system and keeping the codebase consistent.
- [ ] Giving managers a record of who wrote which lines.
- [ ] Ensuring every change gets a second approval for audits.
- [ ] Letting senior engineers block changes they dislike.

**Why:** Reviews spread knowledge, keep code consistent, and teach in both directions. Gatekeeping is a listed trap. See [[code-review]].
