# Quiz: Functional Core, Imperative Shell

## Which question sorts a function into the core or the shell?

- [x] "Does this decide, or does this do?"
- [ ] "Is this function longer than 20 lines?"
- [ ] "Is this function called by more than one module?"
- [ ] "Does this function use a class or plain functions?"

**Why:** Decisions go in pure functions; effects like database writes and emails go in a thin shell. See [[functional-core-imperative-shell]].

## In a functional core, imperative shell design, where should a pure `overdueReminders(invoices, today)` function get the current date?

- [x] As an argument passed in by the shell.
- [ ] By calling the system clock inside the function.
- [ ] From a global variable set once at startup.
- [ ] From the database, as part of the invoice query.

**Why:** Pass everything the core needs as arguments, so tests can use any date with no clock to mock. Injecting a clock also works, but passing the value keeps the core fully pure. See [[functional-core-imperative-shell]].

## A pure core picks overdue invoices from a database snapshot, and the shell sends reminders. What risk must the shell handle?

- [x] The snapshot may be stale, so send only if still unpaid and unreminded.
- [ ] The core might start sending emails on its own if the shell runs slowly.
- [ ] Pure functions can't return lists, so the shell has to rebuild the result.
- [ ] The shell must re-run the core for each invoice to keep the result correct.

**Why:** A conditional update ("unpaid and not yet reminded") keeps two runs from sending the same reminder. Its cost: a crash between the mark and the send skips that reminder. That's fine here; use an outbox for effects that must happen. See [[functional-core-imperative-shell]] and [[transactional-outbox]].

## A 40-line script fetches pages from an API until it finds a matching record, then prints it. Should you split it into a pure core and an imperative shell?

- [x] Probably not; for a tiny script the split costs more than it saves.
- [ ] Yes; every program should keep its decisions in pure functions.
- [ ] Yes, and move the page fetching into the pure core as well.
- [ ] No; code that calls an API can never have a functional core.

**Why:** Logic interleaved with I/O ("fetch until you find it") leaves the shell doing most of the work, and for tiny scripts the split may be overkill. See [[functional-core-imperative-shell]].
