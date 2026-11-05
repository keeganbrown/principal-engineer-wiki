# Quiz: Relational Databases

## Two buyers race for the last item and stock goes negative. What makes this impossible?

- [x] A `CHECK (stock >= 0)`, with stock decremented in SQL in one transaction.
- [ ] An application check that reads stock before writing the new value.
- [ ] A cache of current stock that's refreshed every few seconds.
- [ ] A nightly job that resets any negative stock back to zero.

**Why:** An application check runs before the write, so both buyers can pass it. A relative `UPDATE` plus the constraint can't be raced. The cost: in flash sales that single row becomes a lock hotspot. See [[relational-databases]].

## A team's database is under read load. What should they try before anything exotic?

- [x] Indexes for the actual queries, then read replicas.
- [ ] Sharding the database across several machines.
- [ ] Moving to a document database for scale.
- [ ] Splitting each table into its own separate database.

**Why:** An index can make a slow query fast, and replicas add read capacity without splitting data; bigger hardware and caching come before sharding too. Sharding multiplies operational cost. See [[relational-databases]].

## A page loads 50 orders and then runs one query per order to fetch its customer. What's the fix?

- [x] One join or batched query for all 50 customers.
- [ ] Caching each customer for an hour after its first read.
- [ ] Adding a read replica to take the extra queries.
- [ ] Raising the connection pool size so queries run in parallel.

**Why:** This is the N+1 query problem: one query plus N follow-ups is slow at scale. A join or batched query fetches the same data in one round trip. See [[relational-databases]].
