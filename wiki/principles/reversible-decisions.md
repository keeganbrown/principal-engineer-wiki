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

- **Two-way door** — you can walk back through. If you don't like what's on the other side, you return. A module's internal structure or a feature's first design are usually two-way doors.
- **One-way door** — it locks behind you. Undoing it is very expensive or impossible. A public API used by partners, a database that will hold billions of rows, a data format written to customer devices, and a security model are often one-way doors.

Most decisions are two-way doors. The mistake teams make is treating them all the same: either agonizing over everything (slow), or rushing everything (reckless).

The framing comes from Jeff Bezos's 2015 Amazon shareholder letter, which called one-way doors *Type 1* decisions and two-way doors *Type 2*.

## Why it matters

Decision speed is a large part of engineering speed. A team that spends three weeks debating a reversible choice has lost three weeks for nothing — they could have tried one option and learned. A team that rushes an irreversible choice may spend years living with it.

Telling the two apart is a core principal-engineer skill. It's often the most useful thing you can say in a design review: "This part is a two-way door — let's just pick one. *This* part is a one-way door — let's slow down."

## How to apply it

- **Ask what undoing it would cost in a year.** Think about data migrations, consumers you don't control, contracts, and the people who'd have to coordinate.
- **Look for the one-way parts inside a two-way decision.** Choosing a queue technology is reversible; the message format other teams build on may not be.
- **Make a one-way door two-way only where it pays.** You can version a data format from day one ([[expand-and-contract]] then lets it evolve), start with an internal API before publishing it, or ship gradually behind [[feature-flags]]. But each hedge is code you carry, and abstractions over a vendor rarely hide every vendor-specific behavior. Buy reversibility only for doors you have a real reason to expect to walk back through.
- **Decide two-way doors quickly, at the lowest level.** Let the person closest to the work choose. Set a short timebox.
- **Invest in one-way doors.** Write a [[design-docs|design doc]], consider alternatives, prototype, get review from the people affected, and record the decision in an [[architecture-decision-records|architecture decision record (ADR)]].
- **Notice when a door is closing.** Reversible decisions often become irreversible gradually — as more data, more callers, or more teams depend on them. Revisit before that happens.

## Example

A team is building a new notifications service. In the design review:

- **Which web framework?** Two-way door. The service is small and could be rewritten in a week. Use what the team knows. Five minutes.
- **Which database?** Mostly two-way at first, but harder to change as data grows. Start with the company's standard Postgres ([[relational-databases]]) and keep data access behind one module.
- **What event format will other teams subscribe to?** One-way door — once ten teams consume it, changes need coordinating across all of them. Spend a week on it, review it with two consuming teams, and version it from day one.

Two engineers disagree about the database: one calls it a one-way door. The cost-to-undo question settles most of it — at today's data size, a migration is a week of work. The tech lead decides it's two-way, keeps data access behind one module so a later database swap touches one place, and records the dissent in the ADR so it can be revisited when the data grows.

## Common traps

- **Treating everything as a one-way door.** Fear of mistakes turns every choice into a committee — and "it's a one-way door" becomes a way to stall.
- **Treating nothing as a one-way door.** "We can always change it later" — while ten teams start depending on it.
- **Forgetting that small doors add up.** Ten teams each picking their own logging library is ten two-way doors and one org-wide migration. Standardize choices many teams repeat ([[paved-roads]]).
- **Ignoring social irreversibility.** A reorg, a public promise, or a hiring decision can be harder to undo than any code.
- **Confusing "expensive to build" with "hard to undo."** A big project can still be easy to abandon; a tiny API decision can be permanent.

## When it doesn't apply

In a crisis, even one-way decisions sometimes have to be made fast, with whatever information you have. And very early in a product's life, almost everything is a two-way door because nothing depends on it yet — the framing matters more as the system and organization grow.

## Related

- [[yagni]] — build only what you need, *except* where a one-way door makes waiting expensive.
- [[architecture-trade-offs]] — how to compare the options once a door deserves the analysis.
- [[design-docs]] — the right tool for one-way doors.
- [[architecture-decision-records]] — record one-way decisions so the reasoning outlives the people.
- [[api-versioning]] — published APIs are a classic one-way door.
- [[paved-roads]] — how to standardize the small doors that add up.
- [[influencing-without-authority]] — spend your credibility on one-way doors, not two-way ones.
- [[bikeshedding]] — the trap of spending one-way-door effort on a two-way door.
