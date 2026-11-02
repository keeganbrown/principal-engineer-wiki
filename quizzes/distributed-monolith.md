# Quiz: Distributed Monolith

## Which sign most strongly suggests a distributed monolith?

- [x] Releases need a runbook that deploys services in a fixed order.
- [ ] Each service has its own deploy pipeline and its own on-call rotation.
- [ ] Services publish events that others consume at their own pace.
- [ ] Each service owns its own database and nobody else reads it.

**Why:** Services that must change and deploy together pay for distribution without getting independence. See [[distributed-monolith]].

## `order-service` calls `pricing-service` on every order, prices matter only at order time, and a bad pricing deploy stopped all orders. What should the team do?

- [x] Merge pricing into the order service, migrating its data.
- [ ] Add a service mesh so retries between the two are handled for them.
- [ ] Split pricing into two smaller services with narrower interfaces.
- [ ] Add a shared library so both services use the same pricing model.

**Why:** Pricing has no life outside an order, and its outage blocked every order, so the split buys nothing. The data migration is the hard part. A synchronous call alone isn't a reason to merge if you plan for the callee being down. See [[distributed-monolith]].

## When is lockstep deployment acceptable?

- [x] As a temporary state mid-migration, with an end date.
- [ ] As the normal way features ship, once the runbook is reliable.
- [ ] Whenever a shared library changes, since every service must upgrade.
- [ ] Never; needing it at all means the services should be merged.

**Why:** Some coupling is fine. The problem is coupling as the normal case, not the exception. See [[distributed-monolith]].
