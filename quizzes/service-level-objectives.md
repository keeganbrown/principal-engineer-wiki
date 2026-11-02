# Quiz: Service Level Objectives (SLOs)

## A product lead asks for checkout to be "100% reliable." What should the principal engineer propose instead?

- [x] A target just below recent performance, with an agreed error budget.
- [ ] A 100% target, with every incident reviewed by the executive team.
- [ ] Whatever availability the cloud provider promises for its databases.
- [ ] No target at all, since any outage at all is unacceptable for checkout.

**Why:** Perfect can't be achieved and blocks every risky change, while users can't tell the difference past a point. Set the target from history, a little below what you achieved while users were content, and spend the gap on change. See [[service-level-objectives]].

## A team's checkout SLO counts fast responses as good. A bug starts charging some customers twice, and the SLO stays green. What does this show?

- [x] The indicator misses failures it can't see, so add a correctness check.
- [ ] The SLO is too loose, so raise the target from 99.9% to 99.99%.
- [ ] Double charges are rare enough that the SLO can safely ignore them.
- [ ] The SLO should be measured from server logs instead of the load balancer.

**Why:** Fast, wrong answers count as good unless you measure correctness. An SLO covers only what its indicator measures, so choosing the indicator is most of the work. See [[service-level-objectives]].

## How should a team get paged on its SLO?

- [x] When the error budget is burning fast enough to run out within hours.
- [ ] Every time a single request fails, so that no error goes unnoticed.
- [ ] Whenever any server's CPU rises above 80% for more than a minute.
- [ ] Only at the end of the window, once the SLO is known to be missed.

**Why:** Alert on burn rate: page when the budget is draining fast and open a ticket for slow burns. Paging on every error or on machine metrics wakes people for things users don't feel. See [[service-level-objectives]] and [[observability]].

## A new internal product gets about a hundred requests a day. Should the team set up SLOs with burn-rate alerts now?

- [x] Not yet; at that traffic one failure swings the ratio, so alert on user-facing errors.
- [ ] Yes; every service needs SLOs and burn-rate alerts from its first day running.
- [ ] Yes, and set a 99.99% target so problems are caught as early as possible.
- [ ] No; internal products never need a reliability target of any kind at all.

**Why:** At a hundred requests a day, one failure is a 1% swing, so a couple of alerts on user-facing errors are enough until traffic grows. See [[service-level-objectives]].
