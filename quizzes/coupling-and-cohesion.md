# Quiz: Coupling and Cohesion

## Orders and Shipping both read and write the same `orders` table. Shipping adds a column and Orders' reports break. What kind of coupling is this?

- [x] Hidden coupling through shared storage that neither codebase shows.
- [ ] High cohesion, since both services keep related order data in one place.
- [ ] Loose coupling, since the services talk only through the database.
- [ ] A versioning bug that a library upgrade would have prevented by itself.

**Why:** Shared storage couples services invisibly. The usual fix is for one service to own the table and publish events or an API. See [[coupling-and-cohesion]].

## Orders and Shipping shared an `orders` table. Orders now owns it and publishes an `OrderPlaced` event. What happens to the coupling?

- [x] It moves into the event contract, which still needs versioning.
- [ ] It disappears completely, because events decouple producers from consumers.
- [ ] It shrinks to zero for reads, but stays the same as before for writes.
- [ ] It becomes Shipping's problem alone, since Orders no longer shares a table.

**Why:** Coupling rarely disappears; it moves. The win is that the new dependency is one documented, narrow contract, and Shipping's copy is eventually consistent. See [[coupling-and-cohesion]] and [[api-versioning]].

## When is tight coupling acceptable?

- [x] Between private helpers in a small module that change together.
- [ ] Between two teams' services, as long as they always deploy together.
- [ ] Only when the module will be extracted into a service soon.
- [ ] Whenever the coupling goes through a database rather than through code.

**Why:** Loosening coupling adds indirection: an interface, an event, a copy of data. Inside a small module, that price usually isn't worth paying. See [[coupling-and-cohesion]].
