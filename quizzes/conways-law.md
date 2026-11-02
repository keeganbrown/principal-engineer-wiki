# Quiz: Conway's Law

## A company has separate frontend, backend, and database teams. What does Conway's law predict?

- [x] Every feature needs hand-offs, and the system grows chatty interfaces along those team lines.
- [ ] The three layers will slowly merge into one codebase because the teams share a product.
- [ ] Features will ship faster, because each team specializes in one layer of the stack.
- [ ] The architecture will be shaped by the product requirements, regardless of the teams.

**Why:** Systems mirror the communication structure of the teams that build them. Layer teams produce layer boundaries and three backlogs per feature. See [[conways-law]].

## What is the "inverse Conway maneuver"?

- [x] Shaping teams around the architecture you want, so the system grows toward it.
- [ ] Redrawing the architecture to match whatever org chart you already have.
- [ ] Merging every team into one so that no boundaries form in the code.
- [ ] Assigning each microservice to a different team to force loose coupling.

**Why:** Since structure follows communication, you can design the teams first and let the system follow. It isn't free: specialists get spread thin and shared infrastructure can lose its owner. See [[conways-law]].

## When is a non-domain team, like a platform or security team, the right call?

- [x] When expertise is scarce or a capability is shared by everyone.
- [ ] Never; every team should own one business domain end to end.
- [ ] Only for companies with fewer than one team of engineers.
- [ ] Whenever a domain team is too busy to take on more work.

**Why:** The goal is fewer hand-offs on the common path, not organizational purity. Platform and deep-specialty teams are legitimate where knowledge is scarce or shared. See [[conways-law]].
