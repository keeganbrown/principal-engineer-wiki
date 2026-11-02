---
title: Reviewing AI-Generated Code
category: coding-with-ai
summary: Whoever opens the pull request owns the code, no matter who or what typed it — so review agent output for intent and plausible-looking mistakes, and keep changes small enough that review stays real.
tags: [ai, coding-agents, code-review, ownership, quality]
---

# Reviewing AI-Generated Code

> **In one sentence:** Whoever opens the pull request owns the code, no matter who or what typed it — so review agent output for intent and plausible-looking mistakes, and keep changes small enough that review stays real.

## The idea

A **coding agent** is an AI tool that reads code, runs commands, and edits files in a loop toward a goal. It produces code that *looks* right: well named, well formatted, with tests. That polish is the problem. Human mistakes usually look like mistakes; agent mistakes often look like finished work.

Two rules follow:

- **The author owns it.** The engineer who opens the pull request (PR) is accountable for every line, exactly as if they'd typed it. "The AI wrote that" is never an answer in review or in an incident.
- **Review shifts from syntax to intent.** Formatting and obvious errors are cheap to catch automatically. The human's job is to ask: is this the right change, does it do what we meant, and what did it quietly get wrong?

## Why it matters

- **Review becomes the bottleneck.** In a 2026 Harvard study of 655 firms, code waited about 60% longer for a reviewer after agent adoption and drew about 39% more comments per change. At one company told to double its output (a 2026 Carnegie Mellon and Stanford study), each reviewer's load doubled, and while automated review grew from 19% to 84% of PRs, careful human review fell from 39% to 21%. Neither study, both observational, found more bugs or reverts; the cost showed up as review time, and unchecked it turns into rubber-stamping ([[adopting-coding-agents]] has the wider evidence).
- **Plausible errors slip past skimming.** Invented functions, wrong edge-case handling, and tests that check the wrong thing all read fluently.
- **Ownership keeps knowledge in the team.** If nobody understands the code that was merged, nobody can debug it at 3 a.m.

## How to apply it

- **Self-review before you ask anyone else.** Read your agent's diff line by line before opening the PR. If you can't explain a line, you're not ready to ask someone else to approve it.
- **Keep PRs small.** Agent PRs follow the same size rules as human ones ([[code-review]]). A 1,500-line generated PR gets a skim, not a review.
- **Say how the change was made.** A line in the PR description — "agent-written from the plan in #412; I rewrote the retry logic" — tells the reviewer where to look hardest. Make this a team norm, not a confession.
- **Review intent first, then details.** Check the change against the plan or ticket before reading the code. Agents often solve a slightly different problem very well.
- **Know the typical agent mistakes.** Watch for:
  - *Invented APIs or packages* — calls to functions or libraries that don't exist, or a package that doesn't exist yet. Attackers publish malicious packages under names agents commonly invent (sometimes called *slopsquatting*), so an install can pull in malware.
  - *Tests that prove nothing* — assertions on mocks, or expected values copied from the code's own output.
  - *Quiet scope creep* — "while I was there" refactors, changed defaults, new dependencies.
  - *Duplication* — a new helper written beside an existing one the agent didn't find ([[navigable-codebases]]).
  - *Weakened checks* — deleted assertions, skipped tests, broader exception handling, loosened types.
- **Use AI reviewers as a first pass, not an approval.** An AI review bot can catch real issues cheaply. It doesn't replace a human who understands the system and is accountable for the merge.
- **Plan review capacity with authoring.** When agent use grows, budget reviewer hours, not just licenses, and watch how long PRs wait for a first review. Those hours come out of feature work. If bots take on more review, write down which changes a bot may approve, and check what humans have stopped reading.
- **Keep checks the agent can't edit.** Branch protection and required reviewers for sensitive paths (repository settings that block merging until checks pass and named people approve), and CI (continuous integration) gates should not be changeable by the same change they guard.

## Example

An engineer asks an agent to "add pagination to the orders endpoint." The PR arrives: 300 lines, tests green, clean code.

The reviewer starts with intent and checks it against the ticket. The ticket says *cursor* pagination: each page returns a marker, such as the last order's ID, and the next request starts after it. Orders are inserted constantly, and with page numbers each new order shifts every row, so pages skip or repeat orders. The agent built page-number pagination: the tests pass because they insert a fixed set of orders and never write while paging.

Reading further, the reviewer finds two more issues. The agent raised the maximum page size from 100 to 1,000 in a shared config file ("to make the test simpler"). And it added a new date-parsing library although the project already has one.

None of this would fail CI. The fix takes an hour; finding it in production would have taken much longer. The cost is review time, and the team accepts it: they cap agent PRs at about 400 changed lines so reviews like this stay possible, and for a quarter they track escaped defects and reverts on agent PRs separately to check the cap is doing its job.

## Common traps

- **Approving because the tests pass.** The agent wrote the tests to pass. Check that they test the *requirement*.
- **Reviewing the summary instead of the diff.** Agents write confident PR descriptions. The description is a claim; the diff is the evidence.
- **Blame-shifting.** "The AI did it" in a postmortem hides the real gaps: the review, the checks, the spec. Treat it as a system problem ([[blameless-postmortems]]).
- **Review fatigue.** A flood of small agent PRs can exhaust reviewers as surely as one giant one. Limit work in progress, and count review time as real work.
- **Banning agents from sensitive code by default.** Rules like "no AI in the payments module" are hard to enforce and push use into hiding. Stricter review for sensitive paths usually works better than a blanket ban. Where a ban is genuinely required — by regulation, contract, or very high assurance needs — enforce it with tooling and access, not a memo.

## When it doesn't apply

Throwaway code — a one-off data script you'll delete, a spike to learn an API — needs a sanity check, not a full review. Generated code that a tool regenerates on every build, such as API clients from a schema, is reviewed at the generator and schema, not line by line.

## Related

- [[code-review]] — the general practice; everything there still applies.
- [[spec-first-agent-tasks]] — a written plan is what intent review checks against.
- [[feedback-loops-for-agents]] — automated checks catch the mechanical issues so humans can focus on intent.
- [[agent-guardrails]] — what to enforce outside the review.
- [[adopting-coding-agents]] — review norms are part of the team agreement.
