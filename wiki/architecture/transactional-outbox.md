---
title: Transactional Outbox
category: architecture
summary: Save a state change and the event announcing it in the same database transaction, then publish the event separately, so you never save without publishing or publish without saving.
tags: [distributed-systems, messaging, data]
---

# Transactional Outbox

> **In one sentence:** Save a state change and the event announcing it in the same database transaction, then publish the event separately, so you never save without publishing or publish without saving.

## The idea

A service often needs to do two things at once: update its database ("order 42 is placed") and tell others via a message broker ("`OrderPlaced` happened"). These are two separate systems, and there's no transaction that covers both. This is called the **dual-write problem**:

- Save, then publish: if the process crashes in between, the order exists but nobody hears about it.
- Publish, then save: if the save fails, everyone hears about an order that doesn't exist.

The **outbox pattern** fixes this by making it one write:

1. In the **same database transaction** as the business change, insert the event into an `outbox` table.
2. A separate **relay** process reads new rows from the outbox and publishes them to the broker.
3. Once the broker confirms, the relay marks the rows as sent.

Because the event and the change commit together, they either both happen or neither does.

A close cousin is **change-data-capture (CDC)**: instead of an outbox table, a tool like Debezium reads the database's own change log and turns committed changes into events.

## Why it matters

Lost or phantom events are some of the hardest bugs to find in an event-driven system. They're rare, they don't throw errors, and they show up weeks later as "why didn't this customer get a shipping email?" The outbox removes the whole class of bug with a simple table and a small background job.

## How to apply it

- **Write the outbox row in the same transaction** as the state change. That's the whole trick.
- **Run the relay as its own process** (or a scheduled job), not in the request handler.
- **Expect duplicates.** If the relay crashes after publishing but before marking a row sent, it will publish again. Consumers must be idempotent ([[idempotency]]).
- **Preserve order where it matters.** Publish rows for the same entity (e.g., same `orderId`) in the order they were written.
- **Clean up.** Delete or archive sent rows so the table doesn't grow forever.
- **Monitor the lag** between a row being written and being published. A growing lag means the relay is stuck.
- **Choose CDC instead** when you have many services or high volume and already run the infrastructure for it — it avoids an extra write and a polling job.

## Example

```
# In the orders service — one transaction
with db.transaction():
    db.insert("orders", order)
    db.insert("outbox", {
        "event_type": "OrderPlaced",
        "payload": {"orderId": order.id, "total": order.total},
    })

# Separate relay process, running every second
for row in db.query("SELECT * FROM outbox WHERE sent_at IS NULL ORDER BY id LIMIT 100"):
    broker.publish(row.event_type, row.payload, message_id=row.id)
    db.update("outbox", row.id, sent_at=now())
```

If the service crashes after the commit, the relay publishes the event when it next runs. If the transaction rolls back, there's no outbox row and no event. The `message_id` lets consumers drop duplicates.

## Common traps

- **Publishing from the request handler "after commit"** — this is the dual-write problem again.
- **Non-idempotent consumers** that break on the duplicates the outbox will produce.
- **A single relay as a bottleneck** at very high volume. Partition or switch to CDC.
- **Leaking internal table structure** into events. Design the event payload as a public contract.

## When it doesn't apply

If losing an occasional event is acceptable (analytics pings, cache warm-ups), a direct publish is simpler. If your broker and database support a shared transaction, or your database *is* your queue, you may not need it. And a system that doesn't publish events at all has no dual write to solve.

## Related

- [[event-driven-architecture]] — the outbox is how events get published reliably.
- [[idempotency]] — consumers must handle the duplicates the relay can produce.
- [[cqrs]] — CDC and outbox events are common ways to update read models.
- [[saga-pattern]] — each saga step usually publishes its result through an outbox.
