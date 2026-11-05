# Quiz: Reversible Decisions

## For a new notifications service, which decision deserves the most time?

- [x] The event format that ten other teams will subscribe to.
- [ ] The web framework for the service's own small codebase.
- [ ] The name of the service's internal module for templates.
- [ ] The logging library that the service uses internally.

**Why:** Once many teams consume a format, changing it means coordinating with all of them: a one-way door. Framework choice in a small service is a two-way door. See [[reversible-decisions]].

## Which test best separates a one-way door from a two-way door?

- [x] What undoing it would cost a year from now.
- [ ] How much it costs to build the first version today.
- [ ] How many people attended the design review for it.
- [ ] Whether the choice involves a technology that's new to the team.

**Why:** Expensive to build isn't the same as hard to undo. Spend decision effort in proportion to the cost of reversing it later, and notice when a door is closing as more callers depend on it. See [[reversible-decisions]].

## A team treats every choice, from library choices to linters, as a one-way door. What is the likely result?

- [x] Every choice becomes a committee, and progress stalls.
- [ ] Fewer mistakes overall, because every choice gets careful review.
- [ ] Faster delivery, because decisions are made once and rarely revisited.
- [ ] Better morale, since everyone gets a say in every single decision.

**Why:** Over-caution is a trap too. Decide two-way doors quickly and at the lowest level, and save the deliberation for choices that lock you in. See [[reversible-decisions]].

## A team wants an abstraction over every cloud vendor it uses, in case it ever switches. Is that worth it?

- [x] Only for vendors it has a real reason to expect to leave.
- [ ] Yes; every vendor choice is a one-way door, so hedge them all.
- [ ] Yes, because abstractions over vendors make switching free.
- [ ] No; abstractions over vendors never pay off, whatever the vendor.

**Why:** Each hedge is code you carry, and abstractions over a vendor rarely hide every vendor-specific behavior. Buy reversibility only for doors you have a real reason to expect to walk back through. See [[reversible-decisions]] and [[yagni]].
