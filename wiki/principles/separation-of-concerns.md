---
title: Separation of Concerns
category: principles
summary: Split a system into parts that each handle one kind of job, so you can understand, test, and change each part without touching the others.
tags: [design, modularity, architecture]
---

# Separation of Concerns

> **In one sentence:** Split a system into parts that each handle one kind of job, so you can understand, test, and change each part without touching the others.

## The idea

A **concern** is a distinct area of responsibility: business rules, storing data, talking over the network, rendering a screen, logging. Separation of concerns means each part of the code deals with as few of these as possible.

Think of a restaurant. The chef cooks, the server takes orders, the cashier handles payment. If the chef also had to run the register, every rush hour would be chaos. Software is the same.

The term comes from Edsger Dijkstra, who argued it's the only way humans can reason about complex systems: focus on one aspect at a time.

## Why it matters

- **Understandability.** You can read the pricing logic without wading through SQL and HTTP code.
- **Testability.** Pure business logic can be tested in milliseconds without a database or browser.
- **Replaceability.** Swap Postgres for DynamoDB, or a web UI for a mobile app, without rewriting the rules.
- **Parallel work.** Different people can change different concerns with fewer merge conflicts.

## How to apply it

- Keep **decisions** (logic) apart from **effects** (I/O: database, network, files, UI).
- Group code by what changes together. If two things always change at the same time, they're probably one concern.
- Put boundaries where the "language" changes — e.g., HTTP requests vs. domain objects vs. database rows.
- Translate at the boundary: convert raw input into clean domain types once, at the edge.
- Watch for functions that do "this *and* that." The word "and" is a hint.

## Example

**Tangled:**

```
function handleSignup(request):
    if not request.body.email.contains("@"): return 400
    row = db.query("SELECT ... WHERE email = ?", request.body.email)
    if row: return 409
    db.insert(...)
    smtp.send(welcomeEmail(request.body.email))
    return 201
```

**Separated:** the HTTP handler parses input and maps results to status codes; a `signUp(email, users, mailer)` function holds the rules; `users` and `mailer` are small interfaces backed by the database and SMTP. Now the rules can be tested with in-memory fakes.

## Common traps

- **Separating by technical layer only.** A "controllers/ services/ repositories/" folder split can still tangle every feature across all three. Consider grouping by feature too.
- **Too many tiny pieces.** Splitting one simple concern across ten files adds navigation cost without benefit.
- **Leaky separation.** If the "business logic" module imports the HTTP framework, the concerns aren't really separate.

## When it doesn't apply

Small scripts and throwaway prototypes rarely need strict separation — a 50-line script that does everything top-to-bottom is fine. Introduce boundaries when the code is long-lived, shared, or growing.

## Related

- [[functional-core-imperative-shell]] — a concrete way to separate logic from effects.
- [[hexagonal-architecture]] — separation of concerns applied at the architecture level.
- [[coupling-and-cohesion]] — the vocabulary for judging whether your separation is good.
- [[solid-principles]] — single responsibility is separation of concerns at the class level.
