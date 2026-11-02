# Quiz: Domain-Driven Design (DDD)

## Underwriting, billing, and claims all add columns to one `Policy` table. What does DDD suggest?

- [x] Separate bounded contexts, each with its own model of a policy, linked by events and a shared ID.
- [ ] A single canonical enterprise model that all three teams must agree on.
- [ ] More columns with team prefixes so nobody overwrites each other.
- [ ] One team owns the table and the others ask it for every change.

**Why:** The same word means different things in different contexts. Splitting the model lets each team ship independently, though agreeing who owns shared fields is the hard part. See [[domain-driven-design]].

## What is a sign that you've crossed a bounded-context boundary?

- [x] The same word starts meaning something different to the people using it.
- [ ] The code switches from one programming language to another.
- [ ] A different database technology is used.
- [ ] A function grows longer than one screen.

**Why:** Look for language shifts. Drawing contexts around technology is a listed trap. See [[domain-driven-design]].

## For a simple CRUD app with little business logic, what part of DDD is still worth using?

- [x] The strategic ideas: shared language and clear boundaries.
- [ ] The full tactical toolkit: aggregates, repositories, and value objects.
- [ ] None of it; DDD only applies to large enterprises.
- [ ] Only the event-sourcing patterns.

**Why:** Strategic design is cheap and useful almost everywhere. Tactical patterns pay off only where the rules are genuinely complex. See [[domain-driven-design]].
