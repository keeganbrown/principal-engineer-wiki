# Quiz: Message Brokers (Queues and Logs)

## Which job fits a log, such as a Kafka topic, better than a queue?

- [x] Several services each reading "video published" at their own pace.
- [ ] A pool of workers sharing "transcode this video" tasks between them.
- [ ] Sending exactly one password-reset email for each request.
- [ ] Running a nightly cleanup job exactly once each night.

**Why:** Queues distribute tasks among workers; logs keep an ordered history many consumers can read and replay. Choose by the job. See [[message-brokers]].

## What should consumers of a message broker assume about delivery?

- [x] The same message may arrive more than once.
- [ ] Each message arrives exactly once, if the broker is configured right.
- [ ] Lost messages are common, so producers must resend them by hand.
- [ ] Duplicates happen only across partitions, never within one.

**Why:** Assume at-least-once delivery and make consumers idempotent. Some brokers offer exactly-once within their own system, but side effects outside it, like emails, still need idempotency. See [[message-brokers]] and [[idempotency]].

## Where should a message go after it fails processing repeatedly?

- [x] A dead-letter queue that a named owner reviews.
- [ ] Back onto the queue, to retry until it finally succeeds.
- [ ] Discarded, with a log line written after the last attempt.
- [ ] To a different consumer that is set up to ignore errors.

**Why:** A dead-letter queue stops one bad message from blocking the rest. Set it up on purpose rather than relying on the broker's default, and give it an owner, or it becomes a silent graveyard. See [[message-brokers]].

## A small app needs background jobs to send emails. What's the simplest fit?

- [x] A database table used as a job queue.
- [ ] A Kafka cluster with one topic per email type.
- [ ] A dedicated broker cluster run by a new team.
- [ ] A separate microservice for each kind of email.

**Why:** A small system can often use a database table as a job queue: fewer moving parts. Add a broker when the load or the number of consumers calls for it. See [[message-brokers]] and [[kiss]].
