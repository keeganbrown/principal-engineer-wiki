# Quiz: Coupling and Cohesion

## Orders and Shipping both read and write the same `orders` table. Shipping adds a column and Orders' reports break. What is this?

- [x] Shared-database coupling: hidden coupling through storage that neither codebase shows.
- [ ] High cohesion: both services keep related order data together in one place.
- [ ] Loose coupling: the services talk only through the database, never directly.
- [ ] A versioning bug that an ORM upgrade would have prevented on its own.

**Why:** Shared storage couples services invisibly. The usual fix is for one service to own the table and publish events or an API. See [[coupling-and-cohesion]].

## Orders takes ownership of the table and publishes an `OrderPlaced` event. What happens to the coupling?

- [x] It moves to the event contract, where it is explicit and narrow but still needs versioning.
- [ ] It disappears completely, because events decouple producers from consumers.
- [ ] It doubles, because Shipping now depends on both the table and the event.
- [ ] It becomes Shipping's problem only, since Orders no longer reads the table.

**Why:** Coupling rarely disappears; it moves. The win is that the new dependency is one documented contract, and Shipping's copy is eventually consistent. See [[coupling-and-cohesion]] and [[api-versioning]].

## When is tight coupling acceptable?

- [x] Between private helpers inside a small module that always change together.
- [ ] Between two services owned by different teams, as long as they deploy together.
- [ ] Never; zero coupling is the goal for any well-designed system.
- [ ] Whenever the coupling goes through a database rather than through code.

**Why:** Loosening coupling adds indirection — an interface, an event, a copy of data. Inside a small module, that price usually isn't worth paying. See [[coupling-and-cohesion]].
