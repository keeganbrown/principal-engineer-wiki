# Quiz: Transactional Outbox

## What is the dual-write problem?

- [x] Saving to the database and publishing to the broker can't share one transaction, so a crash can do one without the other.
- [ ] Two services writing to the same table at the same time.
- [ ] Writing the same row twice because of a retry.
- [ ] Two brokers receiving the same event from one service.

**Why:** Save-then-publish can lose events; publish-then-save can announce what never happened. The outbox puts both writes in one database transaction. See [[transactional-outbox]].

## The relay publishes an event, then crashes before marking it sent. What happens?

- [x] The event is published again, so consumers must handle duplicates.
- [ ] The event is lost, because the row was never marked sent.
- [ ] The transaction rolls back and the order is deleted.
- [ ] The broker rejects the second copy automatically.

**Why:** The outbox gives at-least-once delivery. Expect duplicates and make consumers idempotent. See [[transactional-outbox]] and [[idempotency]].

## When is a direct publish without an outbox reasonable?

- [x] When losing an occasional event is acceptable, such as analytics pings.
- [ ] When the event is important enough that duplicates are a problem.
- [ ] When the service has more than one database table.
- [ ] When the broker is hosted by a cloud provider.

**Why:** The outbox costs a relay and cleanup. Skip it when an occasional lost event doesn't matter. See [[transactional-outbox]].
