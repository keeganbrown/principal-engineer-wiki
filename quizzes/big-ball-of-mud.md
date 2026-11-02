# Quiz: Big Ball of Mud

## A team wants to escape a big ball of mud. What does the wiki suggest first?

- [x] Draw the boundary you want and enforce one with a lint rule, starting with an allow list of known violations.
- [ ] Declare bankruptcy and rewrite the system cleanly from scratch.
- [ ] Split the codebase into microservices so the network enforces boundaries.
- [ ] Draw the target architecture on a diagram and ask teams to follow it.

**Why:** Stop the bleeding, then fix violations where you're already working. Rewrites and premature service splits are listed traps. See [[big-ball-of-mud]].

## What usually goes wrong with an allow list of known boundary violations?

- [x] Without a deadline it becomes permanent, and new code copies the old violations.
- [ ] It blocks every build until all violations are fixed.
- [ ] It hides the violations from the team that owns the module.
- [ ] Lint tools can't support allow lists.

**Why:** "It's done that way already" spreads. Give the allow list an end date and shrink it as teams touch the files. See [[big-ball-of-mud]].

## When is leaving mud alone reasonable?

- [x] In a stable corner nobody changes, since mud costs you on every change.
- [ ] In the module that changes most often, since it's already familiar.
- [ ] In any code older than five years.
- [ ] In shared modules that many teams import.

**Why:** Use churn to pick where boundaries pay off. Throwaway prototypes are also fine as mud. See [[big-ball-of-mud]].
