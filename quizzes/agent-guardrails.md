# Quiz: Agent Guardrails

## An agent's test called the real delete function and wiped files in the user's home directory. Which change makes the test itself safe to run?

- [x] Put deletion behind an interface, so tests inject a spy.
- [ ] Add a line to the instruction file saying never to delete files.
- [ ] Ask the agent to review its own tests carefully before running them.
- [ ] Stop running the test suite whenever an agent session is active.

**Why:** Instructions are not limits. The team also sandboxed agents to the repository, so even a bad path can't reach the home directory: layers, not one fix. See [[agent-guardrails]].

## An agent reads public issues and the private repository, and its network is allowlisted to the package registry. Is the lethal trifecta broken?

- [x] Narrowed, not closed; the registry can still carry data out.
- [ ] Yes; an allowlist removes the outbound path, so nothing can leak.
- [ ] Yes, because public issues don't count as untrusted content.
- [ ] No, and it can't be narrowed without removing the agent entirely.

**Why:** The trifecta is private data, untrusted content, and a way out. For most coding agents the repository is the private data, so keep what's at stake small. See [[agent-guardrails]].

## When can an agent safely run with few limits?

- [x] In a disposable container with no credentials or anything of value.
- [ ] On a senior engineer's laptop, since they know what they're doing.
- [ ] When the network is allowlisted to the package registry only.
- [ ] When the repository is private and only employees can read it.

**Why:** Scale the guardrails to what the agent can reach. A throwaway sandbox is the guardrail. See [[agent-guardrails]].
