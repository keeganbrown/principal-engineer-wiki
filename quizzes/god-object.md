# Quiz: God Object

## How do you find the seams in a 4,800-line `OrderService`?

- [x] Group its methods by the data they use, then extract one group at a time.
- [ ] Split it into classes of about 500 lines each, following the order of the file.
- [ ] Split it by technical layer into controller, logic, and data access.
- [ ] Rewrite it as four separate services and ship them in a single release.

**Why:** Clusters of methods sharing data reveal the jobs hidden inside. Extract each behind the old interface, and set a removal date for the delegating methods, or both paths live forever. See [[god-object]].

## When splitting a god object `OrderService`, why extract its pure `Pricing` calculations first?

- [x] With no I/O, it's the easiest cluster to test and move.
- [ ] It's the largest cluster, so moving it gives the most benefit at once.
- [ ] It has the fewest callers, so moving them over is quick and cheap.
- [ ] It owns the shared `status` field, so the others depend on it moving.

**Why:** Start with the safest extraction. The hard part comes later, when clusters share state like the order's status and you must decide who owns it. See [[god-object]].

## An app's `App` class is large because it wires all the dependencies together, and it makes no decisions. Is it a god object?

- [x] No; it's a composition root, which lists things rather than deciding them.
- [ ] Yes; its size alone shows that it has taken on too many responsibilities.
- [ ] Yes; it should be split into one factory class for each dependency.
- [ ] No, but only while the app is small; in a large app the same class would be one.

**Why:** A composition root is fine at any size. Size combined with many reasons to change is the problem, not size alone. See [[god-object]] and [[hexagonal-architecture]].
