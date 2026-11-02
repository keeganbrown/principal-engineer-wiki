# Quiz: Relational Databases

## Two buyers race for the last item and stock goes negative. What makes this impossible?

- [x] A `CHECK (stock >= 0)` constraint, with checkout in one transaction.
- [ ] An application-level check before decrementing stock.
- [ ] A cache of current stock with a short TTL.
- [ ] A nightly job that resets negative stock to zero.

**Why:** Put rules in constraints; correctness is cheaper inside the database. Application-level fixes each had a race. See [[relational-databases]].

## A team's database is under read load. What should they try before anything exotic?

- [x] Indexes for the actual queries, then read replicas.
- [ ] Sharding the database across several machines.
- [ ] Moving to a document database for scale.
- [ ] Caching every query result for an hour.

**Why:** Relational databases scale further than most teams assume. Premature sharding is a listed trap. See [[relational-databases]].

## A page loads a list of 50 orders and then runs one query per order for its customer. What is this called?

- [x] An N+1 query problem.
- [ ] A lock hotspot.
- [ ] Replication lag.
- [ ] A long-running transaction.

**Why:** One query plus N follow-ups is slow at scale. A join or a batched query fetches the same data in one round trip. See [[relational-databases]].
