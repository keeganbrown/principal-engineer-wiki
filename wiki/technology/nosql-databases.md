---
title: NoSQL Databases
category: technology
summary: Non-relational databases trade joins and flexible queries for a specific strength — massive scale, simple lookups, flexible documents, or fast search — so pick one for a known access pattern, not for vague "scale."
tags: [databases, nosql, storage, data-modeling]
---

# NoSQL Databases

> **In one sentence:** Non-relational databases trade joins and flexible queries for a specific strength — massive scale, simple lookups, flexible documents, or fast search — so pick one for a known access pattern, not for vague "scale."

## The idea

**NoSQL** is a loose name for databases that don't use the relational table model. They aren't one thing; they're several families, each built for a particular shape of data and query:

- **Key-value stores** — look up a value by its key, very fast, at huge scale. Examples: Redis, DynamoDB in its simplest use.
- **Document stores** — store JSON-like documents; good when each record is read and written as one unit. Examples: MongoDB, Firestore.
- **Wide-column stores** — rows grouped by a *partition key* and spread across many machines; each row can hold different columns. You design the key so each query reads one group from one machine: all readings for sensor 17 share a key, so they live together. Built for very high write volume. Examples: Cassandra, Bigtable.
- **Search engines** — full-text search, ranking, and filtering over text. Examples: Elasticsearch, OpenSearch.
- **Time-series and analytics stores** — metrics and events over time, or aggregates over billions of rows: analytical work rather than many small transactions. Many keep a SQL interface but drop transactional features. Examples: InfluxDB, ClickHouse.

The common trade: you give up flexible queries and often multi-record transactions (or get them with tighter limits), and in return get scale or speed *for the queries you designed for*. Google's 2006 Bigtable paper and Amazon's 2007 Dynamo paper started the modern wave; the "NoSQL" label caught on in 2009.

## Why it matters

- **Some workloads outgrow one server.** Millions of writes per second, or data spread across continents, need storage designed to be distributed.
- **Some queries aren't relational.** Ranking documents by relevance to "red running shoes" is a search problem, not a SQL one.
- **Choosing wrong is expensive.** A store chosen for imagined scale makes everyday queries hard and pushes consistency rules into application code.

## How to apply it

- **Start from access patterns.** List the exact queries — "get cart by user ID," "latest 50 readings for sensor X." Many NoSQL stores require you to design the key around these up front, and queries you didn't plan for become slow or impossible.
- **Know what consistency you get.** Many distributed stores are eventually consistent by default: a read may return stale data for a while ([[cap-theorem]]).
- **Keep one system of record.** One store owns the truth (often a relational database), and search indexes or caches are fed from it ([[transactional-outbox]] covers how). Writing to both separately from the app lets them disagree whenever one write fails.
- **Plan for denormalization.** Without joins, you copy data into the shape each query needs. That's fast to read and harder to keep correct when the source changes.
- **Pick managed services where possible.** Running a distributed database cluster yourself is a specialist job.

## Example

An e-commerce team needs product search: typo tolerance, ranking by relevance and popularity, filters by size and color. They first try SQL `LIKE '%shoe%'` queries; they're slow, and "running shoos" finds nothing.

They add a search engine as a *secondary* store. Products stay in PostgreSQL; a change-data-capture (CDC) pipeline, which reads every committed change from the database's log, streams product-table changes into the search index within seconds. CDC on a business table exposes its column layout to whoever reads the stream; that's acceptable here because only this team reads it, to keep its own private index ([[transactional-outbox]]). Search requests go to the index; checkout reads prices and stock from PostgreSQL.

The trade-off shows up immediately: the index lags the database by a few seconds, so a just-discontinued product can still appear in results. The product page re-checks availability from the database, and the team accepts the brief staleness in search results.

## Common traps

- **Choosing NoSQL "for scale" before measuring.** A relational database on good hardware handles most companies' workloads ([[relational-databases]]).
- **Document stores for relational data.** Orders, customers, and products have relationships and rules. Modeling them as unrelated documents moves joins and integrity checks into application code.
- **Ignoring the consistency model.** Code written as if every read is fresh will have bugs against an eventually consistent store.
- **Using the search index as the source of truth.** Search engines are built to be rebuilt from a source; if they're the only copy, a corrupt index is lost data.
- **One store per team, by taste.** Every new database is something to operate, back up, secure, and hire for ([[paved-roads]]).

## When it doesn't apply

If your data has relationships, needs transactions across records, or faces unknown future questions, a relational database is usually the better default — many of them now handle JSON documents, full-text search, and key-value access well enough. Reach for a specialized store when you have a measured need it fits. Some needs are known before they can be measured, such as multi-region writes from day one or purely key-based access at large scale; there a purpose-built store can be the right first choice.

## Related

- [[relational-databases]] — the default these trade against.
- [[cap-theorem]] — the consistency trade-offs behind many distributed stores.
- [[caching]] — key-value stores often serve as caches.
- [[cqrs]] — separate read models, often in a different store.
- [[transactional-outbox]] — keeping secondary stores in sync with the source.
