# Quiz: God Object

## How do you find the seams in a 4,800-line `OrderService`?

- [x] Group its methods by the data they use, then extract one cluster at a time.
- [ ] Split it into one class per 500 lines.
- [ ] Split it by technical layer: controller, logic, and data access.
- [ ] Rewrite it as four services in a single release.

**Why:** Clusters of methods sharing data reveal the jobs hidden inside. Extract them one at a time behind the old interface. See [[god-object]].

## Why extract `Pricing` first?

- [x] It's pure calculation with no I/O, so it's the easiest to test and move.
- [ ] It's the largest cluster, so it gives the most benefit at once.
- [ ] Pricing changes least, so nobody will notice.
- [ ] It touches the shared `status` field, so it must go first.

**Why:** Start with the safest extraction. The hard part comes later, when clusters share state like the order's status. See [[god-object]].

## A small app's `App` class is large because it wires all the dependencies together. Is it a god object?

- [x] No; it's a composition root, large because it lists things, not because it decides things.
- [ ] Yes; any class over 500 lines is a god object.
- [ ] Yes; it should be split into one class per dependency.
- [ ] No, but only because the app is small.

**Why:** Size alone isn't the problem. Size combined with many reasons to change is. See [[god-object]].
