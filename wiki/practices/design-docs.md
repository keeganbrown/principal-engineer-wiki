---
title: Writing Design Docs
category: practices
summary: Before building something significant, write a short document explaining the problem, the proposed solution, and the alternatives, so the team can find flaws while they're still cheap to fix.
tags: [documentation, communication, decision-making]
---

# Writing Design Docs

> **In one sentence:** Before building something significant, write a short document explaining the problem, the proposed solution, and the alternatives, so the team can find flaws while they're still cheap to fix.

## The idea

A design doc (sometimes called an RFC or tech spec) is a written proposal for how to build something. It's shared for feedback *before* most of the code exists.

The main purpose isn't documentation — it's **thinking**. Writing forces you to turn a vague plan into concrete decisions, and gives others a chance to spot problems you can't see. Changing a paragraph costs minutes; changing a shipped system costs months.

Design docs and ADRs work together: the design doc explores a problem and proposes a solution; the ADR records the final decision in a page.

## Why it matters

- **Catches big mistakes early.** Reviewers find missing requirements, scaling problems, and security gaps before they're built in.
- **Aligns people.** Product, engineering, and dependent teams agree on scope and approach.
- **Scales your influence.** A clear doc can be read by fifty people across time zones; a meeting reaches only who's in the room.
- **Leaves a trail.** Months later, the doc explains what was intended and why.

## How to apply it

A useful structure:

1. **Context and problem** — what's wrong today, who's affected, why now.
2. **Goals and non-goals** — what success looks like, and what you're deliberately *not* doing. Non-goals prevent scope creep.
3. **Proposed design** — the approach, with a diagram. Enough detail to evaluate, not to implement line by line.
4. **Alternatives considered** — including "do nothing," and why each was rejected.
5. **Risks and open questions** — what could go wrong; what you don't know yet.
6. **Rollout and testing** — how it ships safely, how you'll know it works.
7. **Cross-cutting concerns** — security, privacy, cost, observability, operations.

Guidelines:
- **Write for a smart reader new to the area.** Define terms; lead with the problem.
- **Keep it short.** 2–6 pages is typical. Move details to appendices.
- **Share early as a draft.** A rough doc reviewed early beats a perfect doc reviewed too late.
- **Name reviewers explicitly** and set a deadline for feedback.
- **Resolve comments in writing.** Record decisions in the doc so the discussion isn't lost.

## Example

An engineer plans to add a cache in front of the pricing service. Their design doc's "Alternatives" section compares a local in-memory cache, a shared Redis cache, and precomputing prices nightly. In review, the finance team points out that prices must update within one minute of a change for legal reasons — a requirement nobody on the engineering team knew. The nightly option is dropped, and the cache gets event-based invalidation. Cost of the discovery: one comment. Cost if found after launch: a compliance incident.

## Common traps

- **Writing it after building it.** Then it's documentation, not design.
- **Solution-first docs** that skip the problem, so reviewers can't judge if the solution fits.
- **No alternatives,** which signals the decision was made before the review.
- **Novel-length docs** that nobody finishes.
- **Design by committee.** Gather input widely, but have a clear decision-maker.

## When it doesn't apply

Small, reversible, well-understood changes don't need a doc — a good PR description is enough. A useful rule: write a doc when the work takes more than a couple of weeks, crosses team boundaries, or is hard to undo.

## Related

- [[architecture-decision-records]] — record the outcome of a design doc concisely.
- [[influencing-without-authority]] — clear writing is a principal engineer's main lever.
- [[code-review]] — design review is code review moved earlier.
- [[yagni]] — non-goals are where YAGNI gets written down.
