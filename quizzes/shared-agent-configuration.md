# Quiz: Shared Agent Configuration

## A shared config denies the agent reading `.env` files. Does that keep the secrets in it safe?

- [x] Not fully; a script the agent runs can still read the file.
- [ ] Yes; deny rules apply to every process the agent ever starts.
- [ ] Yes, as long as the `.env` file is listed in `.gitignore`.
- [ ] No; deny rules only work when they live in a personal file.

**Why:** The deny rule stops the agent's file tools, not its commands. Keeping secrets truly out of reach takes a sandbox, or not having the file in the agent's environment. See [[shared-agent-configuration]] and [[agent-guardrails]].

## What belongs in the shared, checked-in configuration?

- [x] Team permissions, hooks, and reusable commands.
- [ ] A permission one engineer finds convenient for their work.
- [ ] API keys for the tools the agent connects to.
- [ ] Each engineer's personal experiments with new settings.

**Why:** Team rules go in the committed file; personal preferences, experiments, and anything with credentials go in the ignored one. See [[shared-agent-configuration]].

## How should a team treat a new tool connection, such as a Model Context Protocol (MCP) server?

- [x] Vet it like a dependency: prefer official, pin it, and limit access.
- [ ] Install it if it's popular, since public registry tools are reviewed.
- [ ] Let each engineer install whatever they like, without any review.
- [ ] Avoid all tool connections, since none of them can ever be trusted.

**Why:** Tool descriptions and output are untrusted input, and a connection with both data access and internet access recreates the lethal trifecta. See [[shared-agent-configuration]].

## A team commits a format hook that runs on every edit. What cost should they plan for?

- [x] A broken or slow hook breaks every teammate's agent.
- [ ] Hooks can't run in CI, so formatting drifts between machines.
- [ ] Agents ignore hooks they didn't write themselves.
- [ ] Each engineer must approve the hook before every edit.

**Why:** A committed hook is code that runs automatically on everyone's machine, so keep it fast and review it like a CI script. See [[shared-agent-configuration]].
