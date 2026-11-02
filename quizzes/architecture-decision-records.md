# Quiz: Architecture Decision Records (ADRs)

## An old ADR chose synchronous calls, and the team now moves to events. What should they do with the old ADR?

- [x] Write a new ADR and mark the old one as superseded by it.
- [ ] Edit the old ADR so it describes the new decision.
- [ ] Delete the old ADR, since it no longer reflects the system.
- [ ] Leave the old ADR as is and record the change in a chat thread.

**Why:** ADRs are a history of reasoning. Supersede rather than edit, so future readers can see what changed and why. See [[architecture-decision-records]].

## Which part of an ADR is most often skipped and most missed later?

- [x] The rejected options and why they lost.
- [ ] The ADR's number and title.
- [ ] The date the ADR was written.
- [ ] The name of the person who typed it up.

**Why:** Without the rejected options, the next team re-proposes them. "Skipping rejected options" is a listed trap. See [[architecture-decision-records]].

## Which decision most clearly deserves an ADR?

- [x] Moving order fulfillment from synchronous calls to a queue.
- [ ] Renaming a local variable in the checkout module.
- [ ] Picking a small date-formatting library inside one module.
- [ ] Choosing the color of the internal dashboard header.

**Why:** A good test: would a new teammate in a year plausibly ask *why*? Small, easily reversed choices don't need one. See [[architecture-decision-records]].
