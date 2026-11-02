# Quiz: Conway's Law

## A company has separate frontend, backend, and database teams. What does Conway's law predict?

- [x] Every feature needs hand-offs, and large interfaces form along team lines.
- [ ] The three layers slowly merge into one codebase, since the teams share a product.
- [ ] Features ship faster, because each team specializes in one layer of the stack.
- [ ] The architecture follows the product requirements, whatever the teams look like.

**Why:** Systems mirror the communication structure of the teams that build them. Layer teams produce layer boundaries, big contracts that change often, and three backlogs per feature. See [[conways-law]].

## What is the "inverse Conway maneuver"?

- [x] Shaping teams around the architecture you want, so the system follows.
- [ ] Redrawing the architecture to match whatever org chart you already have.
- [ ] Merging every team into one, so that no boundaries form in the code.
- [ ] Giving each microservice its own team, to force loose coupling between them.

**Why:** Since structure follows communication, you can design the teams first and let the system follow. It isn't free: specialists get spread thin and shared infrastructure can lose its owner. See [[conways-law]].

## When is a non-domain team, like a platform or security team, the right call?

- [x] When expertise is scarce or a capability is shared by everyone.
- [ ] Rarely; domain teams should absorb platform work as they grow.
- [ ] Only once the company has grown past a dozen product teams or so.
- [ ] Whenever a domain team is too busy to take on more work this quarter.

**Why:** The goal is fewer hand-offs on the common path, not organizational purity. See [[conways-law]].
