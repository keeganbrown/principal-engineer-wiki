# Quiz: Reviewing AI-Generated Code

## Who owns code an agent wrote?

- [x] The engineer who opened the pull request.
- [ ] The vendor of the coding agent.
- [ ] The reviewer who approved it.
- [ ] Nobody, until a human edits it.

**Why:** The author owns it, no matter who or what typed it. Blame-shifting to the agent is a listed trap. See [[reviewing-ai-generated-code]].

## An agent-built pagination PR has green tests but uses page numbers, while the ticket asked for cursors. How did the reviewer catch it?

- [x] By reviewing intent first, checking the change against the ticket before the details.
- [ ] By reading the agent's summary of what it changed.
- [ ] By running the tests a second time.
- [ ] By checking the code's formatting and naming.

**Why:** Agent errors look plausible and pass tests. Review intent, then details, and read the diff, not the summary. See [[reviewing-ai-generated-code]].

## How should AI code reviewers be used?

- [x] As a first pass that finds issues, not as the approval.
- [ ] As the only reviewer for agent-written code.
- [ ] As a replacement for tests.
- [ ] Not at all; they always miss bugs.

**Why:** AI reviewers help with volume, but a human still owns the approval. See [[reviewing-ai-generated-code]].
