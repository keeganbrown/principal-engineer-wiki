# Quiz: Modular Monolith

## How does `orders` get a payment made in a modular monolith?

- [x] It calls `payments.charge(...)` through the module's public API.
- [ ] It writes directly to the payments tables in a shared transaction.
- [ ] It imports the payments module's internal classes and calls them.
- [ ] It sends an HTTP request to a payments microservice.

**Why:** Modules talk through public interfaces and own their own tables. A CI check can fail builds that reach into another module's internals. See [[modular-monolith]].

## A payments module is extracted from a modular monolith into its own service. What usually takes longest?

- [x] Places where two modules still share a database transaction.
- [ ] Moving the payments code, which is tangled with every other module.
- [ ] Rewriting payments in a new language for the new service.
- [ ] Getting a new CI system to build the extracted service.

**Why:** Clean boundaries let the code move quickly; each shared transaction must become a saga. Avoid cross-module transactions from the start. See [[modular-monolith]] and [[saga-pattern]].

## What risk does a modular monolith still share with a big ball of mud?

- [x] A memory leak in one module can take down all of them.
- [ ] Modules can't share a database transaction with each other.
- [ ] Network calls between modules add latency to every request.
- [ ] Each module needs its own deploy pipeline and on-call rotation.

**Why:** One deployable means one process, so modules share runtime fate. Monitor per module, and keep risky work isolated. See [[modular-monolith]].
