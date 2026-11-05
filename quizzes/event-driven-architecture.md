# Quiz: Event-Driven Architecture

## Which event name is a fact rather than a disguised command?

- [x] `OrderPlaced`
- [ ] `SendWelcomeEmail`
- [ ] `UpdateInventoryNow`
- [ ] `ChargeCustomerCard`

**Why:** Events announce what happened, and any interested service reacts. A broadcast command couples the publisher to one consumer's job. Commands are fine when one coordinator owns the workflow, as in an orchestrated saga. See [[event-driven-architecture]] and [[saga-pattern]].

## "My Shipments" lags a few seconds behind checkout, because shipping reacts to an event. What should the page show meanwhile?

- [x] "Processing…" instead of an empty list.
- [ ] The new order, by making shipping synchronous again.
- [ ] An error, so users know to check back later.
- [ ] An empty list, since users won't notice.

**Why:** Events bring eventual consistency. Design the experience around the lag rather than pretending it isn't there. See [[event-driven-architecture]] and [[cap-theorem]].

## A team moves checkout's side effects to events. What does the order service lose?

- [x] Knowing which consumers break when it changes the event.
- [ ] Its own database, which now moves into the broker.
- [ ] Any need to version the events it publishes from now on.
- [ ] At-least-once delivery for the events it sends.

**Why:** Coupling doesn't vanish: it moves into the event schema and into flows nobody can see in one place. The broker also becomes critical infrastructure. See [[event-driven-architecture]].

## When is a synchronous call the better choice?

- [x] When the caller needs an answer now, like "is this card valid?"
- [ ] When more than two services need to hear about the same change.
- [ ] When a consumer might be down for a while during deploys.
- [ ] When the work can safely happen a few seconds later.

**Why:** Payment stays synchronous in the example because checkout needs the answer. Events suit side effects that can happen later. See [[event-driven-architecture]].
