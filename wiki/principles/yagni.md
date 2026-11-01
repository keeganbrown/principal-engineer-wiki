---
title: You Aren't Gonna Need It (YAGNI)
category: principles
summary: Don't build features or flexibility until you actually need them, because guesses about the future are often wrong and always cost something now.
tags: [simplicity, design, agile]
---

# You Aren't Gonna Need It (YAGNI)

> **In one sentence:** Don't build features or flexibility until you actually need them, because guesses about the future are often wrong and always cost something now.

## The idea

Engineers love to prepare for the future: "Let's make this configurable in case…", "Let's add a plugin system so later…". YAGNI says to stop. Build what today's requirement needs, and trust that you can add more when a real need shows up.

It works because good tests and clean code make *later* changes cheap — so there's little reason to pay for them *now*.

The phrase comes from Extreme Programming (XP), an agile method from the late 1990s.

## Why it matters

Martin Fowler describes four costs of building a speculative feature:

- **Even if the guess is right**, you pay:
  1. **Cost of delay** — what users need today ships later.
  2. **Cost of carry** — every change until the feature is used must work around the extra code.
- **If the guess is wrong** (which is common), you also pay:
  3. **Cost of build** — the time spent building it was wasted.
  4. **Cost of repair** — you must remove it, or bend everything else around the wrong design.

## How to apply it

- **Ask for the concrete, current requirement.** If there isn't one, leave it out.
- **Write code that's easy to change, not code that predicts change.** A plain function with good tests is easy to change; an interface with one implementation and three empty extension points is a prediction.
- **Park ideas outside the code.** Put them in a backlog or a design doc.
- **Keep good tests.** They are what make deferring decisions safe.
- **When the need arrives, refactor first,** then add the feature.

## Example

You're building export-to-CSV. A teammate suggests a generic `Exporter` interface with pluggable formats (CSV, JSON, XML, Parquet).

**YAGNI response:** write an `export_csv(rows)` function with tests. Six months later, a customer asks for JSON. Now you have two real formats and can see what they share, so you can design an abstraction that actually fits — and you never wasted time on XML or Parquet, which nobody asked for. (When to extract that abstraction is covered in [[dry|the rule of three]].)

## Common traps

- **Using YAGNI to skip quality.** Tests, error handling, security, and readable code are needed *now*. YAGNI is about features and flexibility, not craftsmanship.
- **Ignoring known, committed requirements.** If the contract says multi-region in Q2, that's not speculation.
- **Painting yourself into a corner.** YAGNI assumes change stays cheap. Don't make decisions that are expensive to reverse (see below).

## When it doesn't apply

YAGNI weakens wherever later change is expensive, no matter how good your tests are:

- **One-way doors** — public API shapes, database schemas with lots of data, security models, and data formats shared with partners are hard to undo. Spend more thought up front. See [[reversible-decisions]].
- **Team boundaries** — anything other teams build on is costly to change later because of coordination, not code quality. Ten consumers means ten migrations.

A principal engineer's job is often to tell the difference: most decisions are two-way doors where YAGNI applies; a few are one-way doors that deserve care.

## Related

- [[kiss]] — keep the solution simple; YAGNI keeps the *scope* simple.
- [[dry]] — owns the question of *when* to extract an abstraction.
- [[reversible-decisions]] — where YAGNI stops applying.
- [[api-versioning]] — public API shapes are a classic one-way door.
- [[test-driven-development]] — the safety net that makes deferring decisions cheap.
