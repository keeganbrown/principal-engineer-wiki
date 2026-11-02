# Quiz: Transactional Outbox

## What is the dual-write problem?

- [x] A crash between the database save and the broker publish does only one.
- [ ] Two services writing the same table at once, so one update overwrites the other.
- [ ] Writing the same row twice because a client retried after a timeout.
- [ ] Two relays publishing the same outbox row, so consumers see it twice.

**Why:** They can't share one transaction. Save-then-publish can lose events; publish-then-save can announce what never happened. The outbox puts both writes in one database transaction. See [[transactional-outbox]].

## The relay publishes an event, then crashes before marking it sent. What happens?

- [x] The event is published again, so consumers must handle duplicates.
- [ ] The event is lost, because the row was never marked as sent.
- [ ] The transaction rolls back and the order is deleted with it.
- [ ] The broker always drops the second copy, so consumers needn't care.

**Why:** The outbox trades lost events for duplicate ones. Make consumers idempotent. See [[transactional-outbox]] and [[idempotency]].

## A team runs a second outbox relay for availability, and every event is now published twice. What fixes it?

- [x] Leader election, or relays that claim rows with `SKIP LOCKED`.
- [ ] Deleting outbox rows as soon as either relay reads them.
- [ ] Having consumers drop any event that arrives a second time.
- [ ] Running both relays less often, so that their polling rarely overlaps.

**Why:** One active relay keeps order; claiming rows shares the load but gives up ordering. Consumers still need to be idempotent either way. See [[transactional-outbox]].

## When is a direct publish without an outbox reasonable?

- [x] When losing an occasional event is fine, as with analytics pings.
- [ ] When consumers can't tolerate a duplicate event of any kind.
- [ ] When the service writes to more than one database table.
- [ ] When the broker is a managed service run by a cloud provider.

**Why:** The outbox costs an extra write and a relay to run. Skip it when a lost event doesn't matter, or when the broker and database share a transaction. See [[transactional-outbox]].
