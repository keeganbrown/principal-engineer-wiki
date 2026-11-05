---
title: Keep It Simple, Stupid (KISS)
category: principles
summary: Choose the simplest design that solves today's problem, because simple systems are easier to understand, change, and fix.
tags: [simplicity, design, maintainability]
---

# Keep It Simple, Stupid (KISS)

> **In one sentence:** Choose the simplest design that solves today's problem, because simple systems are easier to understand, change, and fix.

## The idea

Most code is read many more times than it is written. Every extra layer, option, or clever trick is something the next reader has to hold in their head. KISS says: when two designs both work, pick the one with fewer moving parts.

"Simple" is not the same as "easy." Easy means familiar or quick to type. Simple means *not tangled* — each piece does one thing and you can understand it without understanding everything else. Sometimes the simple solution takes more thought up front.

The phrase is usually credited to Lockheed engineer Kelly Johnson in the 1960s; the "Stupid" is aimed at the design, not the people. The simple-versus-easy distinction comes from Rich Hickey's 2011 talk *Simple Made Easy*.

## Why it matters

- **Bugs hide in complexity.** The more paths through the code, the more paths nobody tested.
- **Onboarding is faster.** A new teammate can contribute to a simple system in days, not months.
- **Change is cheaper.** You can't safely change what you don't understand.
- **Incidents are shorter.** At 3 a.m., the on-call engineer needs to reason about the system fast.

## How to apply it

- **Start with the most direct solution.** Add structure only when real pressure appears.
- **Prefer boring, well-known technology.** Choose something new only when it gives a clear, large win ([[golden-hammer]]).
- **Ask what you can remove before what you can add.**
- **Count the concepts.** How many ideas must a reader learn to understand this change? Fewer is better.
- **Favor plain data and functions.** Reach for frameworks and deep class hierarchies only when they pay for themselves.
- **Restructure instead of explaining.** If you need a long comment to say *what* code does, the code is too complicated.
- **Judge simplicity against what you already run.** One more instance of a familiar tool is often simpler than a new special case.

## Example

A team needs to send a nightly report email.

**Option A:** add a new message queue and a worker service — "so it can retry and scale."

**Option B:** a scheduled job that runs one script, renders a template, and calls the email API. If it fails, the scheduler alerts and someone reruns it. Option B ships in a day and has one place to look when it breaks.

The harder call: suppose the team *already* runs a job queue in production for other work. Now putting the report on that queue may be the simpler choice — one familiar system with existing monitoring beats a special-case scheduled (cron) job nobody remembers. Simple is relative to what you already operate.

## Common traps

- **Confusing simple with simplistic.** Ignoring real requirements (security, error handling) isn't simplicity; it's a bug you've postponed.
- **Writing clever one-liners.** Dense code is short, not simple.
- **Judging simplicity as the author.** Simplicity is judged by the reader.
- **Moving complexity rather than removing it.** Hiding a mess behind a nice interface still leaves the mess.

## When it doesn't apply

Some problems are inherently complex — distributed consensus, tax rules, real-time systems. Fred Brooks called this **essential complexity**: it comes from the problem itself and can't be designed away. What you *can* avoid is **accidental complexity**, which comes from your design choices rather than the problem ("No Silver Bullet," 1986).

A slightly more complex design is worth it when you have strong evidence — not a guess — that a requirement is coming, or when the decision would be expensive to reverse later.

## Related

- [[yagni]] — the time-based cousin of KISS: don't build for imagined futures.
- [[separation-of-concerns]] — a key technique for keeping each piece simple.
- [[technical-debt]] — what accumulates when complexity goes unchecked.
- [[modular-monolith]] — KISS applied to architecture: clean boundaries without a network.
- [[reversible-decisions]] — when a little up-front complexity is worth it.
