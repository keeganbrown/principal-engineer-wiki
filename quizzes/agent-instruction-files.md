# Quiz: Agent Instruction Files

## A team's agent instruction file is 400 lines pasted from their wiki. What's the better approach?

- [x] Cut it to commands, conventions, and what the code can't tell you.
- [ ] Add more detail, so the agent has every piece of context it might need.
- [ ] Split it into ten files, one per topic, all loaded at every session start.
- [ ] Delete it, since agents can learn everything they need from the code.

**Why:** Keep it short and lead with the commands; in the example it ended near 40 lines. Agents ignore much of a long file, and nobody can tell which part. Move the style guide into the linter. See [[agent-instruction-files]].

## An agent keeps making the same mistake in review. What should you do?

- [x] Turn the repeated correction into a line in the file, or a check.
- [ ] Correct it in the chat each time, since that's where it happened.
- [ ] Switch to a larger model that makes fewer mistakes of this kind.
- [ ] Add the correction to a personal file that only you load.

**Why:** The agent remembers nothing between sessions. Repeated corrections belong in the shared file, and hard rules belong in checks. See [[agent-instruction-files]].

## Why can't an instruction file alone guarantee that tests run before every commit?

- [x] It's advice the model may ignore; a CI check that fails is a guarantee.
- [ ] Instruction files load only at session start, so later edits are missed.
- [ ] Agents stop reading instruction files after their very first session.
- [ ] Instruction files may only contain build commands, not working rules.

**Why:** Use the file to explain, and tools (tests, linters, type checks, permission settings) to enforce. See [[agent-instruction-files]] and [[shared-agent-configuration]].

## A lead says committing a rules file will halve how fast agent-written code grows more complex. How should you treat the claim?

- [x] As plausible but unproven, since the evidence is observational.
- [ ] As proven, since a large study measured it across many repositories.
- [ ] As false, since agents ignore rules files in most of their sessions.
- [ ] As irrelevant, since rules files only change how often agents commit.

**Why:** A 2026 Stanford and Carnegie Mellon study found complexity rose about half as much in agent-heavy repositories with a committed rules file, but disciplined teams may simply write more rules files; the authors treat it as a hypothesis. Either way, rules that must hold belong in tools. See [[agent-instruction-files]].
