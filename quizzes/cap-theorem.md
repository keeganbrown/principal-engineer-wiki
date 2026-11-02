# Quiz: CAP Theorem and Consistency Models

## The link between two data centers fails. What choice does CAP say the system now faces?

- [x] Stay consistent by refusing some requests, or stay available and risk serving stale or conflicting data.
- [ ] Stay consistent and available, but give up tolerance of the partition until the link heals.
- [ ] Keep all three properties, but only for read requests until the link heals.
- [ ] Switch both data centers to a single shared database until the link heals.

**Why:** Partitions happen whether you like it or not, so the real choice during one is between consistency and availability. "We picked CA" isn't an option for a distributed system. See [[cap-theorem]].

## An airline runs seat booking and a flight-status page across two regions. Which split fits?

- [x] Consistency for seat booking, availability for flight status.
- [ ] Availability for seat booking, consistency for flight status.
- [ ] Consistency for both, since they share the same data centers.
- [ ] Availability for both, since partitions are rare in practice.

**Why:** Selling seat 14C twice is costly, so booking should refuse rather than guess. A slightly stale status page beats an error page. Decide per operation, not per system. See [[cap-theorem]].

## A team adds read replicas to their single Postgres database. What should they watch for?

- [x] Replica reads can be seconds stale, so "show me what I just saved" should read from the primary.
- [ ] Replicas make writes strongly consistent everywhere, so nothing changes for readers.
- [ ] CAP no longer applies at all, because replicas live in the same data center.
- [ ] Every read must now go to the primary, or the replicas will drift apart permanently.

**Why:** A single database has nothing to partition, but replicas bring back a small version of the trade-off: replication lag. Route reads that must be fresh to the primary. See [[cap-theorem]] and [[relational-databases]].
