---
title: Code Review
category: practices
summary: Have another engineer read each change before it merges, focusing on correctness, clarity, and design — and keep changes small so reviews are fast and thorough.
tags: [collaboration, quality, mentorship]
---

# Code Review

> **In one sentence:** Have another engineer read each change before it merges, focusing on correctness, clarity, and design — and keep changes small so reviews are fast and thorough.

## The idea

Code review is a second pair of eyes on every change. It catches bugs, but that's not its main value. Reviews **spread knowledge** (more people understand each part of the system), **keep the codebase consistent**, and **teach** — in both directions.

A good review is a conversation between peers about making the code better, not a gate where one person approves another's work.

## Why it matters

- **Shared ownership.** No part of the system is understood by only one person.
- **Earlier feedback.** A design problem caught in review is far cheaper than one caught in production.
- **Mentorship at scale.** For senior engineers, review comments are one of the most effective ways to raise the team's skill level.
- **Readability check.** The reviewer is the first "next reader." If they're confused, future readers will be too.

## How to apply it

**As an author:**
- Keep changes small — ideally under ~400 lines. Review quality drops sharply on large diffs.
- Write a description: *what* changed, *why*, and *how you tested it*.
- Review your own diff first. You'll catch half the comments yourself.
- Separate refactors from behavior changes into different PRs.

**As a reviewer:**
- Review in priority order: **correctness → design → readability → style.** Let tools (linters, formatters) handle style.
- Ask questions instead of issuing orders: "What happens if this list is empty?"
- Label comment weight: `nit:` (optional), `suggestion:`, `blocking:`.
- Respond quickly. Waiting a day for review kills momentum. Aim for within a few working hours.
- Praise good work. It tells people what to keep doing.

## Example

**Unhelpful:** "This is wrong."

**Helpful:** "blocking: if `retryCount` is 0 this loop never runs, so the request is never sent. Should the condition be `<=`? A test for the zero case would lock this down."

The helpful version names the problem, explains the impact, suggests a fix, and points to a test.

## Common traps

- **Rubber-stamping.** Approving without reading defeats the purpose. If you don't have time, say so.
- **Bike-shedding.** Long debates over naming and formatting while missing a race condition.
- **Gatekeeping.** Using reviews to enforce personal preference rather than shared standards.
- **Giant PRs.** "LGTM" on a 3,000-line diff means nobody really reviewed it.
- **Reviewing only code, not tests.** Tests are part of the change and deserve the same scrutiny.

## When it doesn't apply

Pair or ensemble (mob) programming provides continuous review, so a separate async review may add little. Very low-risk changes (typo fixes, docs) can use a lighter process. Emergency fixes may merge first and get reviewed immediately after — but that should be rare and explicit.

## Related

- [[test-driven-development]] — tests make changes easier to review and trust.
- [[architecture-decision-records]] — big design decisions deserve a review before code exists.
- [[technical-debt]] — reviews are a key point for spotting and naming debt.
- [[feature-flags]] — let you merge small, reviewable slices of unfinished features.
- [[design-docs]] — review the design before the code exists.
