---
title: Don't Repeat Yourself (DRY)
category: principles
summary: Every piece of knowledge should live in one place, but wait until you've seen real repetition before building an abstraction for it.
tags: [design, abstraction, maintainability]
---

# Don't Repeat Yourself (DRY)

> **In one sentence:** Every piece of knowledge should live in one place, but wait until you've seen real repetition before building an abstraction for it.

## The idea

DRY says: "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

The key word is **knowledge**, not *code*. Two pieces of code can look identical but represent different ideas that will change for different reasons. Two pieces of code can look different but encode the same rule. DRY cares about the rule.

The principle comes from Andy Hunt and Dave Thomas's *The Pragmatic Programmer* (1999).

## Why it matters

When the same business rule lives in three places, someone will eventually update two of them. The result is a bug that's hard to find, because each copy looks correct on its own.

But the opposite mistake is just as costly. A premature abstraction couples things that should have stayed separate. Every new case adds another `if` or flag until the shared function is harder to understand than the duplicates were.

## How to apply it

This article owns the wiki's answer to "when should I abstract?":

- **Unify a known rule at the second copy.** If you already *know* two places encode the same business fact — a tax rate, a validation rule — don't wait. Give it one home now.
- **Wait for the third copy of look-alike code.** When code merely *looks* similar, writing it twice is fine. By the third time, you know enough about the pattern to abstract it well. This is the **rule of three** (Don Roberts, via Martin Fowler's *Refactoring*).
- **Ask whether the copies change together.** If the rule changes, must every copy change? If yes, unify. If not, they only look alike.
- **Centralize facts.** Constants, validation rules, pricing logic, config, and schemas each get one source of truth.
- **Keep helpers small and focused.** One big "do everything" function with flags is a sign of the wrong abstraction.
- **Generate from one source.** Produce clients and docs from a single API schema rather than hand-syncing them.

## Example

The tax rate `0.0825` is hard-coded in the checkout page, the invoice generator, and the refunds service. When the rate changes, refunds keeps the old value for a week.

Checkout and invoices live in the same codebase, so they share one `TAX_RATE` constant. But refunds is a **separate service**, and a shared library constant would tie its releases to the others. Instead, one service — pricing — *owns* the tax rate and exposes it through its API. Refunds reads it at runtime. Knowledge is shared across the boundary through a contract, not through shared code.

Counter-example: `validate_shipping_address` and `validate_billing_address` look identical today. Merging them seems DRY — until billing must match the card issuer's format and shipping must support PO boxes. They were different knowledge all along.

## Common traps

- **Abstracting on coincidence.** Similar-looking code isn't necessarily the same idea.
- **The wrong abstraction.** Once a shared function grows flags for each caller, it's often cheaper to inline it back into copies and start over. Sandi Metz put it well: "duplication is far cheaper than the wrong abstraction."
- **Sharing code across service boundaries.** A shared library of domain models couples the services' release cycles. Share knowledge through APIs and events instead. [[domain-driven-design]] makes the same point from the other side: don't build one canonical model for everyone.
- **Over-DRY tests.** Tests should read on their own; a little repetition beats a maze of shared helpers.

## When it doesn't apply

Prototypes and spikes don't live long enough for duplication to hurt. Generated code is fine to repeat, because the generator is the single source. And sometimes two teams *should* keep separate copies of similar logic so they can evolve independently — that's a deliberate trade, not a DRY violation.

## Related

- [[yagni]] — don't build the abstraction until you need it.
- [[coupling-and-cohesion]] — over-eager DRY creates coupling between unrelated parts.
- [[solid-principles]] — single responsibility helps you see which code shares a "reason to change."
- [[domain-driven-design]] — why one shared model across contexts backfires.
