# Quiz: Sagas

## In a checkout saga, why does the confirmation email go last?

- [x] It can't be undone, so it should happen only after every step that might fail.
- [ ] Emails are slow, so they should never block other steps.
- [ ] The email service has the lowest priority in the company.
- [ ] Sagas always run notification steps last by convention.

**Why:** Order steps by how easy they are to undo. Irreversible steps come after everything that might need compensating. See [[saga-pattern]].

## Why authorize the card before capturing payment?

- [x] Voiding a hold is invisible to the customer, while a refund is slow and visible.
- [ ] Authorization is cheaper for the payment provider.
- [ ] Capture can't happen without a separate customer approval.
- [ ] Authorization makes the saga run in a single transaction.

**Why:** Easy-to-undo steps come early. If stock runs out, nothing has touched the customer's card. See [[saga-pattern]].

## A single business action regularly needs a saga across many services. What might that signal?

- [x] The service boundaries may be drawn in the wrong place.
- [ ] The team should add a distributed two-phase commit.
- [ ] The saga needs more compensating actions.
- [ ] The services need faster networks between them.

**Why:** If steps live in one database, use a normal transaction. Frequent cross-service sagas can mean the domain was split badly. See [[saga-pattern]] and [[domain-driven-design]].
