---
title: SOLID Principles
category: principles
summary: Five guidelines for object-oriented design that keep code easy to extend and safe to change — useful as heuristics, not commandments.
tags: [design, object-oriented, maintainability]
---

# SOLID Principles

> **In one sentence:** Five guidelines for object-oriented design that keep code easy to extend and safe to change — useful as heuristics, not commandments.

## The idea

SOLID is an acronym. Each letter is a principle:

| Letter | Principle | Plain English |
| --- | --- | --- |
| **S** | Single Responsibility | A module should have one reason to change. |
| **O** | Open/Closed | Add new behavior by adding code, not by editing working code. |
| **L** | Liskov Substitution | A subtype must work anywhere its parent type is expected. |
| **I** | Interface Segregation | Don't force callers to depend on methods they don't use. |
| **D** | Dependency Inversion | High-level logic depends on abstractions, not on low-level details. |

They were written for classes, but the ideas apply to functions, modules, and services.

Robert C. Martin collected these principles around 2000, and Michael Feathers coined the acronym. Open/Closed comes from Bertrand Meyer (1988) and Liskov Substitution from Barbara Liskov (1987).

## Why it matters

All five aim at the same goal: **limit the blast radius of change.** When requirements shift, you want to touch one small place, not ten. SOLID gives you named checks for spotting designs that will fight you later.

## How to apply it

- **S: describe the module in one sentence without "and."** Ask "who would ask for this to change?" — Martin later clarified that a "reason to change" means one *actor*, one group of stakeholders.
- **O: replace a switch only when it repeats.** When the *same* `switch` on a type appears in several places, polymorphism or a lookup table lets new cases be additions. A single switch in one place is often the simplest thing ([[kiss]]).
- **L: watch for "not supported."** If a subclass throws for an inherited method, the hierarchy is wrong. Prefer composition.
- **I: split fat interfaces.** A `Printer` that also has `fax()` and `scan()` burdens every simple printer.
- **D: let business logic declare what it needs.** The logic defines an interface; infrastructure provides the implementation and passes it in as a parameter (called **dependency injection**). [[hexagonal-architecture]] applies this to a whole system.

## Example

Dependency inversion in practice:

```
# The business rule defines what it needs
interface Clock:
    now()

function isExpired(token, clock):
    return token.expiresAt < clock.now()

# Production passes SystemClock(); tests pass FixedClock("2026-01-01").
```

The rule doesn't know or care about the system clock, so tests are deterministic and fast.

## Common traps

- **An interface for everything.** An interface with exactly one implementation and no **test double** (a fake or stub used in tests) is often just noise.
- **Over-applying S.** Splitting every class into one-method fragments makes code harder to follow, not easier.
- **Open/closed as an excuse for speculation.** Don't build extension points until a real second case exists ([[dry]] has the wiki's rule for when to abstract).
- **Treating SOLID as a review checklist.** It's a vocabulary for discussing trade-offs, not a scoring rubric.

## When it doesn't apply

In functional or data-oriented code, some principles translate differently — "pass a function" often replaces "define an interface." In small programs, the indirection SOLID introduces can cost more than it saves. Use the principles to diagnose pain, not to prevent pain you don't have yet.

## Related

- [[separation-of-concerns]] — the broader idea behind single responsibility.
- [[hexagonal-architecture]] — owns ports, adapters, and dependency inversion at system scale.
- [[dry]] — single responsibility helps you tell real duplication from coincidence.
- [[yagni]] — the counterweight to building extension points too early.
