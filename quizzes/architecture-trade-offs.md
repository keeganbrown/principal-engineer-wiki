# Quiz: Evaluating Architecture Trade-offs

## Two senior engineers have argued for a week about adding an event bus. What usually breaks the stalemate?

- [x] Ranking which qualities matter most, with the people who own the outcome.
- [ ] Building a weighted scoring matrix and choosing whatever scores highest.
- [ ] Letting the engineer with the most experience of event buses decide.
- [ ] Adopting whatever design the largest companies in the industry use.

**Why:** Such arguments are often about values in disguise: each engineer ranks flexibility and simplicity differently. Naming the ranking turns a stalemate into a decision. Scoring matrices give false precision, and fashion skips the question of fit. See [[architecture-trade-offs]].

## A design review compares only one proposed option against the current problem. What is missing?

- [x] A second real option, including keeping the current design.
- [ ] A longer list of the proposed option's benefits and features.
- [ ] A vendor benchmark showing how the option performs at scale.
- [ ] A vote among the team on whether they like the proposal.

**Why:** With one candidate you're justifying a decision, not making one. Compare at least two real options, and the current design, maybe improved, is always one of them. See [[architecture-trade-offs]].

## A team must pick a logging library, and both candidates are easy to swap later. Should they run a full trade-off analysis?

- [x] No; pick one, try it, and switch if it turns out wrong.
- [ ] Yes; every architecture choice deserves a ranked comparison.
- [ ] Yes, and record a weighted score for each library in an ADR.
- [ ] No; ask each engineer to use whichever library they prefer.

**Why:** For choices that are cheap to undo, the analysis costs more than a mistake. Save the full comparison for decisions that lock you in. Letting each engineer choose adds up, though: many cheap choices made differently become one org-wide migration later. See [[architecture-trade-offs]] and [[reversible-decisions]].

## A team chose a modular monolith over services last year. An engineer wants to reopen it, though team count and traffic are unchanged. What should happen?

- [x] The decision stands, since the conditions in its record haven't changed.
- [ ] Reopen it, since architecture decisions should be revisited every year.
- [ ] Reopen it, since anyone who disagrees should get a fresh debate.
- [ ] Switch to services, since the team has grown more experienced now.

**Why:** Writing down what would have to be true for each option to win gives you a revisit trigger. If the conditions haven't changed, point at the architecture decision record rather than re-arguing settled trade-offs. See [[architecture-trade-offs]] and [[architecture-decision-records]].
