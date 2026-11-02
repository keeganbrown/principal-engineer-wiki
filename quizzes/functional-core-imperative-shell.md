# Quiz: Functional Core, Imperative Shell

## Which question sorts a function into the core or the shell?

- [x] "Does this decide, or does this do?"
- [ ] "Is this function longer than 20 lines?"
- [ ] "Is this function called by more than one module?"
- [ ] "Does this function use a class or plain functions?"

**Why:** Decisions go in pure functions; effects like database writes and emails go in a thin shell. See [[functional-core-imperative-shell]].

## Where does `overdueReminders(invoices, today)` get the current date?

- [x] As an argument passed in by the shell.
- [ ] By calling the system clock inside the function.
- [ ] From a global variable set once at startup.
- [ ] From the database, as part of the invoice query.

**Why:** Pass everything the core needs as arguments, so tests can use any date with no clock to mock. Injecting a `Clock` is the dependency-inversion form of the same idea; passing `today` keeps the core fully pure. See [[functional-core-imperative-shell]] and [[solid-principles]].

## A pure core picks overdue invoices from a database snapshot, and the shell sends reminders. What risk must the shell handle?

- [x] The snapshot may be stale, so send only if the invoice is still unpaid.
- [ ] The core might start sending emails on its own if the shell runs slowly.
- [ ] Pure functions can't return lists, so the shell has to rebuild the result.
- [ ] The shell must re-run the core for each invoice to keep the result correct.

**Why:** A conditional update ("unpaid and not yet reminded") keeps two runs from sending the same reminder. Its cost: a crash between the mark and the send skips that reminder. That's fine here; use an outbox for effects that must happen. See [[functional-core-imperative-shell]] and [[transactional-outbox]].
