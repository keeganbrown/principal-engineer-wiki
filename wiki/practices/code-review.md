---
title: Code Review
category: practices
summary: Have another engineer read changes before or soon after they merge, focusing on correctness, clarity, and design — and keep changes small so reviews are fast and thorough.
tags: [collaboration, quality, mentorship]
---

# Code Review

> **In one sentence:** Have another engineer read changes before or soon after they merge, focusing on correctness, clarity, and design — and keep changes small so reviews are fast and thorough.

## The idea

Code review is a second pair of eyes on a change. It catches bugs, but that's not its main value. Reviews **spread knowledge** (more people understand each part of the system), **keep the codebase consistent**, and **teach** — in both directions.

A good review is a conversation between peers about making the code better. It also has a cost: mandatory review before every merge is a gate, and waiting at that gate is often the biggest delay in a team's workflow.

## Why it matters

- **Shared ownership.** No part of the system is understood by only one person ([[hero-culture]]).
- **Earlier feedback.** A design problem caught in review is far cheaper than one caught in production.
- **Mentorship at scale.** For senior engineers, review comments are one of the most effective ways to raise the team's skill level.
- **Readability check.** The reviewer is the first "next reader." If they're confused, future readers will be too.

## How to apply it

**As an author:**
- **Keep changes small.** Aim for under about 400 lines per pull request (PR). A well-known SmartBear/Cisco study found that reviewers catch fewer defects beyond roughly 200–400 lines — treat it as a heuristic.
- **Write a description.** Say *what* changed, *why*, and *how you tested it*.
- **Review your own diff first.** You'll catch many of the comments yourself.
- **Separate refactors from behavior changes.** Put them in different PRs.

**As a reviewer:**
- **Review in priority order.** Correctness, then design, then readability, then style. Let linters and formatters handle style ([[paved-roads]]).
- **Ask questions instead of issuing orders.** "What happens if this list is empty?"
- **Label comment weight.** Use `nit:` (optional), `suggestion:`, or `blocking:`.
- **Respond within a few working hours.** Waiting a day kills momentum.
- **Praise good work.** It tells people what to keep doing.

## Example

The change under review:

```
for attempt in range(1, retryCount):
    if send(request): break
```

**Unhelpful comment:** "This is wrong."

**Helpful comment:** "blocking: `range(1, retryCount)` runs `retryCount - 1` times, so with `retryCount = 1` the request is never sent at all. Should this be `range(retryCount)`? A test for `retryCount = 1` would lock this down."

The helpful version names the problem, explains the impact, suggests a fix, and points to a test.

## Common traps

- **Rubber-stamping.** Approving without reading defeats the purpose. If you don't have time, say so.
- **Bike-shedding.** Long debates over naming and formatting while missing a race condition.
- **Gatekeeping.** Using reviews to enforce personal preference rather than shared standards.
- **Giant PRs.** "LGTM" ("looks good to me") on a 3,000-line diff means nobody really reviewed it.
- **Reviewing only code, not tests.** Tests are part of the change and deserve the same scrutiny.

## When it doesn't apply

Mandatory pre-merge review on every change is a policy choice, not a law. Some high-trust teams use **ship / show / ask** (Rouan Wilsenach, martinfowler.com, 2021): *ship* trivial changes directly, *show* low-risk ones by merging and reviewing afterwards, and *ask* for blocking review only on risky or unfamiliar code. Measure how long PRs wait for review; if it's measured in days, the gate costs more than it catches.

Pair or ensemble (mob) programming provides continuous review, so a separate review may add little. Emergency fixes may merge first and get reviewed immediately after — but that should be rare and explicit.

## Related

- [[test-driven-development]] — tests make changes easier to review and trust.
- [[design-docs]] — review the *design* before the code exists.
- [[architecture-decision-records]] — propose architecture decision records (ADRs) as PRs so decisions get the same review as code.
- [[technical-debt]] — reviews are a key point for spotting and naming debt.
- [[feature-flags]] — let you merge small, reviewable slices of unfinished features.
- [[reviewing-ai-generated-code]] — the same practice when an agent wrote the first draft.
- [[bikeshedding]] — when review effort goes to style instead of risk.
