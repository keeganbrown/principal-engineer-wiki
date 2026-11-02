# Quiz: Domain-Driven Design

## Underwriting, billing, and claims all add columns to one `Policy` table. What does DDD suggest?

- [x] Give each team its own model of a policy, linked by a shared ID.
- [ ] One canonical enterprise model of a policy that all three teams agree on.
- [ ] More columns with team prefixes, so nobody overwrites anyone else's fields.
- [ ] One team owns the table, and the others ask that team for every change.

**Why:** The same word means different things in different contexts, so each bounded context keeps its own model. That lets each team ship independently, though agreeing who owns shared fields is the hard part. See [[domain-driven-design]].

## What signals that you've crossed into a different bounded context?

- [x] A shared word starts meaning something else to its users.
- [ ] The code switches from one programming language to another one.
- [ ] A different database technology stores the data from here on.
- [ ] A module grows past the size one team can comfortably own.

**Why:** Look for language shifts. Drawing contexts around technology splits things that share a language. See [[domain-driven-design]].

## For a simple create-read-update-delete (CRUD) app with little business logic, what part of DDD is still worth using?

- [x] The strategic ideas: shared language and clear boundaries.
- [ ] The full tactical toolkit of aggregates, repositories, and value objects.
- [ ] None of it, since DDD only applies to large enterprise systems.
- [ ] Only aggregates, so the data stays consistent across tables.

**Why:** Strategic design is cheap and useful almost everywhere. Tactical patterns pay off only where the rules are genuinely complex. See [[domain-driven-design]].
