# Quiz: Spec-First Agent Tasks

## An agent adds an in-memory rate-limit counter, but the service runs on eight instances. What would have caught it before any code was written?

- [x] An explore step that reads the deployment config and reports back.
- [ ] A longer prompt telling the agent to be careful with shared state.
- [ ] More unit tests of the in-memory counter, written up front.
- [ ] A larger model, which would have guessed the instance count.

**Why:** Correcting a plan is cheaper than correcting code. Check the facts the report rests on yourself, since the exploration is model output too. See [[spec-first-agent-tasks]].

## Who should define what "done" means for an agent task?

- [x] You, as acceptance criteria written before the work.
- [ ] The agent, once it has finished the implementation.
- [ ] Whoever reviews the pull request afterward.
- [ ] Nobody; passing tests are what define done.

**Why:** A clear "done" lets the agent check itself. If the agent defines it, it can declare success on anything. See [[spec-first-agent-tasks]].

## You've corrected the agent twice on the same task and it's still off. What now?

- [x] Write a better spec and start a fresh session.
- [ ] Keep correcting it until the session runs out of context.
- [ ] Approve the change now and plan to fix it later.
- [ ] Switch to a different agent tool and paste the same prompt.

**Why:** Failed attempts stay in the session's context and seem to keep steering the agent; the same prompt elsewhere repeats the same gaps. A fresh session with a clearer spec starts clean. See [[spec-first-agent-tasks]].

## You're unsure how to approach a small change that's cheap to throw away. Should you plan first?

- [x] Not necessarily; a quick throwaway attempt can teach more.
- [ ] Yes; every agent task needs an explore step and a written plan.
- [ ] Yes, because skipping the plan makes the change irreversible.
- [ ] No; plans are only worth it for changes over a thousand lines.

**Why:** Plan first when a wrong attempt is expensive to review or hard to undo. For a one-line fix, a planning phase is ceremony. See [[spec-first-agent-tasks]].
