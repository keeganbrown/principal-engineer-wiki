# Quiz: Event-Driven Architecture

## Which event name is a fact rather than a disguised command?

- [x] `OrderPlaced`
- [ ] `SendWelcomeEmail`
- [ ] `UpdateInventoryNow`
- [ ] `ChargeCustomerCard`

**Why:** Events announce what happened; any interested service reacts. A "command" event couples the publisher to one consumer's job. See [[event-driven-architecture]].

## After moving checkout's side effects to events, "My Shipments" may not show a new order for a few seconds. What's the right response?

- [x] Show "Processing…" instead of an empty list.
- [ ] Make every consumer synchronous again.
- [ ] Hide the shipments page for the first minute after checkout.
- [ ] Ignore it; users won't notice a few seconds.

**Why:** Events bring eventual consistency. Design the experience around the lag rather than pretending it isn't there. See [[event-driven-architecture]].

## When is a synchronous call the better choice?

- [x] When the caller needs an immediate answer, like "is this card valid?"
- [ ] Whenever more than two services need to hear about something.
- [ ] Whenever a consumer might be down for a while.
- [ ] Whenever the work can happen a few seconds later.

**Why:** Payment stays synchronous in the example because checkout needs the answer. Events suit side effects that can happen later. See [[event-driven-architecture]].
