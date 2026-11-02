# Quiz: CQRS

## A product page assembles data from four services and takes 800ms. How does CQRS help?

- [x] A projector keeps a pre-built document per product, so the page is one lookup.
- [ ] Each request queries the four services in parallel, so the page loads faster.
- [ ] All four services move into one shared database, so a single query can join them.
- [ ] The page caches each service's response for a full day at a time.

**Why:** Separate the read model from the write side when their needs diverge. The price is that the read view can lag by a few seconds. See [[cqrs]].

## A product page reads from a CQRS read model that can lag by a few seconds. What should checkout do?

- [x] Re-check price and stock with the owning services before charging.
- [ ] Trust the product page, since it was correct when the user loaded it.
- [ ] Block the product page until the read model is fully up to date.
- [ ] Charge the displayed price and reconcile any differences monthly.

**Why:** Don't let decisions that matter rely on a lagging view, and tell users what might be stale. See [[cqrs]] and [[cap-theorem]].

## Reads are 50 times writes, but every screen reads the same shape as the table. What should the team try first?

- [x] Read replicas or caching.
- [ ] A separate CQRS read model.
- [ ] Event sourcing for every table.
- [ ] Sharding the main database.

**Why:** A separate read model is for when the shape of reads differs, not just the volume. Replicas and caches handle volume more cheaply. See [[cqrs]], [[relational-databases]], and [[caching]].

## A team wants a separate read model but no event store. Can it use CQRS?

- [x] Yes; CQRS separates reads from writes, and event sourcing is a separate idea.
- [ ] No; CQRS is defined by storing every change as an event in an event store.
- [ ] Only if the read and write sides use separate databases from the first day.
- [ ] Only if every part of the system adopts CQRS, so the design stays consistent.

**Why:** Event sourcing stores the history of events as the source of truth; it pairs well with CQRS but isn't required. Start small, even in one transaction. See [[cqrs]].
