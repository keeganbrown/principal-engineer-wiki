---
title: Reversible Decisions (One-Way and Two-Way Doors)
category: principles
summary: Spend decision effort in proportion to how hard a choice is to undo — move fast on reversible decisions, and slow down for the few that lock you in.
tags: [decision-making, judgment, staff-plus]
---

# Reversible Decisions (One-Way and Two-Way Doors)

> **In one sentence:** Spend decision effort in proportion to how hard a choice is to undo — move fast on reversible decisions, and slow down for the few that lock you in.

## The idea

Picture every decision as a door.

- A **two-way door** can be walked back through. If you don't like what's on the other side, you return. Choosing a logging library, a module's internal structure, or a feature's first design are usually two-way doors.
- A **one-way door** locks behind you. Undoing it is very expensive or impossible. A public API used by partners, a database that will hold billions of rows, a data format written to customer devices, a security model — these are often one-way doors.

Most decisions are two-way doors. The mistake teams make is treating them all the same: either agonizing over everything (slow), or rushing everything (reckless).

The framing comes from Jeff Bezos's 2015 Amazon shareholder letter, which called them Type 1 and Type 2 decisions.

## Why it matters

Decision speed is a large part of engineering speed. A team that spends three weeks debating a reversible choice has lost three weeks for nothing — they could have tried one option and learned. A team that rushes an irreversible choice may spend years living with it.

Telling the two apart is a core principal-engineer skill. It's often the most useful thing you can say in a design review: "This part is a two-way door — let's just pick one. *This* part is a one-way door — let's slow down."

## How to apply it

- **Ask: "What would it cost to undo this in a year?"** Think about data migrations, consumers you don't control, contracts, and the people who'd have to coordinate.
- **Look for the one-way parts inside a two-way decision.** Choosing a queue technology is reversible; the message format other teams build on may not be.
- **Make one-way doors two-way where you can.** Put a thin interface in front of a vendor. Version a data format from day one. Start with an internal API before publishing it externally. Use [[feature-flags]] to ship gradually.
- **For two-way doors: decide quickly, at the lowest level.** Let the person closest to the work choose. Set a short timebox.
- **For one-way doors: invest.** Write a [[design-docs|design doc]], consider alternatives, prototype, get review from the people affected, and record the decision in an [[architecture-decision-records|ADR (architecture decision record)]].
- **Notice when a door is closing.** Reversible decisions often become irreversible gradually — as more data, more callers, or more teams depend on them. Revisit before that happens.

## Example

A team is building a new notifications service. In the design review:

- **Which web framework?** Two-way door. The service is small; it could be rewritten in a week. Decision: use what the team knows. Five minutes.
- **Database choice?** Mostly two-way at first — but it gets harder to change as data grows. Decision: start with the company's standard Postgres, keep data access behind one module.
- **The event format other teams will subscribe to?** One-way door — once ten teams consume it, changes need coordinating across all of them. Decision: spend a week on it, review it with two consuming teams, version it from day one.

The review takes an hour instead of a week, and the effort goes where it matters.

## Common traps

- **Everything is a one-way door.** Fear of mistakes turns every choice into a committee.
- **Nothing is a one-way door.** "We can always change it later" — while ten teams start depending on it.
- **Ignoring social irreversibility.** A reorg, a public promise, or a hiring decision can be harder to undo than any code.
- **Confusing "expensive to build" with "hard to undo."** A big project can still be easy to abandon; a tiny API decision can be permanent.

## When it doesn't apply

In a crisis, even one-way decisions sometimes have to be made fast, with whatever information you have. And very early in a product's life, almost everything is a two-way door because nothing depends on it yet — the framing becomes more important as the system and organization grow.

## Related

- [[yagni]] — build only what you need, *except* where a one-way door makes the cost of waiting high.
- [[design-docs]] — the right tool for one-way doors.
- [[architecture-decision-records]] — record one-way decisions so the reasoning outlives the people.
- [[api-versioning]] — published APIs are a classic one-way door.
- [[influencing-without-authority]] — spend your credibility on one-way doors, not two-way ones.
