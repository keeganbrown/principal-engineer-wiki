# Quiz: Architecture Decision Records

## An old architecture decision record (ADR) chose synchronous calls, and the team now moves to events. What should they do with it?

- [x] Write a new ADR and mark the old one as superseded by it.
- [ ] Edit the old ADR so that it describes the new decision instead.
- [ ] Delete the old ADR, since it no longer reflects the running system.
- [ ] Leave the old ADR alone and note the change in a chat thread.

**Why:** ADRs are a history of reasoning. Supersede rather than edit, so future readers can see what changed and why. See [[architecture-decision-records]].

## Which part of an architecture decision record is often the most valuable, and tempting to skip?

- [x] The rejected options and why they lost.
- [ ] The status line: proposed, accepted, or superseded.
- [ ] A short summary of the decision itself.
- [ ] The context that led to the decision.

**Why:** Code shows what was built; the record explains why, and the alternatives are often the part readers need most. See [[architecture-decision-records]].

## Which decision most clearly deserves an architecture decision record?

- [x] Moving order fulfillment from synchronous calls to a queue.
- [ ] Adding an index to speed up one slow query in the reports page.
- [ ] Picking a small date-formatting library used inside one module.
- [ ] Renaming the checkout module's main class to a clearer name.

**Why:** A good test: would a new teammate in a year plausibly ask why? Small, easily reversed choices don't need one. See [[architecture-decision-records]].
