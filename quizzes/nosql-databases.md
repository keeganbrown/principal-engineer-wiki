# Quiz: NoSQL Databases

## A team needs typo-tolerant product search. How should they add a search engine?

- [x] As a secondary store fed from the database of record.
- [ ] As the new system of record, replacing the relational database.
- [ ] As a second database that the app writes to separately.
- [ ] As a monthly snapshot of the full catalog, loaded in bulk.

**Why:** Keep one system of record. The index lags by a few seconds, so the product page re-checks availability from the database. See [[nosql-databases]].

## What is the right starting point when choosing a NoSQL store?

- [x] The exact queries: how the data is read and written.
- [ ] The scale the team hopes the product reaches someday.
- [ ] Which store has grown most in popularity this year.
- [ ] Whichever store the team is most eager to learn.

**Why:** Many NoSQL stores need the key designed around your queries up front. Measure before choosing for scale, unless the need is known in advance, like multi-region writes from day one. See [[nosql-databases]].

## Which data fits a document store worst?

- [x] Orders that must always point at an existing customer and product.
- [ ] User profiles read and written as one document by ID.
- [ ] A product catalog where each category has different fields.
- [ ] Session data looked up by session ID on every request.

**Why:** Related records that need integrity across them are what relational databases do well, with foreign keys and transactions. See [[nosql-databases]] and [[relational-databases]].
