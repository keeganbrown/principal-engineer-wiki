# Quiz: Reversible Decisions (One-Way and Two-Way Doors)

## For a new notifications service, which decision deserves the most time?

- [x] The event format that ten other teams will subscribe to.
- [ ] The web framework for the service's own small codebase.
- [ ] The name of the service's internal module for templates.
- [ ] The logging library used inside the service.

**Why:** Once many teams consume a format, changing it means coordinating with all of them — a one-way door. Framework choice in a small service is a two-way door. See [[reversible-decisions]].

## Which test best separates a one-way door from a two-way door?

- [x] Asking what undoing it would cost a year from now.
- [ ] Asking how much it costs to build the first version.
- [ ] Asking how many people attended the design review.
- [ ] Asking whether the choice uses a new technology.

**Why:** Expensive to build isn't the same as hard to undo. Spend decision effort in proportion to the cost of reversing it later. See [[reversible-decisions]].

## A team treats every choice, from library names to linters, as a one-way door. What is the likely result?

- [x] Decisions slow to a crawl, and the few truly important ones get no extra attention.
- [ ] Fewer mistakes overall, because every choice gets careful review.
- [ ] Faster delivery, because decisions are made once and never revisited.
- [ ] Better morale, since everyone gets a say in every decision.

**Why:** Over-caution is a trap too. Decide two-way doors quickly and at the lowest level, and save the deliberation for choices that lock you in. See [[reversible-decisions]].
