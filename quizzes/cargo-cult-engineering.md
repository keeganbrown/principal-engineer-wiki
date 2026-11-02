# Quiz: Cargo Cult Engineering

## A 15-person team copies a 2,000-engineer company's split into hundreds of services. What do they get?

- [x] The operating cost, without the coordination problem the split solved.
- [ ] The same delivery speed as the large company, once the split is done.
- [ ] Simpler operations, since each service is small and easy to understand.
- [ ] Fewer incidents overall, since a failure stays inside one service.

**Why:** The visible practice was the output of conditions the copier doesn't have. Find the problem it solved first. See [[cargo-cult-engineering]].

## A 30-person company requires an eight-page design doc for every change. Docs get written after the code, and small changes wait a week. What fits better?

- [x] A short doc only for long, cross-team, or hard-to-undo work.
- [ ] A longer template, so that every doc covers more of the design.
- [ ] Dropping design docs entirely, since most changes here are small.
- [ ] Two senior approvals on every doc, so that nothing slips through.

**Why:** Adopt the principle, then pick the practice that fits your scale. The team checked for a quarter that no undocumented change caused a cross-team problem: a small sample, but enough to shift the burden of proof. See [[cargo-cult-engineering]] and [[design-docs]].

## When is copying a practice without fully understanding it reasonable?

- [x] When it's cheap to try and easy to reverse, like a weekly demo.
- [ ] When it's hard to remove later, but a famous company uses it.
- [ ] When it's expensive to adopt, because the effort shows commitment.
- [ ] Only after a full analysis shows how it will work for your team.

**Why:** For cheap, reversible practices you learn more by doing, and widely tested defaults like version control don't need re-deriving. Save scrutiny for practices that are expensive or hard to remove. See [[cargo-cult-engineering]].
