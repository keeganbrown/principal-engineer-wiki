---
title: Design Docs
category: practices
summary: Before building something significant, write a short document explaining the problem, the proposed solution, and the alternatives, so the team can find flaws while they're still cheap to fix.
tags: [documentation, communication, decision-making]
---

# Design Docs

> **In one sentence:** Before building something significant, write a short document explaining the problem, the proposed solution, and the alternatives, so the team can find flaws while they're still cheap to fix.

## The idea

A design doc (sometimes called an RFC — "request for comments" — or a tech spec) is a written proposal for how to build something. It's shared for feedback *before* the real build starts.

The main purpose isn't documentation — it's **thinking**. Writing forces you to turn a vague plan into concrete decisions, and gives others a chance to spot problems you can't see. Changing a paragraph costs minutes; changing a shipped system costs months.

**Design docs and ADRs do different jobs.** The design doc is for *deliberation*: it explores the problem, compares options, and gathers feedback. The [[architecture-decision-records|architecture decision record (ADR)]] is the *record*: a page or two stating what was decided and why. A design doc usually ends by producing one or more ADRs.

## Why it matters

- **Catches big mistakes early.** Reviewers find missing requirements, scaling problems, and security gaps before they're built in.
- **Aligns people.** Product, engineering, and dependent teams agree on scope and approach.
- **Scales your influence.** A clear doc can be read by fifty people across time zones; a meeting reaches only the people in the room.

## How to apply it

A useful structure:

1. **Context and problem** — what's wrong today, who's affected, why now.
2. **Goals and non-goals** — what success looks like, and what you're deliberately *not* doing. Non-goals prevent scope creep.
3. **Proposed design** — the approach, with a diagram. Enough detail to evaluate, not to implement line by line.
4. **Alternatives considered** — including "do nothing," and why each was rejected.
5. **Risks and open questions** — what could go wrong; what you don't know yet.
6. **Rollout and testing** — how it ships safely (e.g., behind [[feature-flags]]) and how you'll know it works.
7. **Cross-cutting concerns** — security, privacy, cost, [[observability]], operations.

Guidelines:
- **Write for a smart reader new to the area.** Define terms; lead with the problem.
- **Keep it as short as the problem allows.** A few pages is common for a single-team change; large cross-team projects run longer. Move details to appendices.
- **Share early as a draft.** A rough doc reviewed early beats a perfect doc reviewed too late.
- **Name reviewers and a deadline.** Explicit names and dates get feedback; open invitations don't.
- **Resolve comments in writing.** Record decisions in the doc so the discussion isn't lost.

## Example

An engineer plans to add a cache in front of the pricing service. Their design doc's "Alternatives" section compares a local in-memory cache, a shared Redis cache, and precomputing prices nightly.

In review, the finance team points out that prices must update within one minute of a change for legal reasons — a requirement nobody on the engineering team knew. The nightly option is dropped, and the cache gets event-based invalidation (it clears an entry as soon as a "price changed" event arrives). Cost of the discovery: one comment. Cost if found after launch: a compliance incident.

## Common traps

- **Writing it after building the real thing.** Then it's documentation, not design. A throwaway **spike** — quick experimental code built only to answer a technical question — before the doc is fine, often better; the doc still comes before the committed build.
- **Skipping the problem.** Solution-first docs leave reviewers unable to judge whether the solution fits.
- **Listing no alternatives.** It signals the decision was made before the review.
- **Writing a novel.** Nobody finishes it.
- **Design by committee.** Gather input widely, but have a clear decision-maker.

## When it doesn't apply

Small, reversible, well-understood changes don't need a doc — a good pull request description is enough. A useful rule: write a doc when the work takes more than a couple of weeks, crosses team boundaries, or is hard to undo ([[reversible-decisions]]).

Watch for the process turning into bureaucracy. If doc review routinely takes longer than the work it gates, shrink the template or the reviewer list.

## Related

- [[architecture-decision-records]] — record the outcome of a design doc concisely.
- [[reversible-decisions]] — one-way doors are the strongest reason to write one.
- [[influencing-without-authority]] — clear writing is a principal engineer's main lever.
- [[code-review]] — design review is code review moved earlier.
- [[yagni]] — non-goals are where YAGNI ("you aren't gonna need it") gets written down.
