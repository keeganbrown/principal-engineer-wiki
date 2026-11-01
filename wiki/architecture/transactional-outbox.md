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

A close cousin is **change-data-capture (CDC)**: a tool like Debezium reads the database's own change log and turns committed changes into events.

## Why it matters

Lost or phantom events are some of the hardest bugs to find in an event-driven system. They're rare, they don't throw errors, and they show up weeks later as "why didn't this customer get a shipping email?" The outbox removes them.

The trade: you get duplicates instead of losses, an extra write per change, and one more process to deploy, monitor, and page on.

## How to apply it

- **Write the outbox row in the same transaction.** That's the whole trick.
- **Run the relay separately.** Use its own process or a scheduled job, never the request handler.
- **Expect duplicates.** If the relay crashes after publishing but before marking a row sent, it will publish again. Consumers must be idempotent ([[idempotency]]).
- **Run exactly one active relay, or make relays claim rows.** Two naive relays polling the same table publish every row twice. **Leader election** — the relays agree that only one is active at a time — prevents that and keeps order. Alternatively, each relay claims rows with `SELECT … FOR UPDATE SKIP LOCKED` (it locks the rows it takes; the others skip them) and holds its transaction open until it marks them sent. That shares the load but gives up ordering.
- **Don't trust ID order as commit order.** With concurrent writers, row 11 can commit before row 10, so even a single relay can publish them out of order. If per-entity order matters, give each entity's events a sequence number that consumers check, or lock the entity's row before inserting its outbox row so its events commit in order.
- **Clean up sent rows.** Delete or archive them so the table doesn't grow forever.
- **Monitor the lag.** A growing gap between a row being written and being published means the relay is stuck.
- **Point CDC at the outbox, not your business tables.** CDC on business tables publishes your internal schema as events. Many teams still write outbox rows but let CDC publish them: you keep an event shape you designed and drop the polling relay. The price is running the CDC connector and watching its replication lag — in Postgres, a stalled connector keeps the database's change log on disk until the disk fills.

## Example

```
# In the orders service — one transaction
with db.transaction():
    db.insert("orders", order)
    db.insert("outbox", {
        "eventType": "OrderPlaced",
        "payload": {"orderId": order.id, "total": order.total},
    })

# The single active relay, running every second.
# ID order isn't commit order: fine if consumers don't need strict per-entity order.
for row in db.query("SELECT * FROM outbox WHERE sentAt IS NULL ORDER BY id LIMIT 100"):
    broker.publish(row.eventType, row.payload, messageId=row.id)
    db.update("outbox", row.id, sentAt=now())
```

If the service crashes after the commit, the relay publishes the event when it next runs. If the transaction rolls back, there's no outbox row and no event. The `messageId` lets consumers drop duplicates.

For high availability, the team runs a second relay on standby. It takes over only when it wins leader election — otherwise both would publish every row.

## Common traps

- **Publishing "after commit" from the request handler.** That's the dual-write problem again.
- **Writing consumers that break on duplicates.** The outbox *will* produce them.
- **Hitting a single-relay bottleneck.** At very high volume, run several relays that each handle a slice of rows by **partition key** — a value, such as an `orderId` hash, that decides which relay handles a row — or switch to CDC.
- **Leaking internal table structure into events.** Design the event payload as a public contract.

## When it doesn't apply

If losing an occasional event is acceptable (analytics pings, cache warm-ups), a direct publish is simpler. If your broker and database support a shared transaction, or your database *is* your queue, you may not need it. And a system that doesn't publish events at all has no dual write to solve.

## Related

- [[event-driven-architecture]] — the outbox is how events get published reliably.
- [[idempotency]] — consumers must handle the duplicates the relay can produce.
- [[cqrs]] — CDC and outbox events are common ways to update read models.
- [[saga-pattern]] — each saga step usually publishes its result through an outbox.
- [[strangler-fig]] — CDC keeps old and new systems in sync during a migration.
