---
title: KISS — Keep It Simple
category: principles
summary: Choose the simplest design that solves today's problem, because simple systems are easier to understand, change, and fix.
tags: [simplicity, design, maintainability]
---

# KISS — Keep It Simple

> **In one sentence:** Choose the simplest design that solves today's problem, because simple systems are easier to understand, change, and fix.

## The idea

Most code is read many more times than it is written. Every extra layer, option, or clever trick is something the next reader has to hold in their head. KISS says: when two designs both work, pick the one with fewer moving parts.

"Simple" is not the same as "easy." Easy means familiar or quick to type. Simple means *not tangled* — each piece does one thing and you can understand it without understanding everything else. Sometimes the simple solution takes more thought up front.

## Why it matters

- **Bugs hide in complexity.** The more paths through the code, the more paths nobody tested.
- **Onboarding cost.** A new teammate can contribute to a simple system in days, not months.
- **Change is cheaper.** You can't safely change what you don't understand.
- **Incidents are shorter.** At 3 a.m., the on-call engineer needs to reason about the system fast.

## How to apply it

- Start with the most direct solution. Add structure only when real pressure appears.
- Prefer boring, well-known technology unless something new gives a clear, large win.
- Ask "what can I remove?" before "what can I add?"
- Count the concepts a reader must learn to understand a change. Fewer is better.
- Favor plain data and functions over frameworks and deep class hierarchies.
- If you need a long comment to explain *what* code does, restructure it instead.

## Example

A team needs to send a nightly report email.

**Complex:** a message queue, a worker service, a retry scheduler, and a templating microservice — "so it scales."

**Simple:** a scheduled job that runs one script, renders a template, and calls the email API. If it fails, the scheduler alerts and someone reruns it.

The simple version ships in a day, has one place to look when it breaks, and can grow into the complex version *if* report volume ever demands it.

## Common traps

- **Confusing simple with simplistic.** Ignoring real requirements (security, error handling) isn't simplicity; it's a bug you've postponed.
- **Clever one-liners.** Dense code is short, not simple.
- **"Simple for me."** Simplicity is judged by the reader, not the author.
- **Moving complexity rather than removing it.** Hiding a mess behind a nice interface still leaves the mess.

## When it doesn't apply

Some problems are inherently complex — distributed consensus, tax rules, real-time systems. You can't make that complexity disappear; you can only keep it contained and avoid adding *accidental* complexity on top. Also, a slightly more complex design is sometimes worth it when you have strong evidence (not a guess) that a requirement is coming.

## Related

- [[yagni]] — the time-based cousin of KISS: don't build for imagined futures.
- [[separation-of-concerns]] — a key technique for keeping each piece simple.
- [[technical-debt]] — what accumulates when complexity goes unchecked.
