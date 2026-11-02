# Quiz: Big Ball of Mud

## A team wants to escape a big ball of mud in its busiest area. What's the best first step?

- [x] Add a lint rule for one boundary, with an allow list for existing violations.
- [ ] Fix every existing violation first, then turn on a check so no new ones appear.
- [ ] Split the codebase into microservices so the network enforces the boundaries.
- [ ] Draw the target architecture on a diagram and ask every team to follow it.

**Why:** Stop new violations now and fix old ones where teams are already working. Pick the area by churn, and agree with product that the first features there will slow down. See [[big-ball-of-mud]].

## A lint rule starts with an allow list of 37 known boundary violations. What usually goes wrong?

- [x] With no deadline it becomes permanent, and new code copies the old violations.
- [ ] It blocks every build until the last known violation has been fixed.
- [ ] It grows quickly, because the rule forces every new feature to add an entry.
- [ ] It hides the violations from the team that owns the affected module.

**Why:** "It's done that way already" spreads. Review the count regularly, refuse new entries, and shrink it as teams touch the files. See [[big-ball-of-mud]].

## When is leaving mud alone reasonable?

- [x] In a stable corner that nobody changes.
- [ ] In the module that changes most, since the team already knows it well.
- [ ] In any code older than five years, since its authors have moved on.
- [ ] In shared modules that many teams import, since changing them is risky.

**Why:** Mud costs you on every change, so code that rarely changes costs little. Throwaway prototypes are fine as mud too. See [[big-ball-of-mud]].
