# Quiz: Message Brokers (Queues and Logs)

## Which job fits a log, such as a Kafka topic, better than a queue?

- [x] Several services each reading "video published" events at their own pace, with replay.
- [ ] A pool of workers sharing "transcode this video" tasks.
- [ ] Sending one password-reset email per request.
- [ ] Running a nightly job exactly once.

**Why:** Queues distribute tasks among workers; logs keep an ordered, replayable history many consumers can read. Choose by the job. See [[message-brokers]].

## What delivery guarantee should consumers assume?

- [x] At least once, so the same message may arrive more than once.
- [ ] Exactly once, as long as the broker is configured correctly.
- [ ] At most once, so lost messages must be resent manually.
- [ ] In order across all partitions.

**Why:** Assume at-least-once delivery and make consumers idempotent. Assuming exactly-once is a listed trap. See [[message-brokers]] and [[idempotency]].

## Where does a message go after it fails processing repeatedly?

- [x] A dead-letter queue, with an alert so someone looks at it.
- [ ] Back to the front of the queue, forever.
- [ ] Nowhere; it's dropped silently.
- [ ] To a different consumer that ignores errors.

**Why:** A dead-letter queue stops one bad message from blocking the rest, but only helps if someone is alerted. See [[message-brokers]].
