---
title: DRY — Don't Repeat Yourself
category: principles
summary: Every piece of knowledge should live in one place, but wait until you've seen real repetition before building an abstraction for it.
tags: [design, abstraction, maintainability]
---

# DRY — Don't Repeat Yourself

> **In one sentence:** Every piece of knowledge should live in one place, but wait until you've seen real repetition before building an abstraction for it.

## The idea

DRY was coined in *The Pragmatic Programmer*: "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

The key word is **knowledge**, not *code*. Two pieces of code can look identical but represent different ideas that will change for different reasons. Two pieces of code can look different but encode the same rule. DRY cares about the rule.

## Why it matters

When the same business rule lives in three places, someone will eventually update two of them. The result is a bug that's hard to find, because each copy looks correct on its own.

But the opposite mistake is just as costly. A premature abstraction couples things that should have stayed separate. Every new case adds another `if` or flag until the shared function is harder to understand than the duplicates were.

## How to apply it

- **Rule of three.** Tolerate duplication once. When you see the third copy, you know enough about the pattern to abstract it well.
- Ask: "If this rule changes, must all copies change together?" If yes, unify them. If not, they only *look* alike.
- Centralize **facts**: constants, validation rules, pricing logic, config, schemas.
- Prefer small, focused helpers over one big "do everything" function with flags.
- Generate code or docs from a single source (e.g., API schema → client + docs) rather than hand-syncing.

## Example

The tax rate `0.0825` appears in the checkout page, the invoice generator, and the refunds service. When the rate changes, refunds keeps the old value for a week. **Fix:** one `TAX_RATE` source of truth that all three read.

Counter-example: `validate_shipping_address` and `validate_billing_address` look identical today. Merging them seems DRY — until billing must match the card issuer's format and shipping must support PO boxes. They were different knowledge all along.

## Common traps

- **Abstracting on coincidence.** Similar-looking code isn't necessarily the same idea.
- **The "wrong abstraction."** Once a shared function grows flags for each caller, it's often cheaper to inline it back into copies and start over.
- **DRY across service boundaries.** Sharing a library of domain models between microservices couples their release cycles. Some duplication between services is healthy.
- **DRY tests.** Tests should be readable on their own; a little repetition beats a maze of shared helpers.

## When it doesn't apply

Duplication is cheaper than the wrong abstraction. In tests, in prototypes, and across independently deployed services, favor clarity and independence over deduplication.

## Related

- [[yagni]] — don't build the abstraction until you need it.
- [[coupling-and-cohesion]] — over-eager DRY creates coupling between unrelated parts.
- [[solid-principles]] — single responsibility helps you see which code shares a "reason to change."
