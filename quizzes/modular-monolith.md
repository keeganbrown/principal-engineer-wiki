# Quiz: Modular Monolith

## In a modular monolith, the `orders` module needs to charge a payment. How should it do that?

- [x] Call `payments.charge(...)` through the payments module's public API.
- [ ] Write directly to the payments tables in the same transaction as the order.
- [ ] Import the payments module's internal classes and call them directly.
- [ ] Send an HTTP request to a new payments microservice built for this.

**Why:** Modules talk through public interfaces and own their own tables. A build check can fail any change that reaches into another module's internals. See [[modular-monolith]].

## A payments module with a clean code boundary is extracted from a modular monolith into its own service. What is likely to take longest?

- [x] Places where two modules still share a database transaction.
- [ ] Moving the payments code, which is tangled with every other module.
- [ ] Rewriting payments in a new language for the new service.
- [ ] Setting up a new build pipeline for the extracted service.

**Why:** Clean boundaries let the code move quickly; each shared transaction must become a saga. Avoid cross-module transactions from the start. See [[modular-monolith]] and [[saga-pattern]].

## What risk does a modular monolith still share with a big ball of mud?

- [x] A memory leak in one module can take down all of them.
- [ ] Modules can't share a database transaction with each other.
- [ ] Network calls between modules add latency to every request.
- [ ] Each module needs its own deploy pipeline and on-call rotation.

**Why:** One deployable means one process, so modules share runtime fate. Monitor per module, and keep risky work isolated. See [[modular-monolith]].

## Two teams share a modular monolith. One module needs to scale to fifty times the others' load, and its team is regularly blocked by the shared deploy. Should they keep it in the monolith?

- [x] Probably not; very different scaling plus a blocked team is a nameable reason to extract.
- [ ] Yes; a modular monolith should never be split once its boundaries are clean.
- [ ] Yes, and add more servers until the whole monolith handles the load.
- [ ] No; every module should become its own service once there are two teams.

**Why:** "Monolith first," not "monolith forever." Very different scaling needs, or teams truly blocked by one deployment, can make a service worth its cost. See [[modular-monolith]] and [[microservices]].
