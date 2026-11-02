# Quiz: Distributed Monolith

## Which sign most strongly suggests a distributed monolith?

- [x] Releases need a runbook that deploys services in a fixed order.
- [ ] Each service has its own deploy pipeline.
- [ ] Services publish events that others consume at their own pace.
- [ ] Each service owns its own database.

**Why:** Services that must change and deploy together pay for distribution without getting independence. See [[distributed-monolith]].

## `order-service` blocks on `pricing-service`, and prices only matter at order time. What did the team do?

- [x] Merged pricing back into the order service, migrating its data as the hard part.
- [ ] Added a service mesh to manage retries between them.
- [ ] Split pricing into two smaller services.
- [ ] Added a shared library so both services share the pricing model.

**Why:** Merge services that always change together. Treating a merge as defeat, or adding a mesh to manage the pain, are listed traps. See [[distributed-monolith]].

## When is lockstep deployment acceptable?

- [x] As a temporary state mid-migration, with an end date.
- [ ] As the normal way every feature ships.
- [ ] Whenever a shared library changes.
- [ ] Never, under any circumstances.

**Why:** Some coupling is fine. The problem is coupling as the normal case, not the exception. See [[distributed-monolith]].
