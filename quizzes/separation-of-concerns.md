# Quiz: Separation of Concerns

## A signup handler validates the email, queries the database, inserts a row, and sends mail inline. What is the main fix?

- [x] Pull the rules into a function that takes the user store and mailer.
- [ ] Split it into controller, service, and repository layers by file type.
- [ ] Add comments above each step, so readers can tell the concerns apart.
- [ ] Move the SQL into a stored procedure, so the handler has less code in it.

**Why:** Keep decisions apart from effects, and keep the HTTP handler a thin translator. The rules become testable with in-memory fakes, but uniqueness still comes from the database's unique index; fakes can't prove it. See [[separation-of-concerns]].

## Where does separation of concerns suggest putting boundaries?

- [x] Where the shape of the data changes, as at the HTTP edge.
- [ ] Every 50 lines, so that no single file grows too long to read.
- [ ] Between each technical layer, regardless of what changes together.
- [ ] Around each class, so that every class can be tested on its own.

**Why:** Translate once, at the edge, and group code by what changes together. Splitting only by technical layer scatters one change across many files. See [[separation-of-concerns]].

## For which code is strict separation least worth it?

- [x] A 50-line script you'll run once and delete.
- [ ] A long-lived service several teams change every week.
- [ ] A shared library used by every product in the company.
- [ ] A billing module that grows a new feature each month.

**Why:** Boundaries pay off when code is long-lived, shared, or growing. Short-lived scripts rarely need them. See [[separation-of-concerns]].
