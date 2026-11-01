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

The term comes from Edsger Dijkstra (1974), who called it the only technique he knew for effectively ordering one's thoughts.

## Why it matters

- **Understandability.** You can read the pricing logic without wading through SQL and HTTP code.
- **Testability.** Pure business logic can be tested in milliseconds without a database or browser.
- **Contained change.** Adding a mobile app or changing storage touches the edges, not the rules. (Don't oversell this: swapping a relational database for a key-value store still leaks transaction and query semantics into the logic. The reliable win is testability.)
- **Parallel work.** Different people can change different concerns with fewer merge conflicts.

## How to apply it

- **Keep decisions apart from effects.** Logic decides; I/O (database, network, files, UI) does.
- **Group code by what changes together.** If two things always change at the same time, they're probably one concern.
- **Put boundaries where the shape of the data changes.** An HTTP request becomes a domain object; a domain object becomes a database row.
- **Translate once, at the edge.** Convert raw input into clean domain types as it enters the system.
- **Watch for "and."** A function that does "this *and* that" is usually two concerns.

## Example

**Tangled:**

```
function handleSignup(request):
    if "@" not in request.body.email: return 400
    if db.query("SELECT 1 FROM users WHERE email = ?", request.body.email): return 409
    db.insert("users", ...)
    smtp.send(welcomeEmail(request.body.email))
    return 201
```

**Separated:**

```
# rules — testable with in-memory fakes for users and mailer
function signUp(email, users, mailer):
    if "@" not in email: return Invalid
    if not users.add(email): return AlreadyExists   # add() reports a duplicate
    mailer.sendWelcome(email)
    return Created

# HTTP edge — only translates
function handleSignup(request):
    result = signUp(request.body.email, postgresUsers, smtpMailer)
    return {Invalid: 400, AlreadyExists: 409, Created: 201}[result]
```

One subtle point: the tangled version checks *then* inserts, so two simultaneous signups can both pass the check. In the separated version, uniqueness is guaranteed by a unique index in the database; `users.add` catches the duplicate-key error and reports it. In-memory tests can't prove uniqueness — the database constraint does.

## Common traps

- **Separating by technical layer only.** A `controllers/ services/ repositories/` split can still tangle every feature across all three. Consider grouping by domain (orders, billing) too — see [[coupling-and-cohesion]] for why.
- **Too many tiny pieces.** Splitting one simple concern across ten files adds navigation cost without benefit.
- **Leaky separation.** If the "business logic" module imports the HTTP framework, the concerns aren't really separate.

## When it doesn't apply

Small scripts and throwaway prototypes rarely need strict separation — a 50-line script that does everything top-to-bottom is fine. Introduce boundaries when the code is long-lived, shared, or growing.

## Related

- [[functional-core-imperative-shell]] — goes further: keep the rules completely free of I/O.
- [[hexagonal-architecture]] — the `users` and `mailer` parameters above are ports; this is that pattern in miniature.
- [[coupling-and-cohesion]] — the vocabulary for judging whether your separation is good.
- [[solid-principles]] — single responsibility is separation of concerns at the class level.
