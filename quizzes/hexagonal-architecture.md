# Quiz: Hexagonal Architecture (Ports and Adapters)

## Who defines a port in hexagonal architecture?

- [x] The core, in the language of the business use case.
- [ ] The database vendor, to match its client library.
- [ ] The web framework, to match its request objects.
- [ ] Each adapter, so it can expose its own features.

**Why:** Ports are shaped by what the core needs, not by the technology. Shaping ports like the technology is a listed trap. See [[hexagonal-architecture]].

## What's the main testing benefit?

- [x] Use cases can be tested with in-memory fakes, without a database or network.
- [ ] End-to-end tests become unnecessary for every feature.
- [ ] Adapters no longer need any tests at all.
- [ ] Tests can call private methods inside the core.

**Why:** The core talks only to interfaces it defines, so tests plug in fakes. Adapters still need their own integration tests. See [[hexagonal-architecture]].

## Does a port make swapping the real database free?

- [x] No; semantics like transactions and consistency leak, so swaps get cheaper, not free.
- [ ] Yes; any database can be swapped in a day behind a port.
- [ ] Yes, as long as the adapter is generated automatically.
- [ ] No, because ports can only wrap HTTP APIs.

**Why:** Adapters can be swapped, partly. You still need to decide what must succeed or fail together across ports. See [[hexagonal-architecture]].
