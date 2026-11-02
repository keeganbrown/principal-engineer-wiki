# Quiz: Spec-First Agent Tasks

## An agent adds an in-memory rate-limit counter, but the service runs on eight instances. What would have caught it?

- [x] An explore step first: read the deployment config and report back before changing anything.
- [ ] A longer prompt telling the agent to be careful.
- [ ] More unit tests of the in-memory counter.
- [ ] Letting the agent finish and fixing it in review.

**Why:** Correcting a plan is cheaper than correcting code. Exploring first surfaces facts like eight instances and an existing shared store. See [[spec-first-agent-tasks]].

## Who should define what "done" means for an agent task?

- [x] You, as acceptance criteria written before implementation.
- [ ] The agent, once it has finished the work.
- [ ] Whoever reviews the pull request afterward.
- [ ] Nobody; green tests define done.

**Why:** A clear "done" lets the agent check itself. Letting the agent define it is a listed trap. See [[spec-first-agent-tasks]].

## A plan is going badly and the agent keeps patching its mistakes. What's often best?

- [x] Restart with a better spec instead of arguing in the same session.
- [ ] Keep correcting it until the session runs out of context.
- [ ] Approve the change and fix it later.
- [ ] Switch to writing the code by hand forever.

**Why:** A fresh start with a clearer plan is often cheaper than steering a confused session. See [[spec-first-agent-tasks]].
