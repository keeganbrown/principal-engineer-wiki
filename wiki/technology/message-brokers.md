---
title: Message Brokers (Queues and Logs)
category: technology
summary: A message broker lets services hand off work or announce events without waiting for each other; choose a queue to distribute tasks, or a log to keep an ordered, replayable history of events.
tags: [messaging, queues, kafka, asynchronous, distributed-systems]
---

# Message Brokers (Queues and Logs)

> **In one sentence:** A message broker lets services hand off work or announce events without waiting for each other; choose a queue to distribute tasks, or a log to keep an ordered, replayable history of events.

## The idea

A **message broker** sits between services. A **producer** sends a message to the broker; one or more **consumers** read it later. The producer doesn't wait for the work to finish and doesn't need to know who consumes it.

Brokers come in two main shapes:

- **Queues** — each message is a task handed to *one* worker, then removed once that worker *acknowledges* it (tells the broker the work is done). Good for spreading work: "resize this image," "send this email." Examples: RabbitMQ, Amazon SQS.
- **Logs** — messages are appended to a named, ordered, durable log (a *topic*) and kept for a set time. Many consumers read independently, each tracking its own position, and can replay from the past. Good for event streams: "order placed," "payment captured." Examples: Apache Kafka, Amazon Kinesis, Redpanda.

Kafka, open-sourced by LinkedIn in 2011, popularized the log model; queues are decades older. The line is blurring: Kafka 4.2 (2026) added queue-style consumption on top of its log.

## Why it matters

- **Services stay up when others are slow or down.** The broker holds messages until the consumer recovers.
- **Load gets smoothed.** A burst of 10,000 uploads becomes a steady stream for a fixed pool of workers ([[backpressure]]).
- **New consumers join without changing producers.** A log lets an analytics team start reading order events without touching the order service ([[event-driven-architecture]]).

The cost: a broker is another critical system to run, and asynchronous flows are harder to debug, test, and reason about than a direct call.

## How to apply it

- **Choose by the job.** Work to be done once by someone → queue. Facts many parties care about, possibly replayed → log.
- **Assume at-least-once delivery.** Most brokers redeliver a message if a consumer crashes before acknowledging it. Consumers must handle duplicates safely ([[idempotency]]). The alternative, *at-most-once*, never duplicates but can lose messages.
- **Know your ordering guarantee.** Logs keep order only within a **partition** — one ordered slice of a topic, chosen by a key such as order ID. Messages for different keys can arrive in any order.
- **Use a dead-letter queue.** A **dead-letter queue (DLQ)** holds messages that keep failing, so one bad message doesn't block the rest. Someone must own reviewing it, or it becomes a silent graveyard.
- **Publish reliably from a transaction.** Writing to your database and the broker separately can lose or invent messages; use the [[transactional-outbox]].
- **Monitor consumer lag.** **Lag** is how far behind consumers are. Rising lag is the earliest warning that consumers can't keep up ([[observability]]).
- **Version message formats.** Messages outlive deploys; a consumer may read last month's format during a replay.

## Example

A video platform transcodes uploads synchronously in the upload request. Uploads time out for long videos, and a spike of uploads takes the web servers down.

They split it: the upload request stores the file and puts a "transcode video 812" message on a queue, then returns at once. A pool of workers consumes the queue; a spike now means a longer queue, not an outage. Separately, a "video published" event goes to a Kafka topic, where search indexing, notifications, and analytics each consume at their own pace.

The cost shows up in support: "my video is still processing" is now a visible state that needs UI, monitoring of queue age, and an alert when the oldest message is over 15 minutes old. A transcode that crashes after finishing but before acknowledging runs twice, so the worker checks whether output already exists before starting. That check alone races: a transcode that outlasts the queue's redelivery timeout is handed to a second worker while the first is still running. So the team sets the timeout above the longest transcode and writes output under a key derived from the video ID, which makes a duplicate run overwrite rather than double up.

## Common traps

- **Using a queue as a database.** Messages are for handing things off, not long-term querying.
- **Unbounded queues.** A queue that grows forever hides an outage until the backlog is days old. Alert on age and depth.
- **Assuming exactly-once.** Some brokers offer exactly-once features within their own system, but side effects outside it — emails, payments — still need idempotency.
- **Hot partitions.** Keying by a value most messages share (one big customer) puts all the load on one consumer.
- **Async everywhere.** If a user needs the answer now, a direct call with a timeout is simpler than sending a request message and waiting for a reply message.

## When it doesn't apply

For simple request–response work, where the caller needs the result to continue, a direct call is easier to build and debug. And a small system can often use a database table as a job queue — fewer moving parts — until volume or fan-out demands a real broker.

## Related

- [[event-driven-architecture]] — the design style brokers enable.
- [[transactional-outbox]] — publishing to a broker reliably.
- [[idempotency]] — required for at-least-once consumers.
- [[backpressure]] — queues absorb bursts but need limits.
- [[saga-pattern]] — multi-step workflows coordinated through messages.
