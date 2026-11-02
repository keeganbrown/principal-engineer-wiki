# Quiz: Shared Agent Configuration

## Agents keep editing generated API clients that get overwritten on the next build. Which fix enforces the rule?

- [x] A hook that blocks edits under the generated folder, with a message pointing to the schema.
- [ ] A sentence in the instruction file asking agents not to edit generated code.
- [ ] A weekly reminder in the team channel.
- [ ] Making the generated folder read-only on one engineer's laptop.

**Why:** Hooks enforce what instructions only request. The message tells the agent what to do instead. See [[shared-agent-configuration]].

## What belongs in the shared, checked-in configuration?

- [x] Team permissions, hooks, and reusable commands.
- [ ] Each engineer's favorite editor theme and shortcuts.
- [ ] API keys for the tools the agent connects to.
- [ ] Personal notes about which tasks each engineer is working on.

**Why:** Split team settings from personal ones, and keep secrets out. See [[shared-agent-configuration]].

## How should a team treat a new tool connection, such as an MCP server?

- [x] Vet it like a dependency: who maintains it, what it can access, and what it sends out.
- [ ] Install it if it's popular; tools from public registries are safe.
- [ ] Let each engineer install whatever they like, unreviewed.
- [ ] Avoid all tool connections, since none can be trusted.

**Why:** A tool connection is code that runs with the agent's access. Installing them casually is a listed trap. See [[shared-agent-configuration]].
