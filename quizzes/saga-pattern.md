# Quiz: Sagas

## In a checkout saga, why does the confirmation email go last?

- [x] It can't be undone, so it waits for every step that might fail.
- [ ] Email is the slowest step, so it shouldn't delay the order.
- [ ] The email has to include the final order status from every service.
- [ ] Sagas run notification steps last by convention, whatever they do.

**Why:** Order steps by how easy they are to undo. Irreversible steps come after everything that might need compensating. See [[saga-pattern]].

## In a checkout saga, why authorize the card as one step and capture the payment as a later one?

- [x] Voiding a hold is cheaper and less visible than a refund.
- [ ] Authorization costs the payment provider less than a capture does.
- [ ] Capture can't happen without a separate approval from the customer.
- [ ] Authorization lets the whole saga run in a single database transaction.

**Why:** A hold takes no money yet, so voiding it is cheap; a refund after capture is slow and customer-visible, so capture comes as late as possible. See [[saga-pattern]].

## Another process reads an order halfway through a checkout saga. What protects it from acting on half-finished state?

- [x] A `PENDING` status that works as a lock, with a timeout and an owner.
- [ ] Nothing is needed; the saga's steps run inside one isolated transaction.
- [ ] The broker hides every record until the saga's last step has finished.
- [ ] Each service retries its read until the order has been fully committed.

**Why:** Sagas give up isolation: others can see intermediate states. A pending status is a semantic lock, and without a timeout a stalled saga leaves records locked forever. See [[saga-pattern]].

## A single business action regularly needs a saga across many services. What might that signal?

- [x] The service boundaries may be in the wrong place.
- [ ] The team should add distributed two-phase commit.
- [ ] The saga needs more compensating actions in it.
- [ ] The services need faster networks between them.

**Why:** If steps live in one database, use a normal transaction. Frequent cross-service sagas can mean the domain was split badly. See [[saga-pattern]] and [[domain-driven-design]].
