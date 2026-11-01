---
title: Conway's Law
category: principles
summary: Systems end up shaped like the communication structure of the teams that build them, so design your teams and your architecture together.
tags: [organization, architecture, teams]
---

# Conway's Law

> **In one sentence:** Systems end up shaped like the communication structure of the teams that build them, so design your teams and your architecture together.

## The idea

In 1968, Melvin Conway observed: "Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."

Put simply: if four teams build a compiler, you'll get a four-pass compiler. Where teams talk easily, components integrate tightly. Where teams rarely talk, you get a clean (or messy) boundary — an API, a file handoff, or a wall.

This isn't a rule you choose to follow. It's a force, like gravity. You can only choose whether to work with it.

## Why it matters

For a principal engineer, this is one of the highest-leverage ideas there is. Architecture problems are often **organization problems in disguise**:

- A service that every team must change for every feature usually reflects a missing team boundary.
- Two services that are constantly out of sync often belong to two teams that don't talk.
- A planned architecture that contradicts the org chart will quietly drift back toward the org chart.

## How to apply it

- **Reverse Conway maneuver.** Decide the architecture you want, then shape teams to match it. Want independent services? Give each a single owning team.
- **Align teams to business domains** (checkout, search, payments), not technical layers (frontend, backend, DBA). Layer teams force every feature through hand-offs.
- **Make ownership explicit.** Every service, repo, and on-call rotation should have exactly one owning team.
- **Mind team cognitive load.** A team can only own so much. If a team owns too many systems, boundaries will rot.
- **When you see a messy boundary in code, look at the communication path** between the teams involved.

## Example

A company has a frontend team, a backend team, and a database team. Every feature needs all three, so every feature needs three backlogs, three priorities, and two hand-offs. The API between frontend and backend becomes a giant, chatty contract that changes weekly.

They reorganize into *product teams* — "Search," "Checkout," "Accounts" — each with frontend, backend, and data skills. Within months, each domain's code becomes more self-contained, and cross-team APIs shrink to what the domains actually share.

## Common traps

- **Reorgs as a silver bullet.** Moving people without changing ownership, incentives, or architecture just reshuffles the problem.
- **Ignoring the law during design reviews.** A beautiful service diagram that needs five teams to coordinate on every change won't stay beautiful.
- **Too many tiny teams.** Very small teams owning very small services can create more coordination, not less.

## When it doesn't apply

For a single small team, Conway's Law has little bite — everyone talks to everyone, so structure is driven by the code itself. It becomes dominant as soon as you have multiple teams working on one product.

## Related

- [[coupling-and-cohesion]] — team boundaries become coupling boundaries.
- [[modular-monolith]] — module ownership lets multiple teams share one deployable.
- [[event-driven-architecture]] — a common way to decouple team-owned services.
- [[architecture-decision-records]] — a channel for cross-team design communication.
- [[domain-driven-design]] — bounded contexts give teams natural ownership boundaries.
- [[influencing-without-authority]] — reshaping team boundaries is mostly persuasion.
