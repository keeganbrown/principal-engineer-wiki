---
title: SOLID Principles
category: principles
summary: Five guidelines for object-oriented design that keep code easy to extend and safe to change — useful as heuristics, not commandments.
tags: [design, object-oriented, maintainability]
---

# SOLID Principles

> **In one sentence:** Five guidelines for object-oriented design that keep code easy to extend and safe to change — useful as heuristics, not commandments.

## The idea

SOLID is an acronym popularized by Robert C. Martin. Each letter is a principle:

| Letter | Principle | Plain English |
| --- | --- | --- |
| **S** | Single Responsibility | A module should have one reason to change. |
| **O** | Open/Closed | Add new behavior by adding code, not by editing working code. |
| **L** | Liskov Substitution | A subtype must work anywhere its parent type is expected. |
| **I** | Interface Segregation | Don't force callers to depend on methods they don't use. |
| **D** | Dependency Inversion | High-level logic depends on abstractions, not on low-level details. |

They were written for classes, but the ideas apply to functions, modules, and services.

## Why it matters

All five aim at the same goal: **limit the blast radius of change.** When requirements shift, you want to touch one small place, not ten. SOLID gives you named checks for spotting designs that will fight you later.

## How to apply it

- **S:** Describe the module in one sentence without "and." "Who would ask for this to change?" should have one answer.
- **O:** When you see a growing `switch` on a type, consider polymorphism or a lookup table so new cases are additions.
- **L:** If a subclass throws "not supported" for an inherited method, the hierarchy is wrong. Prefer composition.
- **I:** Split fat interfaces. A `Printer` that also has `fax()` and `scan()` burdens every simple printer.
- **D:** Business logic declares the interface it needs (`PaymentGateway`); infrastructure provides the implementation (`StripeGateway`). Inject it.

## Example

Dependency inversion in practice:

```
# Business rule defines what it needs
interface Clock { now() }

function isExpired(token, clock):
    return token.expiresAt < clock.now()

# Production passes SystemClock; tests pass FixedClock("2026-01-01").
```

The rule doesn't know or care about the system clock, so tests are deterministic and fast.

## Common traps

- **Interface for everything.** An interface with exactly one implementation and no test double is often just noise.
- **Over-applying S.** Splitting every class into one-method fragments makes code harder to follow, not easier.
- **Open/closed as an excuse for speculation.** Don't build extension points until a second case exists.
- **Treating SOLID as a checklist for reviews.** It's a vocabulary for discussing trade-offs, not a scoring rubric.

## When it doesn't apply

In functional or data-oriented code, some principles translate differently — "pass a function" often replaces "define an interface." In small programs, the indirection SOLID introduces can cost more than it saves. Use the principles to diagnose pain, not to prevent pain you don't have yet.

## Related

- [[separation-of-concerns]] — the broader idea behind single responsibility.
- [[hexagonal-architecture]] — dependency inversion applied to a whole system.
- [[dry]] — single responsibility helps you tell real duplication from coincidence.
- [[yagni]] — the counterweight to building extension points too early.
