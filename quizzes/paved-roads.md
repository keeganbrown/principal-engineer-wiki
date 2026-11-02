# Quiz: Paved Roads

## A 12-person startup, where everyone talks daily, is thinking about building a maintained service template. Should it?

- [x] Probably not yet; a short shared doc is likely enough.
- [ ] Yes; every company needs a paved road before its second service.
- [ ] Yes, and it should be mandatory so nobody drifts from it.
- [ ] No; paved roads only work at companies with platform teams.

**Why:** A paved road is a product with an owner, upgrades, and support. Below a certain size, that overhead isn't worth it. See [[paved-roads]].

## A service template is used by 90% of new services, but few existing services adopt it. What usually changes that?

- [x] An upgrade that gives them something they want.
- [ ] A mandate with a firm deadline to migrate.
- [ ] More documentation about how the template works.
- [ ] Forbidding new features in services off the road.

**Why:** Adoption follows value. Keeping generated repos upgradable is ongoing work: shared logic moves into versioned libraries the platform team supports. See [[paved-roads]].

## How should a paved road handle teams with needs it doesn't cover?

- [x] Allow exits, but the team meets the guardrails and owns its own upgrades.
- [ ] Forbid exits, so that every service stays consistent with every other.
- [ ] Let anyone leave the road freely, with no extra responsibilities at all.
- [ ] Build a separate new road for every team that asks for something different.

**Why:** Free exits fragment the standard; no exits turns the road into a mandate with extra steps. A team that leaves still meets the mandatory checks, and you learn from why it left. See [[paved-roads]].
