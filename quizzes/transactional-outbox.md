# Quiz: Transactional Outbox

## What is the dual-write problem?

- [x] Saving and publishing can't share a transaction, so a crash can leave one undone.
- [ ] Two services writing the same table at once, so one update overwrites the other.
- [ ] Writing the same row twice because a client retried after a timeout.
- [ ] Two relays publishing the same outbox row, so consumers see it twice.

**Why:** Save-then-publish can lose events; publish-then-save can announce what never happened. The outbox puts both writes in one database transaction. See [[transactional-outbox]].

## The relay publishes an event, then crashes before marking it sent. What happens?

- [x] The event is published again, so consumers must handle duplicates.
- [ ] The event is lost, because the row was never marked as sent.
- [ ] The transaction rolls back and the order is deleted with it.
- [ ] The broker always drops the second copy, so consumers needn't care.

**Why:** The outbox trades lost events for duplicate ones. Make consumers idempotent. See [[transactional-outbox]] and [[idempotency]].

## A team runs a second outbox relay for availability, and both relays now publish every outbox row. What stops the double publishing?

- [x] Leader election, or relays that claim rows with `SKIP LOCKED`.
- [ ] Deleting outbox rows as soon as either relay reads them.
- [ ] Raising the batch size, so each poll claims more rows at once.
- [ ] Running both relays less often, so that their polling rarely overlaps.

**Why:** One active relay publishes in a single sequence; claiming rows shares the load but gives up even that. Consumers still need to be idempotent either way, because a relay can crash after publishing. See [[transactional-outbox]].

## When is a direct publish without an outbox reasonable?

- [x] When losing an occasional event is fine, as with analytics pings.
- [ ] When consumers can't tolerate a duplicate event of any kind.
- [ ] When the service writes to more than one database table.
- [ ] When the broker is a managed service run by a cloud provider.

**Why:** The outbox costs an extra write and a relay to run. Skip it when a lost event doesn't matter, or when the broker and database share a transaction. See [[transactional-outbox]].
