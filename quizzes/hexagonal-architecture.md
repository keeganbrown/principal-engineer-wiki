# Quiz: Hexagonal Architecture (Ports and Adapters)

## Who defines a port in hexagonal architecture?

- [x] The core, in the language of the business use case.
- [ ] The database vendor, to match its client library.
- [ ] The web framework, to match its request objects.
- [ ] Each adapter, so that it can expose its own features.

**Why:** Ports are shaped by what the core needs. A port shaped like the technology ties the core to that technology. See [[hexagonal-architecture]].

## What's the main testing benefit of ports and adapters?

- [x] Use cases can be tested with in-memory fakes, with no database.
- [ ] End-to-end tests are no longer needed for most features.
- [ ] Adapters can be tested through the core's fakes instead of on their own.
- [ ] Tests can call private methods inside the core directly.

**Why:** The core talks only to interfaces it defines, so tests plug in fakes. Adapters still need their own integration tests. See [[hexagonal-architecture]].

## Does a port make swapping the real database free?

- [x] No; transaction behavior leaks, and vendor-shaped ports need reshaping.
- [ ] Yes; any database can be swapped behind a well-designed port in about a day.
- [ ] Yes, as long as the adapter code is generated automatically.
- [ ] No, because ports can wrap remote HTTP services but not databases.

**Why:** Adapters can be swapped, partly. Don't justify a port by a swap you've never planned. See [[hexagonal-architecture]] and [[yagni]].

## A simple CRUD admin app has almost no business rules. Should every database call go through a port?

- [x] No; a thin layer over the database is fine until testing or change hurts.
- [ ] Yes; skipping ports now means a full rewrite later, once the app grows.
- [ ] Yes, but only for reads, since writes are too simple to need one.
- [ ] No; hexagonal architecture only works for large distributed systems.

**Why:** For simple CRUD apps the indirection can outweigh the benefit. Add ports where you feel pain: hard-to-test logic or infrastructure likely to change. See [[hexagonal-architecture]].
