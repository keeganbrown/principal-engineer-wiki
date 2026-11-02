# Quiz: Reviewing AI-Generated Code

## An engineer merges an agent-written change that later causes an incident. Who owns the fix?

- [x] The engineer who opened the pull request.
- [ ] The vendor whose coding agent wrote the change.
- [ ] The reviewer who approved the pull request.
- [ ] Nobody in particular, since no human typed the code.

**Why:** The author owns the code, no matter who or what typed it. Blaming the agent leaves nobody accountable. See [[reviewing-ai-generated-code]].

## An agent-built pagination change has green tests but uses page numbers, while the ticket asked for cursors. What review habit catches this?

- [x] Checking the change against the ticket before reading details.
- [ ] Reading the agent's own summary of what it changed and why.
- [ ] Running the full test suite a second time before approving.
- [ ] Checking the code's formatting and naming against the style guide.

**Why:** Agent errors look plausible and pass tests. Review intent, then details, and read the diff, not the summary. See [[reviewing-ai-generated-code]].

## How should AI code reviewers be used?

- [x] As a first pass that finds issues, not as the approval.
- [ ] As the required approver, but only for small agent changes.
- [ ] As a replacement for tests on code that agents wrote.
- [ ] Not at all, since they miss too many bugs to be useful.

**Why:** AI reviewers catch real issues cheaply, but a human who understands the system still owns the merge. See [[reviewing-ai-generated-code]].

## Security wants to ban agents from the payments module. What usually works better?

- [x] Stricter review for that path; enforce any real ban with tooling.
- [ ] A memo to all engineers saying that agents may not touch payments.
- [ ] Letting agents in freely, since review catches everything anyway.
- [ ] Banning agents from the whole repository, so the rule is simple.

**Why:** Blanket bans are hard to enforce and push use into hiding. Where a ban is genuinely required, by regulation or contract, enforce it with tooling and access. See [[reviewing-ai-generated-code]].

## Agent use has doubled each reviewer's load, and a review bot now checks most pull requests. What should the team do?

- [x] Budget reviewer hours and write down which changes the bot may approve.
- [ ] Let the bot approve everything, since agent changes are rarely reverted.
- [ ] Speed up approvals by reading each change's summary instead of its diff.
- [ ] Add a second review bot so humans can stop reading routine changes.

**Why:** Plan review capacity alongside authoring. Bots are a first pass, not the approval, and the description is a claim while the diff is the evidence; check what humans have stopped reading. See [[reviewing-ai-generated-code]].
