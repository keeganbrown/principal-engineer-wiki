# Quiz: Command Query Responsibility Segregation (CQRS)

## A product page assembles data from four services and takes 800ms. How does CQRS help?

- [x] A projector keeps one pre-built read document per product, so the page is a single fast lookup.
- [ ] All four services merge into one database so the query can join everything.
- [ ] The page caches each service's response for 24 hours.
- [ ] Writes go through the read model, so the page is always current.

**Why:** Separate the read model from the write side when their needs diverge. The price is that the read view can lag by a few seconds. See [[cqrs]].

## The read model can lag by a few seconds. What should checkout do?

- [x] Re-check price and stock with the owning services before charging.
- [ ] Trust the product page, since it was correct when the user loaded it.
- [ ] Block the page until the read model is fully up to date.
- [ ] Charge the displayed price and reconcile differences monthly.

**Why:** Set expectations for staleness and don't let decisions that matter rely on a lagging view. See [[cqrs]].

## Which statement about CQRS is true?

- [x] It doesn't require event sourcing; the two are often confused.
- [ ] It should be applied to every part of a system for consistency.
- [ ] It requires separate databases from day one.
- [ ] It makes read-your-writes automatic for every user.

**Why:** Start small, even in one transaction, and use CQRS only where read and write needs genuinely diverge. See [[cqrs]].
