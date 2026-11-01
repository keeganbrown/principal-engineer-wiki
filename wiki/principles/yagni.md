---
title: YAGNI — You Aren't Gonna Need It
category: principles
summary: Don't build features or flexibility until you actually need them, because guesses about the future are usually wrong and always cost something now.
tags: [simplicity, design, agile]
---

# YAGNI — You Aren't Gonna Need It

> **In one sentence:** Don't build features or flexibility until you actually need them, because guesses about the future are usually wrong and always cost something now.

## The idea

Engineers love to prepare for the future: "Let's make this configurable in case…", "Let's add a plugin system so later…". YAGNI says to stop. Build what today's requirement needs, and trust that you can add more when a real need shows up.

The phrase comes from Extreme Programming. It works because good tests and clean code make *later* changes cheap — so there's little reason to pay for them *now*.

## Why it matters

Speculative work has four costs, even if the guess turns out right:

1. **Cost of building it** — time not spent on what users need today.
2. **Cost of delay** — the real feature ships later.
3. **Cost of carrying it** — every future change must work around the extra code.
4. **Cost of being wrong** — most guesses miss, and now you must remove or bend the wrong abstraction.

## How to apply it

- Ask: "Is there a concrete, current requirement for this?" If not, leave it out.
- Prefer the shape of code that's *easy to change* over code that *anticipates* change.
- Write down the idea in a backlog or design doc instead of in the code.
- Keep good tests. They are what make deferring decisions safe.
- When the need arrives, refactor first, then add the feature.

## Example

You're building export-to-CSV. A teammate suggests a generic `Exporter` interface with pluggable formats (CSV, JSON, XML, Parquet).

**YAGNI response:** write a `export_csv(rows)` function. Six months later, a customer asks for JSON. Now you know two real formats, so you can design an abstraction that fits both — and you never wasted time on XML or Parquet, which nobody asked for.

## Common traps

- **Using YAGNI to skip quality.** Tests, error handling, security, and readable code are needed *now*. YAGNI is about features and flexibility, not craftsmanship.
- **Ignoring known, committed requirements.** If the contract says multi-region in Q2, that's not speculation.
- **Painting yourself into a corner.** YAGNI assumes change stays cheap. Don't make decisions that are expensive to reverse (see below).

## When it doesn't apply

Some decisions are hard to undo: public API shapes, database schemas with lots of data, security models, and data formats shared with partners. For these "one-way doors," spend more thought up front. A principal engineer's job is often to tell the difference: most decisions are two-way doors where YAGNI applies; a few are one-way doors that deserve care.

## Related

- [[kiss]] — keep the solution simple; YAGNI keeps the *scope* simple.
- [[dry]] — wait for real repetition before abstracting, for the same reason.
- [[architecture-decision-records]] — a good place to record the ideas you chose not to build yet.
- [[test-driven-development]] — the safety net that makes deferring decisions cheap.
