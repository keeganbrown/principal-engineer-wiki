# Quiz: Agent Instruction Files

## A team's agent instruction file is 400 lines pasted from their wiki. What's the better approach?

- [x] Rewrite it to about 40 lines: commands, conventions, and what the code can't tell you.
- [ ] Add more detail so the agent has every piece of context.
- [ ] Split it into ten files, one per topic, all loaded every session.
- [ ] Delete it; agents can learn everything from the code.

**Why:** Keep it short and lead with the commands. Agents ignore much of a long file, and nobody can tell which part. See [[agent-instruction-files]].

## An agent keeps making the same mistake in review. What should you do?

- [x] Turn the repeated correction into a line in the instruction file, or a check.
- [ ] Correct it in the chat each time it happens.
- [ ] Switch to a different model.
- [ ] Add the correction to a personal file only you use.

**Why:** The agent remembers nothing between sessions. Repeated corrections belong in the file — and hard rules belong in checks. See [[agent-instruction-files]].

## Why isn't the instruction file enough to enforce a rule like "never edit generated code"?

- [x] It's a request the model may ignore; enforcement needs hooks, permissions, or CI checks.
- [ ] Instruction files can only contain build commands.
- [ ] Agents never read instruction files after the first session.
- [ ] Generated code can't be described in Markdown.

**Why:** "Treating it as enforcement" is a listed trap. Use the file to explain, and tools to enforce. See [[agent-instruction-files]] and [[shared-agent-configuration]].
