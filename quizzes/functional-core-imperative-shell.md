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
- [ ] From a global variable set at startup.
- [ ] From the database, as part of the invoice query.

**Why:** Pass everything the core needs as arguments. Then tests can use any date, with no clock to mock. See [[functional-core-imperative-shell]].

## The core picks invoices from a snapshot, and the shell sends reminders. What risk must the shell handle?

- [x] The snapshot may be stale, so it should update only if the invoice is still unpaid and not yet reminded.
- [ ] The core might send emails on its own if the shell is slow.
- [ ] Pure functions can't return lists, so the shell must rebuild them.
- [ ] The shell must re-run the core for every invoice to stay correct.

**Why:** Stale snapshots are a listed trap. A conditional update in the shell keeps two runs from sending the same reminder twice. See [[functional-core-imperative-shell]].
