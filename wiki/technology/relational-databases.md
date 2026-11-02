---
title: Relational Databases
category: technology
summary: Store data in tables with enforced structure and transactions, and reach for one first — a well-run relational database handles far more scale and variety than most teams assume.
tags: [databases, sql, transactions, storage]
---

# Relational Databases

> **In one sentence:** Store data in tables with enforced structure and transactions, and reach for one first — a well-run relational database handles far more scale and variety than most teams assume.

## The idea

A **relational database** stores data as tables of rows and columns, links tables through shared keys, and answers questions in SQL. PostgreSQL, MySQL, SQL Server, and SQLite are the common ones.

Two features make it the default choice for most business data:

- **Constraints** — the database itself enforces rules: this column is never empty, this email is unique, every order points at a real customer. Bad data is rejected at the door, whatever code sent it.
- **Transactions** — a group of changes either all happen or none do, and concurrent users don't see each other's half-finished work. This bundle of guarantees is called **ACID**: atomicity (all or nothing), consistency (constraints hold), isolation (concurrent transactions don't see each other's half-finished work; how fully they're shielded depends on the *isolation level*, and most defaults allow some anomalies), and durability (committed data survives a crash).

The relational model comes from Edgar F. Codd's 1970 paper at IBM; SQL followed in the 1970s, and the core ideas have outlasted every trend since.

## Why it matters

- **Correctness is cheaper inside the database.** A unique constraint prevents duplicate accounts under any race. The same rule in application code fails the first time two requests arrive together.
- **Questions change; tables adapt.** SQL can answer questions nobody planned for — "which customers ordered twice but never reviewed?" — without restructuring the data.
- **It scales further than people think.** One large server with read replicas comfortably serves most companies' core data. Many teams move to exotic storage years before they need to.

The limits are real: one main server (the *primary*) takes all writes, very large tables need care with indexes and migrations, and spreading one database across regions is hard.

## How to apply it

- **Start here for business data.** Users, orders, payments, inventory — anything with relationships and rules belongs in a relational database unless you have a specific reason otherwise.
- **Put rules in constraints.** Use `NOT NULL`, `UNIQUE`, foreign keys, and `CHECK` constraints. Application checks give friendly errors; constraints give guarantees.
- **Index for your actual queries.** An **index** is a sorted lookup structure that makes a query fast at the cost of slower writes and more storage. Look at the query plan (`EXPLAIN`) before guessing.
- **Keep transactions short.** Long transactions hold locks and block other work. Never wait on a network call inside one ([[retries-and-timeouts]]).
- **Add read replicas before anything exotic.** A **read replica** is a copy that serves reads; it lags the primary slightly, so a screen that shows a user a change they just made should read from the primary, or they may not see their own update ([[cap-theorem]]).
- **Change schemas in safe steps.** Add, migrate, then remove — never rename a live column in one deploy ([[expand-and-contract]]).
- **Use the database's managed version if you can.** Backups, failover, and upgrades are where self-run databases go wrong.

## Example

A startup stores carts, orders, and inventory in a document database "for flexibility." Six months in, they find orders pointing to deleted products and stock counts that go negative when two people buy the last item at once. Each bug gets an application-level fix, and each fix has a race.

They move the core data to PostgreSQL: a foreign key from order lines to products, a `CHECK (stock >= 0)` constraint, and checkout in one transaction that decrements stock and inserts the order. The negative-stock bug becomes impossible: the second buyer's transaction fails the constraint and gets a clear "sold out." During flash sales, that single stock row becomes a lock hotspot that makes checkouts queue one at a time; the team accepts it at their volume and notes reserved or bucketed stock as the next step if it bites.

The cost: a two-month migration, and the team had to learn schema migrations. Their product catalog, which really is loosely structured, stays in a JSON column — relational databases handle semi-structured data well too.

## Common traps

- **Treating the database as a dumb bucket.** Skipping constraints "for speed" moves every rule into code, where it's enforced unevenly.
- **N+1 queries.** Loading a list, then running one query per item, turns one request into hundreds of round trips. Load related data in one query.
- **Sharing one database across services.** Many services writing the same tables couples them tightly ([[coupling-and-cohesion]]).
- **Premature sharding.** **Sharding** splits data across several databases by key. It multiplies operational cost; exhaust bigger hardware, indexes, replicas, and caching first.
- **Untested backups.** A backup you've never restored is a hope. Decide your recovery point objective (RPO — how much recent data you can lose) and recovery time objective (RTO — how long you can be down), then test that restores meet them.

## When it doesn't apply

Some workloads fit other stores better: huge volumes of simple key lookups, full-text search, analytics over billions of rows, or time-series metrics ([[nosql-databases]]). Even then, the usual pattern is a relational database as the system of record, with specialized stores fed from it.

## Related

- [[nosql-databases]] — when a different data model fits better.
- [[caching]] — the usual next step when reads get heavy.
- [[cap-theorem]] — what replicas and distributed databases trade away.
- [[transactional-outbox]] — publishing events reliably from a database transaction.
- [[expand-and-contract]] — changing schemas without downtime.
