# Quiz: CAP Theorem and Consistency Models

## The link between two data centers fails. What choice does CAP say the system now faces?

- [x] Refuse some requests to stay consistent, or answer and risk stale data.
- [ ] Stay consistent and available, giving up partition tolerance until the link heals.
- [ ] Keep all three properties, but only for read requests until the link heals.
- [ ] Switch both data centers onto one shared database until the link heals.

**Why:** Partitions happen whether you like it or not, so the real choice during one is between consistency and availability. "We picked CA" isn't an option for a distributed system. See [[cap-theorem]].

## An airline runs seat booking and a flight-status page across two regions, and a partition forces a choice. Which split fits?

- [x] Consistency for seat booking, availability for flight status.
- [ ] Availability for seat booking, consistency for flight status.
- [ ] Consistency for both, since they share the same data centers.
- [ ] Availability for both, since partitions are rare in practice.

**Why:** Default to one strong store, and relax consistency only where you must; then decide per operation. Selling seat 14C twice is costly, while a slightly stale status page beats an error page. See [[cap-theorem]].

## A team adds read replicas to their single Postgres database. What should they watch for?

- [x] Replica reads can be stale, so "what I just saved" reads the primary.
- [ ] Replicas make every write strongly consistent, so readers see no change.
- [ ] CAP stops applying, because the replicas live in the same data center.
- [ ] Every read must now go to the primary, or the replicas drift apart forever.

**Why:** A single database has nothing to partition, but replicas bring back a small version of the trade-off: replication lag. Route reads that must be fresh to the primary. See [[cap-theorem]] and [[relational-databases]].
