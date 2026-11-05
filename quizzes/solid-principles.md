# Quiz: SOLID Principles

## A `ReadOnlyFile` subclass throws "not supported" when its parent's `write` method is called. Which principle is broken?

- [x] Liskov substitution: a subtype must work wherever its parent does.
- [ ] Single responsibility: a class should have only one reason to change.
- [ ] Dependency inversion: high-level logic should depend on abstractions.
- [ ] Open/closed: add behavior by adding code rather than by editing it.

**Why:** Callers that hold a file expect `write` to work, and the subtype breaks that promise. If a subclass throws for an inherited method, the hierarchy is wrong; prefer composition. See [[solid-principles]].

## A function checks whether a token has expired. How does dependency inversion make it easy to test?

- [x] The rule declares a `Clock` it needs, and tests pass a fixed one.
- [ ] The rule reads the system clock, and tests change the machine's time.
- [ ] The rule caches the current time at startup, so the tests run fast.
- [ ] The rule gets the time from a global variable that tests overwrite.

**Why:** Business logic declares what it needs; production passes the real clock and tests pass a fixed one, so tests are deterministic. Ports in hexagonal architecture are the same idea at system scale. See [[solid-principles]] and [[hexagonal-architecture]].

## A code base has one `switch` on payment type, in one place. Should you replace it with polymorphism?

- [x] Not yet; a single switch in one place is often simplest.
- [ ] Yes; the open/closed principle forbids switch statements.
- [ ] Yes, and add an interface for each payment type now.
- [ ] Yes, so the next payment type can be added without editing it.

**Why:** Replace a switch when the same one repeats in several places, so new cases become additions. Use SOLID to diagnose pain you have, not as a checklist. See [[solid-principles]].
