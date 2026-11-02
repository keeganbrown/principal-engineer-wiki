# Quiz: Modular Monolith

## How does `orders` get a payment made in a modular monolith?

- [x] It calls `payments.charge(...)` through the payments module's public API.
- [ ] It writes directly to the payments tables in a shared transaction.
- [ ] It imports the payments module's internal classes.
- [ ] It sends an HTTP request to a payments microservice.

**Why:** Modules talk through public interfaces and own their own tables. A CI check can fail builds that reach into another module's internals. See [[modular-monolith]].

## Two years later, payments is extracted into a service. What was the slow part?

- [x] Two places where orders and payments still shared a database transaction.
- [ ] Moving the payments code, which was tangled with every other module.
- [ ] Rewriting payments in a new language for the new service.
- [ ] Getting a new CI system to build the extracted service.

**Why:** Clean code boundaries make the code move fast; shared transactions must become sagas. Avoid cross-module transactions from the start. See [[modular-monolith]].

## What runtime risk does a modular monolith still share with a big ball of mud?

- [x] Shared runtime fate: a memory leak in one module can take down all of them.
- [ ] Separate deploys for every module, which adds pipeline work.
- [ ] Network calls between modules, which add latency.
- [ ] Each module needing its own on-call rotation.

**Why:** One deployable means one process. "Forgetting shared runtime fate" is a listed trap. See [[modular-monolith]].
