# Quiz: Agent Guardrails

## An agent ran a test that deleted files in the user's home directory. Which guardrail addresses the root cause?

- [x] Put destructive operations behind an interface so tests inject a spy instead of deleting real files.
- [ ] Add a line to the instruction file telling the agent never to delete files.
- [ ] Ask the agent to review its own tests before running them.
- [ ] Stop running tests during agent sessions.

**Why:** Instructions are not limits. Make tests safe to run by anyone, and run unattended agents in a sandbox. See [[agent-guardrails]].

## What is the "lethal trifecta"?

- [x] Access to private data, exposure to untrusted content, and a way to send data out.
- [ ] Slow tests, flaky tests, and missing types.
- [ ] Read access, write access, and admin access.
- [ ] Hooks, permissions, and tool connections.

**Why:** With all three, prompt injection can leak data. Remove any one and that leak path closes. See [[agent-guardrails]].

## When can an agent safely run with few limits?

- [x] In a disposable container with no credentials and nothing valuable in it.
- [ ] On a senior engineer's laptop, since they know what they're doing.
- [ ] Whenever the task description says to be careful.
- [ ] Whenever the repository is private.

**Why:** Scale the guardrails to what the agent can reach. A throwaway sandbox *is* the guardrail. See [[agent-guardrails]].
