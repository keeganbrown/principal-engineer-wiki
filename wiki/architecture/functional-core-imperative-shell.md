---
title: Functional Core, Imperative Shell
category: architecture
summary: Put all decisions in pure functions that just transform data, and keep a thin outer layer that does the I/O, so most of your code is trivial to test and reason about.
tags: [design, testing, functional-programming]
---

# Functional Core, Imperative Shell

> **In one sentence:** Put all decisions in pure functions that just transform data, and keep a thin outer layer that does the I/O, so most of your code is trivial to test and reason about.

## The idea

Split your program into two parts:

- **Functional core** — pure functions. Given the same input, they always return the same output and touch nothing outside themselves: no database, no network, no clock, no randomness. This is where all the *decisions* live.
- **Imperative shell** — the thin outer layer that gathers inputs (reads the database, the request, the clock), calls the core, and then carries out the results (writes, sends, renders). It makes almost no decisions.

```
  input  ─►  [ shell: read ]  ─►  [ core: decide ]  ─►  [ shell: write ]  ─►  effects
```

Gary Bernhardt named the pattern in a 2012 *Destroy All Software* screencast and expanded on it in his talk "Boundaries."

## Why it matters

- **Testing becomes easy.** The core needs no mocks — just call a function and check the return value. Thousands of tests run in seconds.
- **Reasoning becomes easy.** Pure functions can be read in isolation. No hidden state changes.
- **The risky part shrinks.** The shell is so simple it needs only a few integration tests.
- **Portability.** The core can move to a new framework, platform, or language binding unchanged.

## How to apply it

- **Ask of each function: "Does this decide, or does this do?"** Split ones that do both.
- **Pass everything the core needs as arguments** — including "now" and random seeds.
- **Return a description of what to do** (e.g., a list of emails to send) instead of doing it.
- **Keep the shell boring:** fetch, call, execute. If the shell has `if` statements about business rules, move them inward.
- **Represent results as plain data** (records, structs, dictionaries).

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
        if db.markReminded(inv.id, only_if_not_already=True):   # conditional write
            email.send(inv.customer, "Your invoice is overdue")
```

Every edge case of "who gets a reminder?" is now a fast test of `overdueReminders`.

Note the conditional write. The core decides on a *snapshot* of the data. If two copies of the job run at once, both see the same unpaid invoice. Marking it reminded "only if not already" — and sending the email only if that succeeded — keeps customers from getting two emails.

## Common traps

- **Leaking effects into the core** through "just one" logger call or `now()`. Pass them in.
- **A fat shell.** If the shell grows business logic, you've lost the benefit.
- **Stale snapshots.** The core's decision can be out of date by the time the shell acts. Use conditional writes or idempotent effects ([[idempotency]]).
- **Loading too much.** For huge datasets, loop in pages: the shell loads a page, the core decides, the shell writes, repeat.

## When it doesn't apply

Some logic is inherently interleaved with I/O — e.g., "keep fetching pages until you find a match." You can still keep each step's decision pure, but the shell does more coordination. For tiny scripts, the split may be overkill.

## Related

- [[hexagonal-architecture]] — the two fit together: in a hexagon, the *use case* is a small shell that calls ports, and the *domain rules* it calls are the functional core.
- [[separation-of-concerns]] — this pattern is separation between deciding and doing.
- [[test-driven-development]] — a pure core makes TDD fast and pleasant.
- [[testing-pyramid]] — pushes most of your tests to the cheap bottom layer.
