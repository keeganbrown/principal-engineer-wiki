# Quiz: Code Review

## A loop is written `for attempt in range(1, retryCount)`. Which review comment is most useful?

- [x] "blocking: with retryCount = 1 this never sends. range(retryCount)?"
- [ ] "This loop looks off to me; can you take another look before merging?"
- [ ] "nit: I'd write this loop differently, but it's up to you, really."
- [ ] "LGTM, the logic reads fine to me and all the tests are passing."

**Why:** A helpful comment names the problem, its impact, and a fix, and labels its weight ("blocking"). Asking for a test that locks it down helps too. See [[code-review]].

## Pull requests on your team wait three days for review. What should you do first?

- [x] Measure the wait and fix response time; then consider ship/show/ask.
- [ ] Add more required reviewers, so problems are caught before merge.
- [ ] Batch changes into larger pull requests, so there are fewer to review.
- [ ] Drop review for any change under 50 lines, to restore speed at once.

**Why:** Respond within a few working hours. If the gate still costs more than it catches, a high-trust team can ship trivial changes, show low-risk ones after merging, and ask only on risky code. See [[code-review]].

## What is the main value of code review, beyond catching bugs?

- [x] Spreading knowledge of the system and keeping code consistent.
- [ ] Giving managers a record of who wrote which lines of the code.
- [ ] Catching style issues that an automatic formatter would miss.
- [ ] Letting senior engineers block changes they personally dislike.

**Why:** Reviews spread knowledge, keep code consistent, and teach in both directions. Using review as gatekeeping wastes that. See [[code-review]].
