---
title: Functional Core, Imperative Shell
category: architecture
summary: Put all decisions in pure functions that just transform data, and keep a thin outer layer that does the I/O, so most of your code is trivial to test and reason about.
tags: [design, testing, functional-programming]
---

# Functional Core, Imperative Shell

> **In one sentence:** Put all decisions in pure functions that just transform data, and keep a thin outer layer that does the I/O, so most of your code is trivial to test and reason about.

## The idea

Gary Bernhardt named this pattern in his talk "Boundaries." Split your program into two parts:

- **Functional core** — pure functions. Given the same input, they always return the same output and touch nothing outside themselves: no database, no network, no clock, no randomness. This is where all the *decisions* live.
- **Imperative shell** — the thin outer layer that gathers inputs (reads the database, the request, the clock), calls the core, and then carries out the results (writes, sends, renders). It makes almost no decisions.

```
  input  ─►  [ shell: read ]  ─►  [ core: decide ]  ─►  [ shell: write ]  ─►  effects
```

## Why it matters

- **Testing becomes easy.** The core needs no mocks — just call a function and check the return value. Thousands of tests run in seconds.
- **Reasoning becomes easy.** Pure functions can be read in isolation. No hidden state changes.
- **The risky part shrinks.** The shell is so simple it needs only a few integration tests.
- **Portability.** The core can move to a new framework, platform, or language binding unchanged.

## How to apply it

- Ask of each function: "Does this decide, or does this do?" Split ones that do both.
- Pass everything the core needs as **arguments** — including "now" and random seeds.
- Have the core **return a description of what to do** (e.g., a list of emails to send) instead of doing it.
- Keep the shell boring: fetch, call, execute. If the shell has `if` statements about business rules, move them inward.
- Represent results as plain data (records, structs, dictionaries).

## Example

**Before** — logic and effects tangled:

```
function remindOverdueInvoices():
    for inv in db.query("SELECT * FROM invoices WHERE paid = false"):
        if inv.dueDate < now() - 7 days and not inv.reminded:
            email.send(inv.customer, "Your invoice is overdue")
            db.update(inv.id, reminded = true)
```

**After:**

```
# core: pure, easily tested
function overdueReminders(invoices, today):
    return [i for i in invoices
            if not i.paid and not i.reminded and i.dueDate < today - 7 days]

# shell: thin and dumb
function remindOverdueInvoices():
    for inv in overdueReminders(db.loadUnpaid(), clock.today()):
        email.send(inv.customer, "Your invoice is overdue")
        db.markReminded(inv.id)
```

Every edge case of "who gets a reminder?" is now a fast test of `overdueReminders`.

## Common traps

- **Leaking effects into the core** through "just one" logger call or `now()`. Pass them in.
- **A fat shell.** If the shell grows business logic, you've lost the benefit.
- **Loading too much.** The shell must fetch what the core needs; for huge datasets you may need streaming or several core/shell round-trips.

## When it doesn't apply

Some logic is inherently interleaved with I/O — e.g., "keep fetching pages until you find a match." You can still keep each step's decision pure, but the shell will do more coordination. For tiny scripts, the split may be overkill.

## Related

- [[separation-of-concerns]] — this pattern is separation of concerns between deciding and doing.
- [[hexagonal-architecture]] — a complementary, larger-scale version of the same idea.
- [[test-driven-development]] — a pure core makes TDD fast and pleasant.
- [[testing-pyramid]] — pushes most of your tests to the cheap bottom layer.
