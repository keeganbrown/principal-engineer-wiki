# Quiz: NoSQL Databases

## A team needs typo-tolerant product search. How should they add a search engine?

- [x] As a secondary store fed from the relational database, which stays the system of record.
- [ ] As the new system of record, replacing the relational database.
- [ ] As a second database that the app writes to separately.
- [ ] By loading the full catalog into the search engine once a month.

**Why:** Keep one system of record. Using the search index as the source of truth is a listed trap. See [[nosql-databases]].

## What is the right starting point when choosing a NoSQL store?

- [x] Your access patterns: how the data is read and written.
- [ ] Which store is most popular this year.
- [ ] The vague expectation that you'll need to scale.
- [ ] Whichever store the team wants to learn.

**Why:** Pick a store for a known access pattern, not for vague "scale." Measure before choosing for scale. See [[nosql-databases]].

## Which data fits a document store worst?

- [x] Orders, products, and customers with many relationships and cross-record transactions.
- [ ] User profiles read and written as one document by ID.
- [ ] A product catalog where each category has different fields.
- [ ] Session data looked up by session ID.

**Why:** Relational data in a document store is a listed trap. A relational database is the better default for related records. See [[nosql-databases]] and [[relational-databases]].
