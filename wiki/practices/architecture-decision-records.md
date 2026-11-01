---
title: Architecture Decision Records (ADRs)
category: practices
summary: Write a short record of each significant technical decision — the context, the choice, and the consequences — so future teammates know why things are the way they are.
tags: [documentation, decision-making, communication]
---

# Architecture Decision Records (ADRs)

> **In one sentence:** Write a short record of each significant technical decision — the context, the choice, and the consequences — so future teammates know why things are the way they are.

## The idea

Every codebase is full of decisions: why Postgres and not MongoDB, why events instead of direct calls, why this library. Months later, nobody remembers the reasons. New engineers either fear changing anything or change things without understanding the trade-offs.

An **architecture decision record (ADR)** is a record, a page or two long, of one decision. ADRs are numbered, stored in the repo next to the code (e.g., `docs/adr/0007-use-postgres.md`), and never deleted — only superseded by newer ADRs.

**ADRs and design docs do different jobs.** A [[design-docs|design doc]] is for *deliberation*: exploring a big problem and getting feedback. An ADR is the *record*: what was decided and why, in a page. A big design doc usually ends in one or more ADRs, but many decisions are too small for a design doc and still deserve an ADR.

Michael Nygard popularized the format in a 2011 blog post.

## Why it matters

- **The "why" survives.** Code shows *what* was built; ADRs explain *why*, including options rejected.
- **Speeds onboarding.** Reading ten ADRs gives a newcomer the history of the architecture in an hour.
- **Makes decisions transparent.** Anyone can see what was decided, by whom, and on what basis.
- **Cheap.** A good ADR takes under an hour to write.

## How to apply it

Nygard's template, plus an "Options considered" section (as in MADR, Markdown Architectural Decision Records):

```
# ADR 0007: Use PostgreSQL for the order service

Status: Accepted (2026-03-14)

## Context
What problem are we solving? What constraints and forces apply?

## Decision
What we chose, stated plainly.

## Options considered
Each option with its main pros and cons.

## Consequences
What becomes easier, what becomes harder, what we must now do.
```

Status is one of Proposed, Accepted, or Superseded by ADR NNNN.

Guidelines:
- **Write one for every significant decision.** "Significant" means costly to reverse, or affecting other teams ([[reversible-decisions]]).
- **Write it while the decision is live.** Reasons reconstructed months later are guesses.
- **Keep it to a page or two.** Longer usually means you're recording several decisions.
- **Propose it as a pull request (PR).** Discussion happens in review; the merged ADR is the record.
- **Supersede, don't edit.** Never change an accepted ADR's decision; write a new one that replaces it.

## Example

ADR 0012, "Move order fulfillment from synchronous calls to events":

- **Context** — when the fulfillment service was down, checkout failed too.
- **Options** — (1) add [[retries-and-timeouts|retries]] and a [[circuit-breaker]]; (2) put a queue between checkout and fulfillment; (3) adopt a full event bus, shared infrastructure every service publishes to.
- **Decision** — option 2: checkout publishes an `OrderPlaced` event to a queue that fulfillment reads ([[event-driven-architecture]]). A full event bus was more than this problem needed.
- **Consequences** — fulfillment now lags checkout by a few seconds; consumers must handle duplicate messages safely ([[idempotency]]); failed messages go to a dead-letter queue (a holding queue for messages that keep failing) that someone must watch.

Two years later, a new engineer asks "why is this async?" — and the answer is one link away.

## Common traps

- **Writing them for everything.** Small, easily reversed decisions turn ADRs into busywork.
- **Backfilling everything at once.** When adopting ADRs on an existing system, backfill only the three to five decisions people most often ask "why?" about.
- **Hiding them in a wiki.** Far from the code, they go stale unseen.
- **Skipping rejected options.** The alternatives are often the most valuable part.
- **Using an ADR to skip the conversation.** Filing an ADR doesn't make a decision agreed. Talk to the affected teams first.
- **Quiet abandonment.** Many ADR habits fade within months. A quick health check: do recent significant decisions have ADRs, and do people link to them in reviews?

## When it doesn't apply

Small, easily reversed decisions — a variable name, a minor library inside one module — don't need an ADR. A good test: "Would a new teammate in a year plausibly ask *why* about this?"

## Related

- [[design-docs]] — explore the problem in a design doc; record the outcome in an ADR.
- [[reversible-decisions]] — one-way doors are the decisions most worth recording.
- [[conways-law]] — ADRs are a key communication channel across teams.
- [[technical-debt]] — record deliberate shortcuts so they can be repaid later.
- [[code-review]] — propose ADRs as PRs to get the same review benefits.
