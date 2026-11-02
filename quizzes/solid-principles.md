# Quiz: SOLID Principles

## A `Square` subclass throws "not supported" when its parent's `setWidth` is called. Which principle is broken?

- [x] Liskov substitution: a subtype must work anywhere its parent is expected.
- [ ] Single responsibility: a class should have one reason to change.
- [ ] Interface segregation: clients shouldn't depend on methods they don't use.
- [ ] Open/closed: add behavior by adding code, not editing it.

**Why:** "Not supported" errors in a subtype are the classic warning sign that substitution fails. See [[solid-principles]].

## A function checks whether a token has expired. How does dependency inversion make it easy to test?

- [x] The rule declares a `Clock` it needs, and tests pass a fixed clock.
- [ ] The rule reads the system clock directly, and tests change the machine's time.
- [ ] The rule caches the current time at startup, so tests run fast.
- [ ] The rule gets the time from a global variable that tests overwrite.

**Why:** Business logic declares what it needs; production passes the real clock and tests pass a fixed one. Tests become deterministic and fast. See [[solid-principles]].

## How should SOLID be used, according to the wiki?

- [x] As heuristics to diagnose pain you have, not a checklist to prevent pain you don't.
- [ ] As a mandatory review checklist applied to every class in every pull request.
- [ ] Only in functional code, since it was designed for languages without objects.
- [ ] As a reason to put an interface in front of every class by default.

**Why:** "An interface for everything" and checklist reviews are listed traps. In small programs the indirection can cost more than it saves. See [[solid-principles]].
