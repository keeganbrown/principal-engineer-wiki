---
title: Architecture Decision Records (ADRs)
category: practices
summary: Write a short document for each significant technical decision — the context, the choice, and the consequences — so future teammates know why things are the way they are.
tags: [documentation, decision-making, communication]
---

# Architecture Decision Records (ADRs)

> **In one sentence:** Write a short document for each significant technical decision — the context, the choice, and the consequences — so future teammates know why things are the way they are.

## The idea

Every codebase is full of decisions: why Postgres and not Mongo, why events instead of direct calls, why this library. Months later, nobody remembers the reasons. New engineers either fear changing anything or change things without understanding the trade-offs.

An **ADR** is a one-to-two-page record of one decision. They're numbered, stored in the repo next to the code (e.g., `docs/adr/0007-use-postgres.md`), and never deleted — only superseded by newer ADRs.

The format was popularized by Michael Nygard in 2011 and remains one of the cheapest, highest-value habits a team can adopt.

## Why it matters

- **Preserves the "why."** Code shows *what* was built; ADRs explain *why*, including options rejected.
- **Speeds onboarding.** Reading ten ADRs gives a newcomer the history of the architecture in an hour.
- **Improves decisions.** Writing forces clear thinking. Many bad ideas die in the "Consequences" section.
- **Enables async decision-making.** A proposed ADR can be reviewed like a pull request across time zones.

## How to apply it

Use a simple template:

```
# ADR 0007: Use PostgreSQL for the order service

Status: Accepted (2026-03-14)    # or Proposed / Superseded by ADR 0012

## Context
What problem are we solving? What constraints and forces apply?

## Decision
What we chose, stated plainly.

## Options considered
Each option with its main pros and cons.

## Consequences
What becomes easier, what becomes harder, what we must now do.
```

Guidelines:
- Write one when a decision is **costly to reverse** or **affects multiple teams**.
- Keep it short. If it's more than two pages, you may be documenting several decisions.
- Propose it as a PR. Discussion happens in review; the merged ADR is the record.
- Never edit an accepted ADR's decision. Write a new ADR that supersedes it.

## Example

ADR 0012, "Move from synchronous REST calls to events for order fulfillment," notes the context (fulfillment outages were taking down checkout), the options (retries with circuit breakers, a queue, a full event bus), the decision (publish `OrderPlaced` events to a queue), and consequences (fulfillment becomes eventually consistent; we need idempotent consumers and a dead-letter queue). Two years later, a new engineer asks "why is this async?" — and the answer is one link away.

## Common traps

- **Writing ADRs after the fact, for everything.** They become busywork. Focus on significant decisions as they happen.
- **Hiding them in a wiki** far from the code, where they go stale and unseen.
- **Skipping rejected options.** The alternatives are often the most valuable part.
- **Treating ADRs as permission slips.** They record decisions; they don't replace conversation.

## When it doesn't apply

Small, easily reversed decisions — a variable name, a minor library inside one module — don't need an ADR. A good test: "Would a new teammate in a year plausibly ask *why* about this?"

## Related

- [[yagni]] — ADRs are a good place to note "we chose not to build this yet."
- [[conways-law]] — ADRs are a key communication channel across teams.
- [[technical-debt]] — record deliberate shortcuts so they can be repaid later.
- [[code-review]] — propose ADRs as PRs to get the same review benefits.
- [[design-docs]] — explore the problem in a design doc; record the outcome in an ADR.
