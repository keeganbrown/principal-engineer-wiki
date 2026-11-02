# Quiz: Separation of Concerns

## A signup handler validates the email, queries the database, inserts a row, and sends mail inline. What is the main fix?

- [x] Move the rules into a function that takes the user store and mailer as inputs, and keep the HTTP handler as a thin translator.
- [ ] Split the handler into four microservices, one for each step.
- [ ] Add comments above each step so readers can tell the concerns apart.
- [ ] Move the SQL into a stored procedure so the handler is shorter.

**Why:** Keep decisions apart from effects. The rules become testable with in-memory fakes, and the edge only translates between HTTP and results. See [[separation-of-concerns]].

## Where does separation of concerns suggest putting boundaries?

- [x] Where the shape of the data changes, such as at the HTTP or database edge.
- [ ] Every 50 lines, so no single file grows too long.
- [ ] Between each technical layer, regardless of what changes together.
- [ ] Wherever a different engineer wrote the code.

**Why:** Translate once, at the edge, and group code by what changes together. Splitting only by technical layer is a common trap. See [[separation-of-concerns]].

## When is strict separation not worth it?

- [x] A 50-line throwaway script that does everything top to bottom.
- [ ] A long-lived service that several teams change every week.
- [ ] A shared library used by every product in the company.
- [ ] A billing module that is growing a new feature each month.

**Why:** Boundaries pay off when code is long-lived, shared, or growing. Short-lived scripts rarely need them. See [[separation-of-concerns]].
